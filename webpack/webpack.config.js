var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


module.exports = {
  entry: {
    'app': './js/main.js',
  },
  output: {
    path: path.dirname(__dirname) + '/assets/static/gen',
    filename: '[name].js'
  },
  // devtool: '#cheap-module-source-map',
  devtool: '#source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: require.resolve('babel-loader'),
        options: {
          cacheDirectory: true,
        },
      },
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: ['css-loader', 'sass-loader']
        })
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader'
        })
      },
      {
        test: /\.(woff2?|ttf|eot|svg|png|jpe?g|gif)(\?.*)?$/,
        use: require.resolve('url-loader'),
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin({
      filename: 'styles.css',
      allChunks: true
    }),
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
  ]
};
