'''
Filename:  Logger.py
Project:   core
Author:    lwy
***
Created:   2025/10/28 Tuesday 17:09:09
Modified:  2025/10/28 Tuesday 17:18:15
***
Description: 
'''

import logging

class WLogger():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.console_handler = None
        self.file_handler = None
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s")

    def setConsoleHandler(self):
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)

    def setFileHandler(self):
        self.file_handler = logging.FileHandler("WLogger.log", mode = "w")
        self.file_handler.setLevel(logging.INFO)

    def setFommartterForHandler(self):
        if self.console_handler != None:
            self.console_handler.setFormatter(self.formatter)
        
        if self.file_handler != None:
            self.file_handler.setFormatter(self.formatter)

    def get_defualt_logger(self) -> logging.Logger:
        """
        获得默认日志器，无文件输出
        """
        self.setConsoleHandler()
        self.setFommartterForHandler()
        self.logger.addHandler(self.console_handler)

        return self.logger
    
    def get_file_logger(self) -> logging.Logger:
        self.setFileHandler()
        self.get_defualt_logger()
        self.logger.addHandler(self.file_handler)

        return self.logger

if __name__ == "__main__":
    """
    ? 我也没看到写入文件的逻辑呀——原来是在 logging.basicConfig()
    
    我在想一个封装和暴露的问题，到底要不要暴露出一些参数呢？
    
    ! 印象里边这个库实例之间貌似会有冲突，这个时候就彰显出代码的可扩展性。
    
    * basicConfig 可写可不写，写了则会创建一个默认的日志处理器
    """
    
    # ============================ 日志库面向对象测试 ===========================

    print("\n")
    class_logger = WLogger()
    # ? 这里是不是有些奇怪?算是动态语言的一个特色
    class_logger = class_logger.get_file_logger()
    class_logger.warning("这是来自 class info 的输出")

    # ============================ 设置日志器格式 ===========================

    # logging.basicConfig(
    #     level = logging.DEBUG,
    #     format='%(asctime)s - %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    #     datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期格式
    #     filename='example.log',  # 日志文件名
    #     filemode='w'
    # ) 

    # ============================ 创建日志器实例 ===========================
    
    logger = logging.getLogger(__name__ )

    # 创建控制台处理
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)    

    # 创建格式化器
    # ? 逆天时刻，为什么还要再配置一次 Formmatter ?
    formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # 将我的 日志控制台处理器 添加到 日志记录器中
    # ? 还有逆天时刻
    logger.addHandler(console_handler)

    # 测试
    logger.debug('这是一个调试信息')
    logger.info('这是一个普通信息')
    logger.warning('这是一个警告信息')
    logger.error('这是一个错误信息')
    logger.critical('这是一个严重错误信息')