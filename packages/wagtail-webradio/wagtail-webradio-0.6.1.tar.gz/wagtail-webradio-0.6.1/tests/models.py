from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_webradio.blocks import (
    PodcastChooserBlock,
    PodcastTagChooserBlock,
    RadioShowChooserBlock,
)


class SimplePage(Page):
    body = StreamField(
        [
            ('podcast', PodcastChooserBlock()),
            ('podcast_tag', PodcastTagChooserBlock()),
            ('radio_show', RadioShowChooserBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
