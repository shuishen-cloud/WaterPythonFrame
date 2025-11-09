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

        container.textContent = await response.text()
    } catch (error) {
        container.textContent = "请求出错: ${error.message}";
        container.style.color = 'red';
    }
}

export async function get_from_back_to_vriable(curl_name, container_name) {
    const container = document.getElementById(container_name);

    try {
        const response = await fetch("http://localhost:5000/" + curl_name);
        if (!response.ok) throw new Error("请求失败");

        const response_json =  await response.json()
        
        container.textContent = JSON.stringify(response_json)
        
        return response_json
    } catch (error) {
        container.textContent = "请求出错: ${error.message}";
        container.style.color = 'red';
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
        console.log("Success:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}

export function memory_display() {
	
}