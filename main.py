'''
Filename:  main.py
Project:   WaterPythonFrameWork
Author:    lwy
***
Created:   2025/10/29 Wednesday 19:42:35
Modified:  2025/10/29 Wednesday 19:44:14
***
Description: the main entry of project
'''

import WaterFrameWork.core.Exception
from WaterFrameWork.core.Logger import WLogger
from WaterFrameWork.core.JsonParser import JsonParser

if __name__ == "__main__":
    print("main entry start...\n")

    main_logger = WLogger()
    main_logger = main_logger.get_defualt_logger()

    main_logger.info("主函数日志 info 测试")
    main_logger.warning("主函数日志 warning 测试")

    json_parser = JsonParser()
    json_content = json_parser.load_from_json_file("config.json")   # * 项目配置

    main_logger.info(f"配置读取成功，配置项为 {json_content}")

    json_content["platform"] = "wsl2"
    json_parser.write_to_json_file(json_content)
    main_logger.info(f"写入配置")