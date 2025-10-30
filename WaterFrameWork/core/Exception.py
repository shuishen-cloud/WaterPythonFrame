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

from functools import wraps   # ? 我记得还有一种使用 functools 来实现装饰器
from typing import Optional

class WException(Exception):
    """
    此框架的自定义异常
    """
    def __init__(self, message):
        """
        Args:
            message: 异常显示的消息
        """
        super().__init__(message)

def handle_error(default_error_return = False, error_handle = None, logger_info : Optional[str] = None):
    """
    异常处理装饰器，通过三层函数调用，来实现异常捕获，支持异常回调函数
    
    Args:
        default_error_return(bool): 默认返回值：如果发生异常，则返回假
    """

    def decorator(func):
        @wraps(func)  # 保留原函数信息
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e: 
                log = args[0] if args else None  # 从位置参数中取 log               
                log.info(f"decorator: 函数 {func.__name__} 发生异常：{e}")
                
                if error_handle:
                    error_handle(log)

                return default_error_return
        return wrapper
    return decorator

if __name__ == "__main__":
    """
    TODO 将异常处理装饰器设计为类
    """

    # ============================ 测试用例代码 ===========================

    def test_func_callback():
        """
        装饰器异常处理的回调函数
        """
        print(f"test_func_callback: 唤醒异常处理回调函数")

    @handle_error(error_handle = test_func_callback, logger_info = "looger-info-args: 这是异常装饰器的异常")
    def test_func():
        """"
        用于测试异常装饰器的测试函数
        """
        raise WException("raise WaterException: 装饰器异常测试触发")


    # ============================ 异常测试部分 ===========================

    try:
        print("test from exception.")
        
        # 测试装饰器的函数
        test_func()
        
        # 测试自建异常
        raise WException("WaterException 异常发生")
    except WException as e:
        print(f"捕获了 WaterException 异常，异常消息是 {e}")
    finally:
        print("最终执行逻辑")
