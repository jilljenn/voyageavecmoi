var Webpack = require('webpack');
var path = require('path');

var nodeModulesPath = path.join(__dirname, 'node_modules');
var buildPath = path.join(__dirname, 'build');
var mainPath = path.join(__dirname, 'src', 'app.js');
var mainModulesPath = path.join(__dirname, 'src');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

var config = {
  devtool: 'source-map',
	entry: [
    mainPath
  ],
  output: {
    path: buildPath,
    publicPath: '/public/',
    filename: 'bundle.js'
  },
	plugins: [
    new Webpack.optimize.UglifyJsPlugin(),
    new Webpack.optimize.DedupePlugin(),
    new Webpack.optimize.OccurrenceOrderPlugin(),
    new Webpack.DefinePlugin({
      __DEV__: false
    }),
    new ExtractTextPlugin('app.css')
	],
	resolve: {
		root: mainModulesPath,
    extensions: ['', '.js', '.jsx']
	},
  eslint: {
    configFile: '.eslintrc'
  },
  postcss: function () {
    return [require('autoprefixer')];
  },
	module: {
    preLoaders: [
      {
        test: /\.jsx?$/,
        exclude: [nodeModulesPath],
        include: [mainModulesPath],
        loader: 'eslint-loader'
      }
    ],
		loaders: [
			{
        test: /\.json$/,
        loader: "json-loader"
      },
			{
        test: /\.jsx?$/,
        exclude: [nodeModulesPath],
        include: [mainModulesPath],
        loader: 'babel-loader?stage=0&cacheDirectory'
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "url-loader?limit=10000&minetype=application/font-woff"
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "file-loader"
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader!postcss-loader')
      },
      {
        test: /\.(png|gif)$/,
        loader: 'url-loader?limit=100000'
      },
      {
        test: /\.jpg$/,
        loader: 'file-loader'
      },
		],
	},
};

module.exports = config;
