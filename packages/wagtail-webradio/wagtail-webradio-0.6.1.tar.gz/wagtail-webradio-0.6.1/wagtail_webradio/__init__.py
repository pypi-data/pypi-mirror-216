from django.conf import settings
from django.utils.translation import gettext_lazy as _


def has_podcast_sound_file():
    """
    When set to ``False``, the sound file field of a podcast is disabled and it
    is only possible to set the sound by its URL.
    """
    return getattr(settings, 'WEBRADIO_PODCAST_SOUND_FILE', True)


#: The permission codenames of ``RadioShow`` model and any linked model which
#: will be considered when querying all ``RadioShow`` instances for which a
#: user has any direct or indirect permission - e.g. add a podcast.
RADIO_SHOW_ANY_PERMISSION_CODENAMES = (
    'add_radioshow',
    'change_radioshow',
    'delete_radioshow',
    'add_podcast',
    'change_podcast',
    'delete_podcast',
)

#: The permissions related to radio shows which can be granted to a group, as
#: a 3-tuple of the permission codename, its label and its help text.
GROUP_RADIO_SHOW_PERMISSION_TYPES = [
    ('change_radioshow', _("Edit"), _("Edit the radio show")),
    ('add_podcast', _("Add"), _("Add podcasts")),
    ('change_podcast', _("Edit"), _("Edit any podcast")),
    ('delete_podcast', _("Delete"), _("Delete any podcast")),
]

#: The permission codenames related to radio shows.
GROUP_RADIO_SHOW_PERMISSION_CODENAMES = tuple(
    codename for codename, label, help_text in GROUP_RADIO_SHOW_PERMISSION_TYPES
)
