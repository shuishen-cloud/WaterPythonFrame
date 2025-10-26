'''
Filename:  JsonParser.py
Project:   core
Author:    lwy
***
Created:   2025/10/26 Sunday 18:06:22
Modified:  2025/10/26 Sunday 18:07:07
***
Description: 
'''

import json


if __name__ == "__main__":
    json_data_from_file = """
    {
        "name":"lwy",
        "age":20,
        "is_student":false,
        "hobbies":["reading", "coding"],
        "address":null
    }
    """

    # * 将 Json 文件中的配置读取为 Python 变量

    python_data_from_json = json.loads(json_data_from_file)
    print(python_data_from_json)

    # TODO 使用 Python 语法读取变量没有自动补全，写起来不是很危险？
    # 单独读取变量以键值对格式进行
    print(f" python_data_from_json[\"name\"]: {python_data_from_json["name"]}")

    # * 将 Python 变量写为 Json 文件
    python_data_from_json["name"] = "lwf"
    json_data_from_python = json.dumps(python_data_from_json, ensure_ascii = False, indent = 4)
    print(json_data_from_python)
    