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

if __name__ == "__main__":

    # TODO 路径需要修改，从 json/前端 获取
    exe_path = "../../tests/test"
    
    gdb = pexpect.spawn(f"gdb {exe_path}")  # ! 怎么会没加载成功呢？
    
    # 0.1 infod 设置
    gdb.sendline("y")
    
    # ! 这里在 ~/.gdbinit 中设置了 set debuginfod enabled off，禁止下载 debuginfod，减少检索失败的次数
    # gdb.sendline(f"file {exe_path}")
    gdb.expect(r"\(gdb\)")

    # 1. 运行之前的工作 —— 设置断点为 21
    gdb_expect_sendline(gdb, sendline = "break main")

    # * 2. 开始调试代码
    # gdb_expect_sendline(gdb, sendline = "run") # 这个需要额外的逻辑来处理
    gdb.sendline("run")
    gdb.sendline("y")

    # ! 这里还会有一个  `file` 捕获不到
    gdb.sendline("y")

    # ? 这里需不需要捕获 breakpoints 输出？

    gdb_expect_sendline(gdb, sendline = "locals info")
    print(get_gdb_output(gdb))