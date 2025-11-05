const path = require('path');
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = {
  entry: './editor.js', // 入口文件，根据实际项目调整
  output: {
    path: path.resolve(__dirname, '../static/dist'),
    filename: 'editor.js'
  },
  module: {
    rules: [
      // 处理 CSS 文件（monaco-editor 内置样式需要加载）
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      // 处理字体文件（monaco-editor 依赖的图标字体）
      {
        test: /\.ttf$/,
        type: 'asset/resource'
      }
    ]
  },
  plugins: [
    // 配置 Monaco Editor 插件，可按需选择支持的语言和功能（减少打包体积）
    new MonacoWebpackPlugin({
      languages: ['cpp', 'python', 'javascript'], // 仅包含需要的语言，如 C++、Python、JS
      features: ['coreCommands', 'find', 'format'] // 仅包含核心功能
    })
  ]
};