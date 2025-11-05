## 此项目前端开发流程

```shell
npm install monaco-editor monaco-editor-webpack-plugin --save-dev   # 基本的 vscode 编辑包

npm install style-loader css-loader --save-dev      # webpack.config.js 中 module.rules 依赖的模块（是 vscode 的依赖包）

npx webpack --mode development  # 根据 webpack.config.js 的配置文件（第一项的入口目录和）将





```

#### 关键文件是 `webpack.config.js`。可以将其设想为 `CPP` 中的 `CMakeList.txt`。
    
- 指定生成打包内容需要满足的条件。（*至少要知道去哪里找模板，如果是多文件生成*）。
- 生成到什么地方，具体将哪些功能打包进入模块（*plugin -> new MonacoWebpackPlugin*）。

```js
// webpack.config.js

const path = require('path');
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = {
  entry: './editor.js', // 入口文件，多文件则采用[]
  output: {
    path: path.resolve(__dirname, 'static/dist'),
    filename: 'editor.js'   // ! 暂时都打包到一个文件里
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
      features: ['coreCommands', 'find', 'format'] // 仅包含核心功能 ？还有一些什么核心功能
    })
  ]
};
```

#### 如果是 `Flask` 部署运行项目, 静态文件生成的目录 `static` 必须和启动文件夹 `template` 同级才可索引。

```html
<!-- index.html 加载静态文件 -->
  <script src="{{ url_for('static', filename='dist/editor.js') }}"></script>
```

### TODO

-  `webpack.config.js` 中 `plugin` 模块 `features` 字段还有什么功能？ 