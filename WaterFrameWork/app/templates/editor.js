/*
 * Filename:  editor.js
 * Project:   templates
 * Author:    lwy
 * ***
 * Created:   2025/11/07 Friday 20:18:09
 * Modified:  2025/11/07 Friday 20:22:10
 * ***
 * Description: 核心编辑器组件
 */

import * as monaco from 'monaco-editor';
import { get_from_back_to_container, get_from_back_to_vriable, post_to_back, memory_display } from "./utils";


// 初始化 Monaco Editor
const editor = monaco.editor.create(document.getElementById('editor'), {
	value: `/*
 * Filename:  test.cpp
 * Project:   tests
 * Author:    lwy
 * ***
 * Created:   2025/11/04 Tuesday 16:15:18
 * Modified:  2025/11/04 Tuesday 16:15:21
 * ***
 * Description: test code for debugger
 */

#include <iostream>

using namespace std;

void test(){
    int a = 1;
    return;
}

int main(void){
    int sum = 1;
    int * p = &sum;
    test();
    for(int i = 0; i < 10; i++){
        sum += i;
        *p += i;
    }

    return 0;
}`,
	language: 'cpp', // 语言类型，需与上面插件配置的语言一致
	theme: 'vs-light', // 主题
	lineNumbers: 'on', // 显示行号
	glyphMargin: true, // ! 强制启用行号前的 glyph 区域
});

// 调试状态管理器
const debugState = {
	currentLine: null, // 当前执行行（如 3）
	breakpoints: new Set(), // 断点行（如 Set(3,5)）
	lineData: {}, // 每行额外数据（如变量值）：{3: { variables: { a: 10, p: '0x7fffffffde40' } }}
	decorationIds: null,	// 当前的装饰，是一个字符串数组

	// 更新状态的方法
	update: function (data) {
		Object.assign(this, data);
		this.render(); // 状态变更后重新渲染
	},
	render: function () {
		// TODO 后续实现：渲染断点、当前执行行、变量信息
	}
};

// 动态渲染
debugState.render = function () {
	const decorations = [];
	const { currentLine, breakpoints, lineData } = this;

	// * 清空之前的残留装饰
	if (debugState.decorationIds) editor.deltaDecorations(debugState.decorationIds, []);

	// 1. 渲染断点（行号左侧红点）
	console.log(breakpoints);
	breakpoints.forEach(lineNum => {
		decorations.push({
			range: new monaco.Range(lineNum, 1, lineNum, 1), // 行首位置
			options: {
				isWholeLine: false,
				glyphMarginClassName: 'custom-breakpoint', // 自定义CSS类（红点样式）
			}
		});
	});

	// 在工具栏显式断点列表
	const breakpoints_container = document.getElementById("breakpoints")
	breakpoints_container.textContent = Array.from(breakpoints)

	// ! 将断点列表以 JSON 发送到后端
	post_to_back("post_breakpoints", JSON.stringify(Array.from(breakpoints)))

	// 2. 渲染当前执行行（整行高亮）
	if (currentLine) {
		decorations.push({
			range: new monaco.Range(currentLine, 1, currentLine, Infinity),
			options: {
				isWholeLine: true,
				className: 'custom-current-line', // 高亮样式
			}
		});

		// *  3. 渲染当前行变量信息（行尾提示）——这个可以不实现
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

	// ! 应用所有装饰器（实时更新DOM）
	debugState.decorationIds = editor.deltaDecorations([], decorations);
};

// 1. 点击行号左侧添加/移除断点
editor.onMouseDown(event => {
	// const position = editor.getPosition(event.event.offsetX, event.event.offsetY);
	// ! 首先确定鼠标到底能否检测到点击
	const position = editor.getPosition({
		x: event.event.posx,
		y: event.event.posy
	});

	if (position.column === 1) { // 点击行首区域
		const lineNum = position.lineNumber - 1;

		if (debugState.breakpoints.has(lineNum)) {
			debugState.breakpoints.delete(lineNum);
			console.log("断点关闭:" + lineNum)
		} else {
			debugState.breakpoints.add(lineNum);
			console.log("断点添加:" + lineNum)
		}

		debugState.render();
	}
});

// 2. 模拟调试控制（下一步、继续执行）
document.getElementById('step-btn').addEventListener('click', () => {
	// 执行到下一行 

	// * 获取当前行数
	get_from_back_to_vriable("get_currunt_line", "another-container").then(data => { debugState.currentLine = data["curruntline"] });
	// ! 将其转化为数字
	const nextLine = Number(debugState.currentLine)

	// ! 执行后端的下一步
	get_from_back_to_container("step", "another-container")

	// * 获取变量列表和栈帧调用并显示到容器上
	get_from_back_to_container("get_stacktrace_info", "stacktrace-container")
	get_from_back_to_container("get_debugger_info", "viriables-container")

	debugState.update({
		currentLine: nextLine,
		lineData: {
			[nextLine]: { variables: { a: 10, p: '0x7fffffffde40', '*p': 10 } }
		}
	});
});
