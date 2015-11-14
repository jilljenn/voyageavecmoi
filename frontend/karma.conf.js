var Webpack = require('webpack');
var _ = require('lodash');

module.exports = function (config) {
  var webpackDevConfig = _.omit(_.merge(require('./webpack.config.js'), {
    devtool: 'inline-source-map'
  }), 'entry', 'output', 'plugins');
  for (var loader in webpackDevConfig.module.loaders) {
    if (loader.test === /\.jsx?$/) {
      delete loader.loaders;
      loader.loader = 'babel-loader?stage=0&cacheDirectory';
    }
  }
  config.set({
    browsers: ['Chrome'],
    singleRun: true,
    frameworks: ['mocha'],
    files: [
      'tests.webpack.js'
    ],
    preprocessors: {
      'tests.webpack.js': ['webpack', 'sourcemap']
    },
    reporters: ['dots'],
    webpack: webpackDevConfig,
    webpackServer: {
      noInfo: true
    }
  });
}
