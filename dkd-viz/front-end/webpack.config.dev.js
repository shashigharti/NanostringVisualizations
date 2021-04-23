const webpack = require('webpack');
const dotenv = require('dotenv');
const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin');
require('http-proxy-middleware');

module.exports = () => {

    // call dotenv and it will return an Object with a parsed key
    const env = dotenv.config().parsed;

    if (env == null) {
        console.log("ENV not set. Create a .env file in the root folder \n\n");
        return false;
    }

    // reduce it to a nice object, the same as before
    const envKeys = Object.keys(env).reduce((prev, next) => {
        prev[`process.env.${next}`] = JSON.stringify(env[next]);
        return prev;
    }, {});

    return {
        entry: './src/index.js',
        mode: 'development',
        output: {
            path: path.resolve(__dirname, './dist'),
            filename: './app.js',
        },
        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.(s*)css$/,
                    use: [
                        {
                            loader: 'style-loader', // creates style nodes from JS strings
                        },
                        {
                            loader: 'css-loader', // translates CSS into CommonJS
                        },
                        {
                            loader: 'sass-loader', // compiles Sass to CSS
                        },
                    ],
                },
                {
                    test: /\.(jpe?g|png|gif|svg)$/i,
                    loader: 'file-loader?name=/images/[name].[ext]',
                },
                {
                    test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[name].[ext]',
                                outputPath: 'fonts/',
                            },
                        },
                    ],
                },
            ],
        },
        plugins: [
            new HtmlWebPackPlugin({
                template: './src/index.html',
                filename: './index.html',
            }),
            new webpack.DefinePlugin(envKeys),
            new webpack.optimize.ModuleConcatenationPlugin(),
        ],
        devServer: {
            historyApiFallback: true,
            proxy: {
                '/api': env.API_ENDPOINT,
            }
        },
        devtool: 'cheap-module-eval-source-map'
    };
};
