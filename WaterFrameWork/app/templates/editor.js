import * as monaco from 'monaco-editor';

// 初始化 Monaco Editor
const editor = monaco.editor.create(document.getElementById('editor'), {
  value: `// 示例 C++ 代码
#include <iostream>
int main() {
  int a = 10;
  int* p = &a;
  std::cout << *p << std::endl;
  return 0;
}`,
  language: 'cpp', // 语言类型，需与上面插件配置的语言一致
  theme: 'vs-dark', // 主题
  lineNumbers: 'on' // 显示行号
});

