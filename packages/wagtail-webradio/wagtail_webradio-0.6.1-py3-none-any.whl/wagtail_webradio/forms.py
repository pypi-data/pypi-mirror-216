from itertools import groupby

from django import forms
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import Media
from django.template.loader import render_to_string
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.forms.choosers import BaseFilterForm, SearchFilterMixin

from . import (
    GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
    GROUP_RADIO_SHOW_PERMISSION_TYPES,
    has_podcast_sound_file,
)
from .models import GroupRadioShowPermission, RadioShow


class PodcastAdminForm(WagtailAdminModelForm):
    """
    Form used for creating and editing a Podcast in the admin.

    The `sound_url` value or the `sound_file` will be validated on client side
    by loading it as an Audio object. This will trigger the `is_sound_valid`
    field and set the `duration` field if the audio could be loaded.
    """

    is_sound_valid = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.HiddenInput(
            attrs={'data-podcast-form-target': 'isSoundValid'},
        ),
    )

    class Media:
        css = {
            'all': ['wagtail_webradio/admin/css/podcast-form.css'],
        }
        js = (
            'wagtail_webradio/admin/js/{}'.format(
                'podcast-form.js'
                if WAGTAIL_VERSION[0] < 5
                else 'podcast-form_controllers.js'
            ),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not has_podcast_sound_file():
            del self.fields['sound_file']

    def _post_clean(self):
        super()._post_clean()

        if (
            'sound_file' not in self._errors
            and 'sound_url' not in self._errors
            and not self.cleaned_data['is_sound_valid']
        ):
            if 'sound_file' in self.fields and self.cleaned_data['sound_file']:
                self.add_error(
                    'sound_file',
                    ValidationError(
                        _(
                            "Unable to retrieve the duration of this file. "
                            "Check that it is a valid audio file."
                        )
                    ),
                )

            if self.cleaned_data['sound_url']:
                self.add_error(
                    'sound_url',
                    ValidationError(
                        _(
                            "Unable to validate the file at this URL. Check "
                            "that it is a valid audio file by opening it in a "
                            "new tab."
                        )
                    ),
                )


class PodcastFilterForm(SearchFilterMixin, BaseFilterForm):
    """
    Chooser listing filter form for a Podcast.
    """

    radio_show_id = forms.ModelChoiceField(
        queryset=RadioShow.objects.all(),
        empty_label=_("All radio shows"),
        label=_("Radio show"),
        required=False,
        widget=forms.Select(attrs={'data-chooser-modal-search-filter': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_filtering_by_radio_show = False

    def filter(self, objects):
        radio_show_id = self.cleaned_data.get('radio_show_id')
        if radio_show_id:
            self.is_filtering_by_radio_show = True
            objects = objects.filter(radio_show=radio_show_id)
        return super().filter(objects)


class RadioShowPermissionChoiceIterator(ModelChoiceIterator):
    """
    Iterate over permission checkboxes in the same order than what is displayed
    in the header - i.e. the order of ``GROUP_RADIO_SHOW_PERMISSION_TYPES``.
    """

    def __iter__(self):
        assert self.field.empty_label is None, "empty_label should be None"

        indexed_permissions = {obj.codename: obj for obj in self.queryset}

        for codename in GROUP_RADIO_SHOW_PERMISSION_CODENAMES:
            yield self.choice(indexed_permissions.pop(codename))

        assert not indexed_permissions, "Unexpected permission objects left"


class RadioShowPermissionMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Allow the custom labels from ``GROUP_RADIO_SHOW_PERMISSION_TYPES`` to be
    applied to permission checkboxes for the ``RadioShowPermissionsForm``.
    """

    iterator = RadioShowPermissionChoiceIterator

    def label_from_instance(self, obj):
        for codename, label, help_text in GROUP_RADIO_SHOW_PERMISSION_TYPES:
            if codename == obj.codename:
                return help_text

        raise AssertionError(
            "Unexpected permission object '%s'" % obj
        )  # pragma: no cover


class RadioShowPermissionsForm(forms.Form):
    """
    Define the permissions that are assigned to an entity - i.e. group or
    user - for a specific radio show.
    """

    radio_show = forms.ModelChoiceField(
        label=_("Radio show"),
        empty_label=None,
        queryset=RadioShow.objects.all().prefetch_related('group_permissions'),
    )
    permissions = RadioShowPermissionMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=(
            Permission.objects.filter(
                content_type__app_label=RadioShow._meta.app_label,
                codename__in=GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
            ).select_related('content_type')
        ),
    )


class BaseGroupRadioShowPermissionFormSet(forms.BaseFormSet):
    """
    The base formset class for managing ``GroupRadioShowPermission``.

    This class and related ones are adapted from what is produced by
    `wagtail.admin.forms.collections.collection_member_permission_formset_factory`.
    """

    permission_queryset = Permission.objects.filter(
        content_type__app_label=RadioShow._meta.app_label,
        codename__in=GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
    )
    permission_types = GROUP_RADIO_SHOW_PERMISSION_TYPES

    def __init__(
        self,
        data=None,
        files=None,
        instance=None,
        prefix='radio_show_permissions',
    ):
        if instance is None:
            instance = Group()

        if instance.pk is None:
            full_radio_show_permissions = []
        else:
            full_radio_show_permissions = (
                instance.radio_show_permissions.filter(
                    permission__in=self.permission_queryset
                )
                .select_related('permission__content_type', 'radio_show')
                .order_by('radio_show')
            )

        self.instance = instance

        initial_data = []

        # add the group's radio show permissions to initial data
        for radio_show, radio_show_permissions in groupby(
            full_radio_show_permissions,
            lambda obj: obj.radio_show,
        ):
            initial_data.append(
                {
                    'radio_show': radio_show,
                    'permissions': [
                        obj.permission for obj in radio_show_permissions
                    ],
                }
            )

        super().__init__(data, files, initial=initial_data, prefix=prefix)

        for form in self.forms:
            form.fields['DELETE'].widget = forms.HiddenInput()

    @property
    def empty_form(self):
        empty_form = super().empty_form
        empty_form.fields['DELETE'].widget = forms.HiddenInput()
        return empty_form

    def clean(self):
        """Checks that no two forms refer to the same radio show object."""
        if any(self.errors):
            return

        radio_shows = [
            form.cleaned_data['radio_show']
            for form in self.forms
            # need to check for presence of 'radio_show' in cleaned_data,
            # because a completely blank form passes validation
            if form not in self.deleted_forms
            and 'radio_show' in form.cleaned_data
        ]
        if len(set(radio_shows)) != len(radio_shows):
            raise forms.ValidationError(
                gettext(
                    "You cannot have multiple permission records for the same "
                    "radio show."
                )
            )

    @transaction.atomic
    def save(self):
        assert self.instance.pk is not None, (
            "Cannot save a GroupRadioShowPermissionFormSet for an unsaved "
            "group instance"
        )

        forms_to_save = [
            form
            for form in self.forms
            if form not in self.deleted_forms
            and 'radio_show' in form.cleaned_data
        ]

        # get a set of (radio_show, permission) for all ticked permissions
        permission_records = {
            (form.cleaned_data['radio_show'], permission)
            for form in forms_to_save
            for permission in form.cleaned_data['permissions']
        }

        # fetch the group's existing radio show permission records, and from
        # that, build a list of records to be created / deleted
        permission_ids_to_delete = []
        permission_records_to_keep = set()
        for gp in self.instance.radio_show_permissions.filter(
            permission__in=self.permission_queryset
        ):
            if (gp.radio_show, gp.permission) in permission_records:
                permission_records_to_keep.add((gp.radio_show, gp.permission))
            else:
                permission_ids_to_delete.append(gp.id)

        self.instance.radio_show_permissions.filter(
            id__in=permission_ids_to_delete
        ).delete()

        GroupRadioShowPermission.objects.bulk_create(
            [
                GroupRadioShowPermission(
                    group=self.instance,
                    radio_show=radio_show,
                    permission=permission,
                )
                for (radio_show, permission) in (
                    permission_records - permission_records_to_keep
                )
            ]
        )

    def as_admin_panel(self):
        return render_to_string(
            (
                'wagtail_webradio/permissions/includes/'
                'radio_show_permissions_formset.html'
            ),
            {'formset': self},
        )

    @property
    def media(self):
        return (
            Media(
                css={
                    'screen': [
                        'wagtail_webradio/admin/css/radio_show_permissions.css'
                    ]
                }
            )
            + super().media
        )


GroupRadioShowPermissionFormSet = forms.formset_factory(
    RadioShowPermissionsForm,
    formset=BaseGroupRadioShowPermissionFormSet,
    extra=0,
    can_delete=True,
)
