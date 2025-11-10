/*
 * Filename:  utils.js
 * Project:   templates
 * Author:    lwy
 * ***
 * Created:   2025/11/07 Friday 20:21:39
 * Modified:  2025/11/07 Friday 20:22:14
 * ***
 * Description: 
 */

/*
 * 首先来封装 POST 和 GET 请求
*/

export async function get_from_back_to_container(curl_name, container_name) {
	const container = document.getElementById(container_name);

	try {
		const response = await fetch("http://localhost:5000/" + curl_name);
		if (!response.ok) throw new Error("请求失败");

		container.textContent = await response.text();
	} catch (error) {
		container.textContent = `请求出错: ${error.message}`;
		container.style.color = 'red';
	}
}

export async function get_from_back_to_vriable(curl_name) {
	try {
		const response = await fetch("http://localhost:5000/" + curl_name);
		if (!response.ok) throw new Error("请求失败");

		const response_json = await response.json();

		return response_json;
	} catch (error) {
		console.log(`请求出错: ${error.message}`);
	}
}

export async function post_to_back(curl_name, body_message = JSON.stringify({ key1: "value1", key2: "value2" })) {
	try {
		const response = await fetch("http://localhost:5000/" + curl_name, {
			method: "POST",
			headers: {
				"Content-Type": "application/json" // 设置请求头，指定内容类型为 JSON
			},
			body: body_message
		});

		if (!response.ok) throw new Error("POST 请求失败 $ {response.statusText} ");
		const data = await response.json();
		console.log("请求成功:", data);
	} catch (error) {
		console.error("请求出错:", error);
	}
}

/**
 * 获取后端的信息并且选择赋值为变量还是显示在 div 上
 * @param {string} curl_name 后端的接口字段
 * @param {string} container_name 容器的 id
 * @returns 若使用获取到变量，则返回需要构造的变量
 * @todo 是不是将这两个方法的代码直接合并在一起也不错？
 */
export async function get_from_back(curl_name, container_name){
	if(arguments.length == 1){
		const variable = get_from_back_to_vriable(curl_name);
		return variable;
	}else if(arguments.length == 2){
		const container = get_from_back_to_container(curl_name, container_name);
	}
}

/**
 * 在指定的 canvas_div 中渲染内存分布图
 * @param {*} stack_info 栈帧调用信息
 * @param {*} viriables_info 变量信息
 * @description 首先声明一个列表，列表的元素是栈帧信息（尤其是栈的地址）以及里边的变量，根据元素的 数目+1 来切割整个 `canvas` 绘图区，最顶层正在执行的栈分配两个绘图区以彰显其正在运行和展示变量信息。
 * @example
	stack_info = ["#0 test () at ../../tests/test_program2.cpp:18", "#1 0x0000555555555172 in main () at ../../tests/test_program2.cpp:24"]
	viriables_info = ["sum = -137699088", "p = 0x7fffffffdc30"]
 */
export function memory_display(stack_info, viriables_info, canvas_div='memeory-display-canvas') {
	stack_info = ["#0 test () at ../../tests/test_program2.cpp:18", "#1 0x0000555555555172 in main () at ../../tests/test_program2.cpp:24"]
	viriables_info = ["i = 0", "sum = -137699088", "p = 0x7fffffffdc30"]

	var memory_blocks = [[String, [String], Number]]	// * 分别存储栈，变量列表，还有行数

	// * 构建内存分布 memory_blocks
	
	var canvas = document.getElementById(canvas_div);
	var ctx = canvas.getContext('2d');
	var width = 200, length = 400;

	// * 根据 memory_blocks 来逐渐构建

	var block_length = length / (stack_info.length + 1)

	for (var i = 0; i < block_length - 1; i++) {
		ctx.beginPath();
		ctx.rect(0, i * block_length, 200, block_length);

		ctx.fillStyle = "yellow";
		ctx.fill();

		ctx.lineWidth = 5;
		ctx.strokeStyle = "black";
		ctx.stroke();

		// 渲染栈信息
		ctx.font = "12px Arial";
		ctx.fillStyle = "black";
		ctx.fillText(stack_info[i], 10, i * block_length + block_length / 4);

		// 渲染栈内变量的信息
		ctx.font = "10px Arial";
		ctx.fillStyle = "black";

		for (var j = 0; j < viriables_info.length; j++) {
			ctx.fillText(viriables_info[j], 15, j * block_length / 3 + block_length / 6);
		}
	}
}