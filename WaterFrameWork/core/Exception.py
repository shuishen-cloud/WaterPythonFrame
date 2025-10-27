'''
Filename:  Exception.py
Project:   core
Author:    lwy
***
Created:   2025/10/27 Monday 21:02:58
Modified:  2025/10/27 Monday 21:03:20
***
Description: a core module of my framework
'''

import functools

class WaterException(Exception):
    """
    此框架的自定义异常
    """
    def __init__(self, message):
        """
        Args:
            message: 异常显示的消息
        """
        super().__init__(message)

if __name__ == "__main__":
    
    
    # ============================ 异常测试部分 ===========================

    try:
        print("test from exception.")
        raise WaterException("WaterException 异常发生")
    except WaterException as e:
        print(f"捕获了 WaterException 异常，异常消息是 {e}")
    finally:
        print("最终执行逻辑")
