from django.contrib.admin.utils import quote
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail.admin.ui.tables import Column, DateColumn, TitleColumn

from ..models import Podcast, RadioShow
from ..panels import podcast_panel, radio_show_panels
from ..permissions import (
    podcast_permission_policy,
    radio_show_permission_policy,
)
from ..ui import RadioShowPodcastsColumn
from . import generic

# RADIO SHOWS
# ------------------------------------------------------------------------------


class RadioShowViewMixin:
    model = RadioShow
    permission_policy = radio_show_permission_policy
    header_icon = 'microphone'


class RadioShowIndexView(RadioShowViewMixin, generic.IndexView):
    page_title = _("Radio shows")
    add_item_label = _("Add a radio show")

    podcasts_index_url_name = None

    def get_columns(self):
        return [
            TitleColumn(
                'title', get_url=self.get_edit_url, label=gettext("Title")
            ),
            RadioShowPodcastsColumn(
                'podcasts', get_url=self.get_podcasts_index_url
            ),
        ]

    def get_queryset(self):
        return self.permission_policy.instances_user_has_any_permission_for(
            self.request.user
        )

    def get_edit_url(self, instance):
        if self.permission_policy.user_has_permission_for_instance(
            self.request.user, 'change', instance
        ):
            return super().get_edit_url(instance)

    def get_podcasts_index_url(self, instance):
        if podcast_permission_policy.user_has_any_permission_for_radio_show(
            self.request.user, ['add', 'change', 'delete'], instance
        ):
            return reverse(
                self.podcasts_index_url_name, args=(quote(instance.pk),)
            )


class RadioShowCreateView(RadioShowViewMixin, generic.CreateView):
    page_title = _("Add radio show")
    success_message = _("Radio show '%(object)s' added.")

    panels = radio_show_panels


class RadioShowEditView(RadioShowViewMixin, generic.EditView):
    error_message = _("The radio show could not be saved due to errors.")
    success_message = _("Radio show '%(object)s' updated.")

    panels = radio_show_panels


class RadioShowDeleteView(RadioShowViewMixin, generic.DeleteView):
    confirmation_message = _("Are you sure you want to delete this radio show?")
    success_message = _("Radio show '%(object)s' deleted.")


# PODCASTS OF A RADIO SHOW
# ------------------------------------------------------------------------------


class PodcastViewMixin:
    model = Podcast
    permission_policy = podcast_permission_policy
    header_icon = 'headphone'


class RadioShowPodcastIndexView(PodcastViewMixin, generic.IndexView):
    page_title = _("Podcasts of")
    add_item_label = _("Add a podcast")
    # Bypass PermissionCheckedMixin, permission is checked for the radio show
    any_permission_required = None

    columns = [
        TitleColumn(
            'title',
            label=_("Title"),
            url_name='wagtail_webradio:podcast_edit',
            sort_key='title',
        ),
        Column(
            'get_duration_display', label=_("Duration"), sort_key='duration'
        ),
        DateColumn(
            'publish_date', label=_("Publish date"), sort_key='publish_date'
        ),
    ]

    def dispatch(self, request, *args, **kwargs):
        self.radio_show = get_object_or_404(
            RadioShow.objects.prefetch_related('podcasts'),
            pk=self.kwargs['radioshow_id'],
        )
        if not self.permission_policy.user_has_any_permission_for_radio_show(
            self.request.user, ['add', 'change', 'delete'], self.radio_show
        ):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.radio_show.podcasts.all()

    def get_index_url(self):
        return reverse(self.index_url_name, args=(quote(self.radio_show.pk),))

    def get_add_url(self):
        if self.permission_policy.user_has_permission_for_radio_show(
            self.request.user, 'add', self.radio_show
        ):
            return reverse(self.add_url_name, args=(quote(self.radio_show.pk),))

    def get_page_subtitle(self):
        return self.radio_show.title


class RadioShowPodcastCreateView(PodcastViewMixin, generic.CreateView):
    page_title = _("Add podcast in")
    success_message = _("Podcast '%(object)s' added.")
    # Bypass PermissionCheckedMixin, permission is checked for the radio show
    permission_required = None

    panel = podcast_panel

    def dispatch(self, request, *args, **kwargs):
        self.radio_show = get_object_or_404(
            RadioShow.objects.all(),
            pk=self.kwargs['radioshow_id'],
        )
        if not self.permission_policy.user_has_permission_for_radio_show(
            self.request.user, 'add', self.radio_show
        ):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.index_url_name, args=(quote(self.radio_show.pk),))

    def get_add_url(self):
        return reverse(self.add_url_name, args=(quote(self.radio_show.pk),))

    def get_form(self):
        form = super().get_form()
        form.instance.radio_show = self.radio_show
        return form

    def get_page_subtitle(self):
        return self.radio_show.title


class PodcastEditView(PodcastViewMixin, generic.EditView):
    error_message = _("The podcast could not be saved due to errors.")
    success_message = _("Podcast '%(object)s' updated.")

    panel = podcast_panel

    def get_queryset(self):
        return super().get_queryset().select_related('radio_show')

    def get_success_url(self):
        return reverse(
            self.index_url_name, args=(quote(self.object.radio_show_id),)
        )


class PodcastDeleteView(PodcastViewMixin, generic.DeleteView):
    confirmation_message = _("Are you sure you want to delete this podcast?")
    success_message = _("Podcast '%(object)s' deleted.")

    def get_queryset(self):
        return super().get_queryset().select_related('radio_show')

    def get_success_url(self):
        return reverse(
            self.index_url_name, args=(quote(self.object.radio_show_id),)
        )
