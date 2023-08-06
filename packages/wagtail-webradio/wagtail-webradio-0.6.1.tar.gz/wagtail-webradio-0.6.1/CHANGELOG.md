# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.6.1 - 2023-06-28
### Fixed
- Load the required scripts in the create and edit admin views to fix the
  link feature of the Draftail editor

## 0.6.0 - 2023-06-21

**Breaking changes!** The following settings have been renamed:
- ``WEBRADIO_SOUND_FILE`` to ``WEBRADIO_PODCAST_SOUND_FILE``
- ``WEBRADIO_AUTHORIZED_MIME_TYPES`` to ``WEBRADIO_ALLOWED_AUDIO_MIME_TYPES``

### Added
- Add a separator in the add and edit views of a `Podcast` between the sound
  file and the sound URL

### Changed
- Add support for Wagtail 4.1 LTS & 5.0 and remove other unmaintained Wagtail
  and Django versions
- Improve the validation of the `Podcast` sound fields and attach the errors
  to the related fields
- Set the `Podcast` duration field as readonly

## 0.5.0 - 2022-11-26
### Added
- ``WEBRADIO_SOUND_PATH_BY_RADIOSHOW`` setting to store sound files in a
  RadioShow folder

## 0.4.5
### Fixed
- JavaScript error when ``WEBRADIO_SOUND_FILE = False``

## 0.4.4 - 2022-06-28
### Fixed
- Edit a `Podcast` with a soundfile can be saved without upload it twice

## 0.4.3 - 2022-06-17
### Fixed
- ``WEBRADIO_AUTHORIZED_MIME_TYPES`` settings is correctly catched

## 0.4.2 - 2022-06-03
### Fixed
- The player car retrieve URL from sound file

## 0.4.1 - 2022-05-09
### Fixed
- Fix upload failure when magic needs a large buffer to identify the format

## 0.4.0 - 2022-05-09
### Added
- Podcast can be sorted by ``title`` in index admin view
- ``sound_file`` field to Podcast
- add ``description`` fields to search index

## 0.3.0 - 2022-03-24
### Added
- ``get_picture`` podcast method that fallback to RadioShow picture if no one
  is defined.
- ``currents`` queryset method that filter the incoming podcacsts

### Fixed
- inconsistent playlists bug which occur when running in a mutli-process
  production environement

## 0.2.1 - 2022-02-28
### Changed
- Show the podcast duration in the listing view of the admin

## 0.2.0 - 2022-02-28
### Added
- ``duration`` field on Podcast which is retrieved in the admin on client side
  from the ``sound_url`` value
- Player component with a dynamic playlist using django-unicorn

### Changed
- Replace the server side validation of ``sound_url`` - controlled with the
  setting ``WEBRADIO_VALIDATE_PODCAST_URL`` - by a client side validation to
  ensure it is an audio file

## 0.1.0 - 2022-02-14

This is the initial release which provides the basis - e.g. the models, admin
views and chooser blocks.
