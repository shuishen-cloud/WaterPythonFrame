'''
Filename:  Debugger.py
Project:   core
Author:    lwy
***
Created:   2025/11/04 Tuesday 16:12:49
Modified:  2025/11/04 Tuesday 16:12:52
***
Description: 
TODO 将大部分的命令使用 GdbCommand 来标准化，最后直接限定参数为 GdbCommand
'''

import pexpect
import re

class GdbCommand():
    """    
    将会用到的 GDB 的命令封装成为类，易读，也更容易控制
    """
    gdb = r"\(gdb\)"
    run = "run"
    breakpoint = "b"
    next = "n"
    stacktrace = "bt"
    step = "s"
    yes = "y"

class Debugger():
    """
    gdb 的容器，用来封装 pexpect 和 gdb 的交互，装载进入 Flask
    """

    def __init__(self):
        """
        TODO 将 expect 的参数写成一个列表，并对返回结果进行解析，增强健壮性

        ! 这一段代码初始化 GDB 调试 的代码相当不稳定，解决方法之一在 TODO 
        """
        
        self.breakpoints = None
        self.viriables = None
        self.stacktrace = None

        # TODO 代码内容可能来自前端，前端需要先将代码 POST 到后端，后端建立临时文件
        self.exe_path = "/home/lwy/project/WaterPythonFrameWork/tests/test_program2"
        
        self.gdb = pexpect.spawn(f"gdb -q {self.exe_path}")  # ! -q 以静默模式启动 gdb
        self.gdb.sendline("set style enabled off");  # ! 关闭  gdb 色彩输出

        # ! 此后的代码具有相当强的不确定性，需要增强健壮性
        gdb = self.gdb

        # gdb.sendline("y")
        gdb.expect(r"\(gdb\)")

        gdb.expect(r"\(gdb\)")
        
        gdb.sendline("b main")
        print(self.get_gdb_output())
        # .sendline("y")
        gdb.expect(r"\(gdb\)")

        gdb.sendline("run")
        print(self.get_gdb_output())
        # gdb.expect(r"\(session\)", timeout = 3)
        
        gdb.sendline("y")
        gdb.expect(r"Breakpoint")

        # ? 为什么最关键的一步总是出错呢？
        gdb.expect(r"\(gdb\)")
        gdb.sendline("info locals")
        
        print(self.get_gdb_output())

        gdb.expect(r"\(gdb\)")
        
        # ! 此后部分脱离危险性，启动测试代码
        self._test_gdb()

    def gdb_expect_sendline(self, sendline = "n", expect = r"\(gdb\)", timeout = 3):
        """
        进行一次完整的 pexpect 输入输出，并且将缓冲区提取出来

        TODO expect 需要处理列表，需要将 expect 再进行封装一次

        * 此方法的核心在于 sendline 和 expect 还有 before 搭配在一起似乎能刷新 pexpect 的缓冲区

        ! 一次循环之后不管是否要输出到控制台，但是缓冲一定要清空，不过要不要维护一个 Debugger 类内输出的队列呢？
        """

        self.gdb.sendline(sendline)
        self.gdb.expect(expect)
        
        return self.get_gdb_output()

    def get_gdb_output(self) -> str:
        """
        pexpect 捕获 gdb 的输出

        ! decode 检索不到，可能是 before 的问题
        """

        return self.gdb.before.decode("utf-8").strip()
    
    def process_gdb_output(self, gdb_output):
        """
        处理命令行输出的 Gdb 回显，按行解析为列表，需要显式地写出获得的字符串

        ? 要不要在这里将字符串处理成 JSON 呢？
        """

        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        
        processed_gdb_output = ansi_escape.sub('',gdb_output)   # 删除其中的控 ASCII 控制字符
        processed_gdb_output =  processed_gdb_output.replace('\r', '').split("\n")  # TODO 这里还需要将列表中的空格去除

        return processed_gdb_output
    
    def _test_gdb(self):
        """
        完成危险初始化之后对于 gdb 的检测
        
        * 内部采用了枚举的试验方法
        """

        # * 获取的 info locals 进行处理，使之没有违法字符。
        self.viriables = self.process_gdb_output(self.get_gdb_output())
        print(f"* 变量列表：{self.viriables}\n")

        # 对于我的代码而言，循环五次可以到一个函数调用，看到栈帧之间的切换
        for i in range(5):
            self.gdb_expect_sendline(GdbCommand.step)
            print(f"{self.get_gdb_output()}")

        self.gdb_expect_sendline(GdbCommand.stacktrace)
        self.stacktrace = self.process_gdb_output(self.get_gdb_output())
        print(f"* 栈帧调用：{self.stacktrace}\n")

if __name__ == "__main__":
    debugger = Debugger()