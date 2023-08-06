from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.panels import ObjectList
from wagtail.admin.views import generic


class PanelMixin:
    #: The base form class to use for the panel.
    base_form_class = None

    #: The panel to use for the model in this view.
    panels = []

    def get_panel(self):
        if getattr(self, 'panel', None):
            return self.panel
        elif self.panels:
            return ObjectList(
                self.panels,
                base_form_class=self.base_form_class,
            ).bind_to_model(self.model)


class InstancePermissionCheckedMixin:
    #: An action name the user must have on an instance.
    permission_required_for_instance = None

    #: A list of action names the user must have on an instance.
    any_permission_required_for_instance = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if getattr(self, 'permission_policy', None) is not None:
            if self.permission_required_for_instance is not None:
                if not self.user_has_permission_for_instance(
                    self.permission_required_for_instance, obj
                ):
                    raise PermissionDenied

            if self.any_permission_required_for_instance is not None:
                if not self.user_has_any_permission_for_instance(
                    self.any_permission_required_for_instance, obj
                ):
                    raise PermissionDenied

        return obj

    def user_has_permission_for_instance(self, permission, obj):
        return self.permission_policy.user_has_permission_for_instance(
            self.request.user, permission, obj
        )

    def user_has_any_permission_for_instance(self, permissions, obj):
        return self.permission_policy.user_has_any_permission_for_instance(
            self.request.user, permissions, obj
        )


class IndexView(generic.IndexView):
    template_name = 'wagtail_webradio/generic/index.html'


class CreateView(PanelMixin, generic.CreateView):
    template_name = 'wagtail_webradio/generic/create.html'

    def get_success_message(self, instance):
        # FIXME: As of Wagtail 4.2, string formatting is named and old style
        if self.success_message is None:
            return None
        return self.success_message % {'object': instance}


class EditView(InstancePermissionCheckedMixin, PanelMixin, generic.EditView):
    permission_required = None
    permission_required_for_instance = 'change'
    template_name = 'wagtail_webradio/generic/edit.html'

    def get_success_message(self):
        # FIXME: As of Wagtail 4.2, string formatting is named and old style
        if self.success_message is None:
            return None
        return self.success_message % {'object': self.object}


class DeleteView(InstancePermissionCheckedMixin, generic.DeleteView):
    permission_required = None
    permission_required_for_instance = 'delete'
    template_name = 'wagtail_webradio/generic/confirm_delete.html'

    def get_success_message(self):
        # FIXME: As of Wagtail 4.2, string formatting is named and old style
        if self.success_message is None:
            return None
        return self.success_message % {'object': self.object}

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError as e:
            context = self.get_context_data(
                protected_objects=self.format_protected_objects(
                    e.protected_objects
                )
            )
            return self.render_to_response(context)

    def format_protected_objects(self, objects):
        """
        Generate a list of 2-tuple with the string describing the object and
        its admin edit URL from the one which have a protected relation to the
        item to delete.
        """
        url_finder = AdminURLFinder(self.request.user)

        return [
            (
                _('{model}: {object}').format(
                    model=capfirst(obj.__class__._meta.verbose_name), object=obj
                ),
                url_finder.get_edit_url(obj),
            )
            for obj in objects
        ]
