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

if __name__ == "__main__":
    """
    ? 命令行解析模块的关键在于将命令行解析和相对应的代码块对应起来，采用回调函数还是高阶函数？

    还有能够迅速地生成命令行，在一个模块下的 main 演示示例中
    """

    argsPaser = argparse.ArgumentParser(description="这是一个命令行程序，来展示命令行解析")
    
    # 必选参数：
    argsPaser.add_argument("input_file", type = str, help = "文件路径")

    # 可选参数
    argsPaser.add_argument("--verseble", type = bool, help = "命令执行回显是否可见")
    
    # * 解析命令行参数
    args = argsPaser.parse_args()

    input_file = args.input_file

    print(f"这是命令行解析的结果：{input_file}")