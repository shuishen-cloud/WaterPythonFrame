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


class JsonParser():
    def __init__(self):
        self.json_file = None
    
    def load_from_json_file(self, file_path : str):
        with open(file_path, 'r', encoding = "utf-8") as file:
            self.json_file_content = json.load(file)
        
        return self.json_file_content

    def write_to_json_file(self, file_path : str):
        json.dump(file_path)

    def read_viriable_from_json(self):
        pass

if __name__ == "__main__":
    """
    # TODO 使用 Python 语法读取变量没有自动补全，写起来不是很危险？
    
    * 这个遍历分为三种情况，有封装的价值

    """    
    
    # ============================ 面向对象测试 ===========================

    json_parser = JsonParser()
    json_file_content = json_parser.load_from_json_file("tests/test.json")
    print(f"{json_file_content}")

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


    # ============================ 将 Python 变量写为 Json 文件 ===========================
    
    python_data_from_json["name"] = "lwf"
    json_data_from_python = json.dumps(python_data_from_json, ensure_ascii = False, indent = 4)
    print(json_data_from_python)
    