from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

import magic

DEFAULT_ALLOWED_AUDIO_MIME_TYPES = [
    'audio/ogg',
    'audio/mpeg',
    'audio/flac',
    'audio/opus',
]

# Note that magic fails if size is too short.
MAGIC_READ_SIZE = 5 * (1024 * 1024)  # 5M


def validate_audio_file_type(value):
    allowed_mime_types = getattr(
        settings,
        'WEBRADIO_ALLOWED_AUDIO_MIME_TYPES',
        DEFAULT_ALLOWED_AUDIO_MIME_TYPES,
    )

    content = value.file.read(MAGIC_READ_SIZE)
    mime = magic.from_buffer(content, mime=True)

    if mime not in allowed_mime_types:
        raise ValidationError(
            _(
                "File type “%(mimetype)s” is not allowed. Allowed file types "
                "are: %(allowed_mimetypes)s."
                % {
                    'mimetype': mime,
                    'allowed_mimetypes': ', '.join(allowed_mime_types),
                }
            ),
            code='invalid_mimetype',
        )
