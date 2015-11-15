var Webpack = require('webpack');
var path = require('path');

var nodeModulesPath = path.join(__dirname, 'node_modules');
var buildPath = path.join(__dirname, 'build');
var mainPath = path.join(__dirname, 'src', 'app.js');
var mainModulesPath = path.join(__dirname, 'src');

var config = {
  devtool: 'eval',
	entry: [
    'webpack-dev-server/client?http://localhost:8090',
    'webpack/hot/dev-server',
    mainPath
  ],
  output: {
    path: buildPath,
    publicPath: '/public/',
    filename: 'bundle.js'
  },
	plugins: [
    new Webpack.HotModuleReplacementPlugin(),
    new Webpack.DefinePlugin({
      __DEV__: true
    })
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
        loaders: ['react-hot', 'babel-loader?stage=0&cacheDirectory']
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
        loader: 'style-loader!css-loader!postcss-loader'
      },
      {
        test: /\.png$/,
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
