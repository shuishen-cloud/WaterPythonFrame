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
import WaterFrameWork.core.Logger as Logger
import WaterFrameWork.core.JsonParser

if __name__ == "__main__":
    print("main entry start...\n")

    main_logger = Logger.WLogger()
    main_logger = main_logger.get_defualt_logger()

    main_logger.info("主函数日志 info 测试")
    main_logger.warning("主函数日志 warning 测试")