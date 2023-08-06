module.exports = {
  env: {
    browser: true,
    node: true,
  },
  parser: '@babel/eslint-parser',
  extends: [
    'eslint:recommended',
    'airbnb-base',
    'prettier',
  ],
  rules: {
    'class-methods-use-this': 'off',
    'comma-dangle': ['error', 'always-multiline'],
  },
  overrides: [
    {
      files: ['rollup.config.mjs'],
      rules: {
        'import/no-extraneous-dependencies': 'off',
      },
    },
  ],
}
