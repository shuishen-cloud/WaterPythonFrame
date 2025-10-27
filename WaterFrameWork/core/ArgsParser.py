'''
Filename:  ArgsParser.py
Project:   core
Author:    lwy
***
Created:   2025/10/26 Sunday 18:35:14
Modified:  2025/10/26 Sunday 18:35:48
***
Description: 
'''

import argparse
import sys
from typing import List, Any

class Arg():
    def __init__(self, args_name : str, type : argparse.Action):
        self.arg_name = args_name
        self.type = type

    def unwrapped(self) -> List[str]:
        return (self.arg_name, self.type)

class CommandArgsParser():
    def __init__(self, description="这是一个命令行程序，来展示命令行解析"):
        self.args_paser = argparse.ArgumentParser(description = description)
        self.args = self.args_paser.parse_args()

        self.command_list : List[Arg] = [ ]  # 将需要支持的命令以自建类型 Arg 组成的 List[] 收集
        self.viriable_list : List[Any] = [ ] # 将从 command_list 中迭代读取到的 Arg 解包，获取其中的变量
    
    def argsParser(self, arg_list : List[Arg]):
        for arg in arg_list:
            self.command_list.append(arg)

    def argsParserToVarible(self):
        for arg in self.command_list:
            self.viriable_list.append(arg.unwrapped())

    def test_ArgsParser(self):
            args_dict = vars(self.args)  # * 转换为字典：{参数名: 参数值, ...}
            for arg_name, arg_value in args_dict.items():
                print(f"参数名: {arg_name}, 参数值: {arg_value}")

if __name__ == "__main__":
    """
    ? 命令行解析模块的关键在于将命令行解析和相对应的代码块对应起来，采用回调函数还是高阶函数？
    ? 可否将所有添加的命令都添加进入一个列表？再进行维护？颇为艰辛。

    # ! 最重要的问题是，如何将参数解析获得的值安全地放到类内变量里。
    
    还有能够迅速地生成命令行，在一个模块下的 main 演示示例中

    * 因为这个解析库最初的设想是为了 Vscode 的 tasks.json 测试方便（命令行测试）而作为一个工具，
    * 所以没必要支持那么多参数选项，最后成为一次性读取，检测多个命令行参数，也即实现一个迭代器。

    使用这个库还得引入 Arg 类？
    """

    # ============================ OO 式命令行参数读取 ===========================
    
    # 构建命令行参数
    args_list = [
        Arg("--input", type=str),
        Arg("--output", type=str)
    ]

    command_parser = CommandArgsParser()
    command_parser.argsParser(args_list)
    command_parser.argsParserToVarible()
    command_parser.test_ArgsParser()

    # # ============================ 设置命令行参数解析程序 ===========================

    # argsPaser = argparse.ArgumentParser(description="这是一个命令行程序，来展示命令行解析")
    
    # # 必选参数：
    # argsPaser.add_argument("input_file", type = str, help = "文件路径")

    # # 可选参数
    # argsPaser.add_argument("--verseble", type = bool, help = "命令执行回显是否可见")
    

    # # ============================ 解析获取命令行参数 ===========================

    # args = argsPaser.parse_args()

    # input_file = args.input_file

    # print(f"这是命令行解析的结果：{input_file}")