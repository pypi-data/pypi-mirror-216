import datetime
import os

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils import timezone

import pytest
from freezegun import freeze_time

from wagtail_webradio import models

from . import AUDIO_SINE_PATH
from .factories import ImageFactory, PodcastFactory, RadioShowFactory


class TestAutoSlugMixin:
    def test_radioshow_slug(self):
        radioshow = RadioShowFactory.build(title="Ûnicode Show")
        assert radioshow.slug == ''

        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'unicode-show'

    def test_poadcast_slug(self):
        podcast = PodcastFactory.build(
            title="Ûnicode Podcast", radio_show=RadioShowFactory()
        )
        assert podcast.slug == ''

        podcast.full_clean()
        podcast.save()
        assert podcast.slug == 'unicode-podcast'

    def test_generated_slug_update(self):
        radioshow = RadioShowFactory.build(title="A simple Show")
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

        radioshow.slug = ''
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

    def test_generated_slug_suffix(self):
        radioshow = RadioShowFactory.build(title="A simple Show")
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

        radioshow1 = RadioShowFactory.build(title="a Simple show")
        radioshow1.full_clean()
        assert radioshow1.slug == 'a-simple-show-1'

    def test_empty_base_slug(self):
        radioshow = RadioShowFactory.build(title="")

        with pytest.raises(ValidationError) as exc_info:
            radioshow.full_clean()
        assert set(exc_info.value.error_dict.keys()) == {'title', 'slug'}

    def test_slug_unavailable(self):
        RadioShowFactory(title="A simple Show")

        radioshow = RadioShowFactory.build(
            title="A simple Show", slug='a-simple-show'
        )
        with pytest.raises(ValidationError) as exc_info:
            radioshow.full_clean()
        assert set(exc_info.value.error_dict.keys()) == {'slug'}
        assert "already in use" in exc_info.value.messages[0]


class TestGroupRadioShowPermission:
    def test_natural_key(self, change_radioshow_perm):
        group = Group.objects.create(name="A group")
        radio_show = RadioShowFactory()

        obj = models.GroupRadioShowPermission.objects.create(
            group=group,
            radio_show=radio_show,
            permission=change_radioshow_perm,
        )

        assert obj.natural_key() == (group, radio_show, change_radioshow_perm)
        assert (
            models.GroupRadioShowPermission.objects.get_by_natural_key(
                group, radio_show, change_radioshow_perm
            )
            == obj
        )


class TestPodcast:
    def test_no_picture(self):
        podcast = PodcastFactory.build()
        assert podcast.get_picture() is None

    def test_has_picture(self):
        podcast = PodcastFactory.build(
            radio_show=RadioShowFactory(
                picture=ImageFactory(title="RadioShow image")
            ),
            picture=ImageFactory(title="Podcast image"),
        )
        assert podcast.get_picture().title == "Podcast image"

    def test_fallback_radioshow_picture(self):
        podcast = PodcastFactory.build(
            radio_show=RadioShowFactory(
                picture=ImageFactory(title="RadioShow image")
            ),
        )
        assert podcast.get_picture().title == "RadioShow image"

    def test_currents_queryset(self):
        with freeze_time(datetime.datetime(2022, 3, 24, 1)):
            for title, delta in [
                ("yesterday", -1),
                ("today", 0),
                ('tomorrow', 1),
            ]:
                PodcastFactory.create(
                    title=title,
                    publish_date=timezone.now()
                    + datetime.timedelta(days=delta),
                )
            currents_titles = [
                p.title for p in models.Podcast.objects.currents()
            ]
            assert 'yesterday' in currents_titles
            assert 'today' in currents_titles
            assert 'tomorrow' not in currents_titles

    def test_sound_path(self, sound_file_podcast):
        assert sound_file_podcast.sound_file.path == '{}/{}'.format(
            os.path.dirname(__file__),
            f'var/media/podcasts/{sound_file_podcast.slug}.ogg',
        )

    def test_sound_path_by_radioshow(self, settings):
        settings.WEBRADIO_SOUND_PATH_BY_RADIOSHOW = True

        podcast = PodcastFactory(
            sound_file=File(open(AUDIO_SINE_PATH, 'rb')),
            sound_url='',
        )
        radioshow = podcast.radio_show.slug
        sound_file_path = '{}/{}'.format(
            os.path.dirname(__file__),
            f'var/media/podcasts/{radioshow}/{podcast.slug}.ogg',
        )
        assert podcast.sound_file.path == sound_file_path

        # teardown media file
        os.remove(sound_file_path)

    def test_file_url(self, sound_file_podcast):
        assert sound_file_podcast.url == sound_file_podcast.sound_file.url

    def test_external_url(self):
        podcast = PodcastFactory.create(sound_url="https://good.url/sound.mp3")
        assert podcast.url == 'https://good.url/sound.mp3'
