from django import forms

from wagtail.blocks.field_block import FieldBlockAdapter

import pytest

from wagtail_webradio.blocks import (
    PodcastChooserBlock,
    PodcastTagChooserBlock,
    RadioShowChooserBlock,
)
from wagtail_webradio.widgets import PodcastChooserWidget

from .factories import (
    PodcastFactory,
    RadioShowFactory,
    TagFactory,
    TaggedPodcastFactory,
)


class TestBaseSelectChooserBlock:
    def test_get_form_state(self):
        block = RadioShowChooserBlock()

        assert block.get_form_state(1) == ['1']

    def test_form_response(self):
        block = RadioShowChooserBlock()
        radio_shows = RadioShowFactory.create_batch(2)

        value = block.value_from_datadict({'pk': radio_shows[1].pk}, {}, 'pk')
        assert value == radio_shows[1]

    @pytest.mark.parametrize('value', ('', None, '10'))
    def test_form_response_none(self, value):
        block = RadioShowChooserBlock()
        RadioShowFactory.create_batch(2)

        value = block.value_from_datadict({'pk': value}, {}, 'pk')
        assert value is None


class TestPodcastTagChooserBlock:
    def test_serialize(self):
        block = PodcastTagChooserBlock()
        tag = TaggedPodcastFactory().tag

        assert block.get_prep_value(tag) == tag.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = PodcastTagChooserBlock()
        tag = TaggedPodcastFactory().tag

        assert block.to_python(tag.id) == tag
        assert block.to_python(None) is None

    def test_adapt(self):
        block = PodcastTagChooserBlock(help_text="pick a podcast tag")
        block.set_name('test_podcasttagchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_podcasttagchooserblock'
        assert type(js_args[1]) is forms.Select
        assert js_args[2] == {
            'label': 'Podcast tag',
            'required': True,
            'icon': 'tag',
            'helpText': 'pick a podcast tag',
            'classname': (
                'w-field w-field--model_choice_field w-field--select'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_field_queryset(self):
        block = PodcastTagChooserBlock()
        TaggedPodcastFactory.create_batch(2)
        TagFactory.create_batch(3)

        assert block.field.queryset.count() == 2


class TestRadioShowChooserBlock:
    def test_serialize(self):
        block = RadioShowChooserBlock()
        radio_show = RadioShowFactory()

        assert block.get_prep_value(radio_show) == radio_show.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = RadioShowChooserBlock()
        radio_show = RadioShowFactory()

        assert block.to_python(radio_show.id) == radio_show
        assert block.to_python(None) is None

    def test_adapt(self):
        block = RadioShowChooserBlock(help_text="pick a radio show")
        block.set_name('test_radioshowchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_radioshowchooserblock'
        assert type(js_args[1]) is forms.Select
        assert js_args[2] == {
            'label': 'Radio show',
            'required': True,
            'icon': 'microphone',
            'helpText': 'pick a radio show',
            'classname': (
                'w-field w-field--model_choice_field w-field--select'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_field_queryset(self):
        block = RadioShowChooserBlock()
        radio_shows = RadioShowFactory.create_batch(2)

        assert set(block.field.queryset) == set(radio_shows)


class TestPodcastChooserBlock:
    def test_serialize(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        assert block.get_prep_value(podcast) == podcast.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        assert block.to_python(podcast.id) == podcast
        assert block.to_python(None) is None

    def test_adapt(self):
        block = PodcastChooserBlock(help_text="pick a podcast")
        block.set_name('test_podcastchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_podcastchooserblock'
        assert type(js_args[1]) == PodcastChooserWidget
        assert js_args[2] == {
            'label': 'Test podcastchooserblock',
            'required': True,
            'icon': 'headphone',
            'helpText': 'pick a podcast',
            'classname': (
                'w-field w-field--model_choice_field '
                'w-field--podcast_chooser_widget'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_form_response(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        value = block.value_from_datadict(
            {'podcast': str(podcast.id)}, {}, 'podcast'
        )
        assert value == podcast

        empty_value = block.value_from_datadict({'podcast': ''}, {}, 'podcast')
        assert empty_value is None
