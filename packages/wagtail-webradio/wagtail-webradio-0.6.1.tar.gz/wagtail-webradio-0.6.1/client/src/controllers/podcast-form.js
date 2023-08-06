import { Controller } from '@hotwired/stimulus';

/**
 * Format the time from seconds to HH:MM:SS.
 * @param {Number} seconds
 * @return {String}
 */
function formatDuration(seconds) {
  return new Date(1000 * seconds).toISOString().substr(11, 8);
}

export default class extends Controller {
  static targets = ['durationInput', 'input', 'isSoundValid'];

  inputTargetConnected(element) {
    const url = element.attributes.getNamedItem('value')?.value;

    if (url) {
      this.retrieve({ params: { url }});
    }
  }

  // Actions

  /**
   * Retrieve the duration of an audio file either defined by a `url`
   * parameter or by the value of the element that dispatched the event.
   */
  retrieve({ target, params }) {
    let url;

    this.isSoundValidTarget.value = '0';

    if (params.url) {
      url = params.url;
    } else if (target) {
      url = target.files
        ? URL.createObjectURL(target.files[0])
        : target.value;
    }

    if (!url) {
      this.durationInputTarget.value = '';

      throw new Error(`Unable to get the sound URL from ${target}`);
    }

    const audio = new Audio();
    audio.preload = 'metadata';

    audio.addEventListener('error', () => {
      this.durationInputTarget.value = '';
    });
    audio.addEventListener('loadedmetadata', () => {
      this.durationInputTarget.value =
        audio.duration === Infinity ? '' : formatDuration(audio.duration);
      this.isSoundValidTarget.value = '1';
    });

    audio.src = url;
  }
}
