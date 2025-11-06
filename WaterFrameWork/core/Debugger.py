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
    exe_path = "/home/lwy/project/WaterPythonFrameWork/tests/test_program"
    
    gdb = pexpect.spawn(f"gdb -q {exe_path}")  # ! 静默 GDB

    # gdb.sendline("y")
    gdb.expect(r"\(gdb\)")
    
    gdb.sendline("b main")
    print(get_gdb_output(gdb))
    gdb.sendline("y")
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
    # print(get_gdb_output(gdb))
    viriables = get_gdb_output(gdb)
    print(f"变量列表：{viriables}") 