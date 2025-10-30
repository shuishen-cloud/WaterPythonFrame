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

from WaterFrameWork.core.Logger import WLogger
from WaterFrameWork.core.JsonParser import WJsonParser
from WaterFrameWork.core.Exception import handle_error, WException

def error_handle_func(log):
    log.info("这是来自 error_handle func 的异常处理")

@handle_error(default_error_return = False, error_handle = error_handle_func, 
              logger_info = "test_exception 函数捕获到异常")
def test_exception(log):
    raise WException("test_exception 的异常为 A")

if __name__ == "__main__":
    print("main entry start...\n")

    main_logger = WLogger()
    main_logger = main_logger.get_defualt_logger()

    main_logger.info("主函数日志 info 测试")
    main_logger.warning("主函数日志 warning 测试")

    json_parser = WJsonParser()
    json_content = json_parser.load_from_json_file("config.json")   # * 项目配置

    main_logger.info(f"配置读取成功，配置项为 {json_content}")

    json_content["platform"] = "wsl2"
    json_parser.write_to_json_file(json_content)
    main_logger.info(f"写入配置")

    test_exception(main_logger)