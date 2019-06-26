const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');
const webpack = require('webpack');
const path = require('path');
 
module.exports = {
  mode: 'production',
  context: path.resolve(__dirname, "sid", "cmd", "templates"),
  entry: ['./base.js', './base.scss'],
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",  
      jQuery: "jquery" 
    }),
    new MiniCssExtractPlugin({
      filename: "[name].css",
      chunkFilename: "[id].css"
    }),
    new HtmlWebpackPlugin({
      template: './base.html',
      inlineSource: '.(js|css)$' // embed all javascript and css inline
    }),
    new HtmlWebpackInlineSourcePlugin(),
  ],
  output: {
    path: path.resolve(__dirname, "sid", "cmd", "templates", "compiled")
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader"
        ]
      }
    ]
  }
}
