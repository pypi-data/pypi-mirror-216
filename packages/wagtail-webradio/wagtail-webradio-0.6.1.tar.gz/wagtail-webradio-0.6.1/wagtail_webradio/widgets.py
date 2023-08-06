from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .views.chooser import podcast_chooser_viewset

PodcastChooserWidget = podcast_chooser_viewset.widget_class


class ClearableFileInput(widgets.ClearableFileInput):
    initial_text = _('Currently:')
    template_name = 'wagtail_webradio/widgets/clearable_file_input.html'

    class Media:
        css = {'all': ('wagtail_webradio/admin/css/clearable_file_input.css',)}
