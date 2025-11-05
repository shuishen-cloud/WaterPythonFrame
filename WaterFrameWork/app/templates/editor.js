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
  theme: 'vs-light', // 主题
  lineNumbers: 'on' // 显示行号
});

// 调试状态管理器（单例）
const debugState = {
  currentLine: null, // 当前执行行（如 3）
  breakpoints: new Set(), // 断点行（如 Set(3,5)）
  lineData: {}, // 每行额外数据（如变量值）：{3: { variables: { a: 10, p: '0x7fffffffde40' } }}
  // 更新状态的方法
  update: function (data) {
    Object.assign(this, data);
    this.render(); // 状态变更后重新渲染
  },
  render: function () {
    // TODO 后续实现：渲染断点、当前执行行、变量信息
  }
};

// 动态渲染标记
debugState.render = function () {
  const decorations = [];
  const { currentLine, breakpoints, lineData } = this;

  // 1. 渲染断点（行号左侧红点）
  console.log("start 1. 渲染断点（行号左侧红点）");
  console.log(currentLine, breakpoints);
  breakpoints.forEach(lineNum => {
    decorations.push({
      range: new monaco.Range(lineNum, 1, lineNum, 1), // 行首位置
      options: {
        isWholeLine: false,
        glyphMarginClassName: 'custom-breakpoint', // 自定义CSS类（红点样式）
      }
    });
  });
  console.log("end 1. 渲染断点（行号左侧红点）")
  
  // 2. 渲染当前执行行（整行高亮）
  if (currentLine) {
    decorations.push({
      range: new monaco.Range(currentLine, 1, currentLine, Infinity),
      options: {
        isWholeLine: true,
        className: 'custom-current-line', // 高亮样式
      }
    });

    // *  3. 渲染当前行变量信息（行尾提示）这个可以不实现
    const lineInfo = lineData[currentLine];
    if (lineInfo?.variables) {
      const varText = Object.entries(lineInfo.variables)
        .map(([key, val]) => `${key}=${val}`)
        .join(' | ');
      decorations.push({
        range: new monaco.Range(currentLine, Infinity, currentLine, Infinity),
        options: {
          after: {
            content: ` // ${varText}`,
            className: 'custom-variable-hint', // 变量提示样式
          }
        }
      });
    }
  }

  // 应用所有装饰器（实时更新DOM）
  editor.deltaDecorations([], decorations);
};

// 1. 点击行号左侧添加/移除断点
editor.onMouseDown(event => {
  // const position = editor.getPosition(event.event.offsetX, event.event.offsetY);
  // ! 首先确定鼠标到底能否检测到点击
  const position = editor.getPosition({
    x: event.event.posx,  // 相对于视口的X坐标
    y: event.event.posy   // 相对于视口的Y坐标
  });

  if (position.column === 1) { // 点击行首区域
    const lineNum = position.lineNumber;
    if (debugState.breakpoints.has(lineNum)) {
      debugState.breakpoints.delete(lineNum);
      console.log("断点关闭:" + lineNum)
    } else {
      debugState.breakpoints.add(lineNum);
      console.log("断点添加:" + lineNum)
    }
    console.log("开始渲染")
    debugState.render();
    console.log("渲染结束")
  }
});

// 2. 模拟调试控制（下一步、继续执行）
// document.getElementById('step-btn').addEventListener('click', () => {
//   // 模拟执行到下一行（实际需对接后端调试接口）
//   const nextLine = debugState.currentLine ? debugState.currentLine + 1 : 3;
//   debugState.update({
//     currentLine: nextLine,
//     lineData: {
//       [nextLine]: { variables: { a: 10, p: '0x7fffffffde40', '*p': 10 } } // 模拟后端返回的变量数据
//     }
//   });
// });

