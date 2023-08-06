from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PanelGroup

from .forms import PodcastAdminForm
from .models import Podcast
from .widgets import ClearableFileInput


class PodcastObjectList(PanelGroup):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('base_form_class', PodcastAdminForm)
        super().__init__(*args, **kwargs)

    def get_form_options(self):
        options = super().get_form_options()
        # This hidden input is rendered by the template in order to be a
        # target for the Stimulus controller podcast-form
        options['fields'].append('is_sound_valid')
        return options

    class BoundPanel(PanelGroup.BoundPanel):
        template_name = 'wagtail_webradio/panels/podcast_object_list.html'


class PodcastSoundFieldPanel(PanelGroup):
    class BoundPanel(PanelGroup.BoundPanel):
        template_name = 'wagtail_webradio/panels/podcast_sound_field_panel.html'


radio_show_panels = [
    FieldPanel('title', classname='title full'),
    MultiFieldPanel(
        [
            FieldPanel('description'),
            FieldPanel('picture'),
        ],
        heading=_("Description"),
    ),
    MultiFieldPanel(
        [
            FieldPanel('contact_phone'),
            FieldPanel('contact_email'),
        ],
        heading=_("Contact"),
    ),
]

podcast_panel = PodcastObjectList(
    [
        FieldPanel('title', classname='title full'),
        MultiFieldPanel(
            [
                FieldPanel('description'),
                FieldPanel('picture'),
                FieldPanel('tags'),
            ],
            heading=_("Description"),
        ),
        MultiFieldPanel(
            [
                PodcastSoundFieldPanel(
                    [
                        FieldPanel(
                            'sound_file',
                            widget=ClearableFileInput(
                                attrs={
                                    'data-action': 'podcast-form#retrieve',
                                    'data-podcast-form-target': 'input',
                                }
                            ),
                        ),
                        FieldPanel(
                            'sound_url',
                            widget=forms.URLInput(
                                attrs={
                                    'data-action': 'podcast-form#retrieve',
                                    'data-podcast-form-target': 'input',
                                }
                            ),
                        ),
                    ]
                ),
                FieldPanel(
                    'duration',
                    widget=forms.TimeInput(
                        attrs={
                            'title': _("The format must be HH:MM:SS"),
                            'data-podcast-form-target': 'durationInput',
                            'readonly': True,
                        },
                        format='%H:%M:%S',
                    ),
                ),
            ],
            heading=_("Media"),
        ),
        MultiFieldPanel(
            [
                FieldPanel('publish_date', heading=_("Date")),
            ],
            heading=_("Publishing"),
        ),
    ]
).bind_to_model(Podcast)
