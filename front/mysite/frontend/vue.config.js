const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
module.exports = {
  publicPath: "/",
  outputDir: "../dist",
  assetsDir: "static",
  indexPath: "../templates/index.html",
  transpileDependencies: true,
  devServer: {
    host: "localhost",
    hot: "only",
    proxy: {
      "^/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      config.optimization.minimizer = [
        new TerserPlugin({
          terserOptions: {
            compress: {
              drop_console: true,
            },
          },
        }),
      ];
    }
  },
  chainWebpack: (config) => {
    config.module
      .rule('vue')
      .use('vue-loader')
      .loader('vue-loader')
      .tap((options) => {
        options.compilerOptions = {
          whitespace: 'condense',
          delimiters: ['[[', ']]'],
        };
        return options;
      });

    // Monaco Editorのプラグインを追加
    config.plugin('monaco').use(MonacoWebpackPlugin, [
      {
        languages: ['javascript', 'typescript', 'css', 'html', 'json']
      },
    ]);
  },
};