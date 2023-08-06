import { Application } from '@hotwired/stimulus';

import PodcastFormController from './controllers/podcast-form';

window.Stimulus = Application.start();

window.Stimulus.register('podcast-form', PodcastFormController);
