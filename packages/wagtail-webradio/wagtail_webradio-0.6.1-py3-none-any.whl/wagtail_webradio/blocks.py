from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.coreutils import resolve_model_string

from .views.chooser import podcast_chooser_viewset


class BaseSelectChooserBlock(blocks.ChooserBlock):
    """
    Abstract class for fields that implement a chooser interface for a
    model with a Select widget.
    """

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.get_queryset(),
            widget=self.widget,
            required=self._required,
            validators=self._validators,
            help_text=self._help_text,
        )

    @cached_property
    def widget(self):
        return forms.Select()

    def value_from_form(self, value):
        if value == '':
            return None
        return super().value_from_form(value)

    def get_form_state(self, value):
        return blocks.FieldBlock.get_form_state(self, value)

    def get_queryset(self):
        """Return the queryset to use for the field."""
        return self.model_class.objects.all()


class RadioShowChooserBlock(BaseSelectChooserBlock):
    class Meta:
        label = _("Radio show")
        icon = 'microphone'

    @cached_property
    def target_model(self):
        return resolve_model_string('wagtail_webradio.RadioShow')


class PodcastTagChooserBlock(BaseSelectChooserBlock):
    class Meta:
        label = _("Podcast tag")
        icon = 'tag'

    @cached_property
    def tagged_model(self):
        return resolve_model_string('wagtail_webradio.TaggedPodcast')

    @cached_property
    def target_model(self):
        return self.tagged_model.tag_model()

    def get_queryset(self):
        return self.tagged_model.tags_for()


PodcastChooserBlock = podcast_chooser_viewset.get_block_class(
    name='PodcastChooserBlock', module_path='wagtail_webradio.blocks'
)
