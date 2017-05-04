/* eslint import/no-extraneous-dependencies: ["error", {"devDependencies": true}] */
const webpack = require('webpack');
const path = require('path');
const nodeExternals = require('webpack-node-externals');

const nodeEnv = process.env.NODE_ENV || 'production';

module.exports = {
    devtool: 'source-map',
    target: 'node',
    entry: [
        'babel-polyfill',
        './src/server.js'
    ],
    output: {
        path: path.join(__dirname, 'build'),
        filename: 'bundle.js'
    },
    externals: [nodeExternals()], // in order to ignore all modules in node_modules folder
    module: {
        loaders: [{
            test: /\.js$/,
            include: path.join(__dirname, 'src'),
            exclude: /node_modules/,
            loaders: ['babel-loader']
        }, {
            test: /\.json$/,
            loader: 'json-loader'
        }]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify(nodeEnv)
        })
    ]
};
