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


class WJsonParser():
    """
    读取字符串比较简单，所以不需要封装，但是文件有 with 语法，也有多余需要注意的语法，需要封装。
    """

    def __init__(self):
        self.json_file = None
        self.file_path = None
    
    def load_from_json_file(self, file_path : str):
        self.file_path = file_path
        with open(file_path, 'r', encoding = "utf-8") as file:
            self.json_file_content = json.load(file)
        
        return self.json_file_content

    def write_to_json_file(self, content : str):
        with open(self.file_path, 'w', encoding = "utf-8") as file:
            json.dump(content, file, ensure_ascii = False, indent = 4)


if __name__ == "__main__":
    """
    # TODO 使用 Python 语法读取变量没有自动补全，写起来不是很危险？    
    
    * 剩下的就是将 Json 设置为读取核心配置的类

    ? 要不要将读取的数据封装到 Json 对象中呢？——算了。
    """    
    
    # ============================ 面向对象测试 ===========================

    json_parser = WJsonParser()
    json_file_content = json_parser.load_from_json_file("tests/test.json")
    print(f"{json_file_content["name"]}")
    
    json_file_content["name"] = "lwf"
    json_parser.write_to_json_file(json_file_content)


    # ============================ 测试 Json数据 ===========================
    
    json_data_from_file = """
    {
        "name":"lwy",
        "age":20,
        "is_student":false,
        "hobbies":["reading", "coding"],
        "address":null
    }
    """


    # ============================ 将 Json 文件中的配置读取为 Python 变量 ===========================

    print("============================ 普通测试 ===========================\n")

    python_data_from_json = json.loads(json_data_from_file)
    print(python_data_from_json)

    # 单独读取变量以键值对格式进行
    print(f" python_data_from_json[\"name\"]: {python_data_from_json["name"]}")


    # ============================ 将 Python 变量写为 Json 字符串 ===========================
    
    python_data_from_json["name"] = "lwf"
    json_data_from_python = json.dumps(python_data_from_json, ensure_ascii = False, indent = 4)
    print(json_data_from_python)
    