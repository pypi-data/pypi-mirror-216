import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';

const PRODUCTION = process.env.NODE_ENV === 'production';

function addInput(inputFilename, outputFilename) {
  return {
    input: `client/src/${inputFilename}`,
    output: {
      file: `wagtail_webradio/static/wagtail_webradio/${outputFilename}`,
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      resolve(),
      babel({ babelHelpers: 'bundled' }),
      PRODUCTION && terser(),
    ],
  };
}

export default [
  addInput('admin-podcast-form.js', 'admin/js/podcast-form.js'),
  addInput('admin-podcast-form_controllers.js', 'admin/js/podcast-form_controllers.js'),
  addInput('player.js', 'player/js/main.js'),
];
