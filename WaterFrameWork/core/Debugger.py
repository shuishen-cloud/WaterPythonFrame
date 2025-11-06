'''
Filename:  Debugger.py
Project:   core
Author:    lwy
***
Created:   2025/11/04 Tuesday 16:12:49
Modified:  2025/11/04 Tuesday 16:12:52
***
Description: 
'''


import pexpect
import re

def gdb_expect_sendline(gdb : pexpect.spawn, expect = r"\(gdb\)", sendline = None, timout = 5):
    """
    gdb 读取循环，还需要一个 timeout 来等待命令执行（尤其是等待断点，因为程序在遇到断点之前可能会执行一段时间）

    ? bug: expect() 和 sendline() 到底哪个靠前呢？
    TODO 函数头类型检查不完善
    """
    
    gdb.sendline(sendline)
    gdb.expect(expect, timeout = timout)

def get_gdb_output(gdb : pexpect.spawn) -> str:
    """
    pexpect 捕获 gdb 的输出

    ! decode 检索不到，可能是 before 的问题
    """

    return gdb.before.decode("utf-8").strip()

class Debugger():
    """
    gdb 的容器，用来封装 pexpect 和 gdb 的交互，装载进入 Flask

    * 这里的重点是 GDB 的
    """
    def __init__(self):
        # TODO 路径需要修改，从 json/前端 获取
        exe_path = "/home/lwy/project/WaterPythonFrameWork/tests/test_program"
        
        gdb = pexpect.spawn(f"gdb -q {exe_path}")  # ! 静默 GDB

        # gdb.sendline("y")
        gdb.sendline("set style enabled off");  # ! 关闭  gdb 色彩输出
        gdb.expect(r"\(gdb\)")

        gdb.expect(r"\(gdb\)")
        
        gdb.sendline("b main")
        print(get_gdb_output(gdb))
        # gdb.sendline("y")
        print(get_gdb_output(gdb))
        gdb.expect(r"\(gdb\)")

        gdb.sendline("run")
        print(get_gdb_output(gdb))
        # gdb.expect(r"\(session\)", timeout = 3)
        
        gdb.sendline("y")
        gdb.expect(r"Breakpoint")

        # ? 为什么最关键的一步总是出错呢？
        gdb.expect(r"\(gdb\)")
        gdb.sendline("info locals")
        
        print(get_gdb_output(gdb))

        gdb.expect(r"\(gdb\)")
        
        # * 获取的 info locals 进行处理，使之没有违法字符。
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        self.viriables = get_gdb_output(gdb)
        self.viriables = ansi_escape.sub('',self.viriables )
        self.viriables = self.viriables.replace('\r', '').split("\n")
        
        print(f"变量列表：{self.viriables}") 
    
    def get_debugger_info(self):
        return self.viriables

if __name__ == "__main__":
    debugger = Debugger()