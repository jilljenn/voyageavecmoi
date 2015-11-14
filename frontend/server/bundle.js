var Webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var webpackConfig = require('./../webpack.config.js');

module.exports = function() {

    // First we create Webpack using our webpack config
    var bundleStart = null;
    var compiler = Webpack(webpackConfig);

    // We hook when we start building
    compiler.plugin('compile', function() {
        console.log('Bundling...');
        bundleStart = Date.now();
    });

    // We hook we we are done building
    compiler.plugin('done', function() {
        console.log('Bundled in ' + (Date.now() - bundleStart) + 'ms!');
    });

    var bundler = new WebpackDevServer(compiler, {

        // We serve the app from the build path.
        // It makes the proxying simpler:
        // http://localhost:8090/build -> http://localhost:8085/build
        publicPath: '/build/',

        // Configure hot replacement
        hot: true,

        // The rest is terminal configurations
        quiet: false,
        historyApiFallback: true,
        stats: {
            colors: true,
            chunkModules: false
        }
    });

    bundler.listen(8090, 'localhost', function() {
        console.log('Bundling project, please wait...');
    });

};
