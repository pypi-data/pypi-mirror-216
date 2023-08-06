from django.utils.translation import gettext_lazy as _

from wagtail.admin.ui.tables import Column, DateColumn
from wagtail.admin.views.generic.chooser import (
    BaseChooseView,
    ChooseResultsViewMixin,
    ChooseViewMixin,
    CreationFormMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet

from ..models import Podcast
from ..permissions import podcast_permission_policy


class BasePodcastChooseView(BaseChooseView):
    @property
    def columns(self):
        return super().columns + [
            Column('radio_show', label=_("Radio show")),
            DateColumn('publish_date', label=_("Publish date")),
        ]

    def get_filter_form_class(self):
        from ..forms import PodcastFilterForm

        return PodcastFilterForm


class PodcastChooseView(
    ChooseViewMixin, CreationFormMixin, BasePodcastChooseView
):
    pass


class PodcastChooseResultsView(
    ChooseResultsViewMixin, CreationFormMixin, BasePodcastChooseView
):
    pass


class PodcastChooserViewSet(ChooserViewSet):
    model = Podcast
    permission_policy = podcast_permission_policy

    icon = 'headphone'
    choose_one_text = _("Choose a podcast")
    choose_another_text = _("Choose another podcast")
    edit_item_text = _("Edit this podcast")

    choose_view_class = PodcastChooseView
    choose_results_view_class = PodcastChooseResultsView


podcast_chooser_viewset = PodcastChooserViewSet(
    'wagtail_webradio_podcast_chooser',
    url_prefix='webradio/podcast/chooser',
)
