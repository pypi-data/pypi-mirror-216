import PodcastFormController from './controllers/podcast-form';

if (!window.Stimulus) {
  throw new Error("You must instantiate a Stimulus application at first.");
}

window.Stimulus.register('podcast-form', PodcastFormController);
