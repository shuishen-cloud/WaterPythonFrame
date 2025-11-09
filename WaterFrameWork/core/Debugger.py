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
import asyncio
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
    viriables = "info locals"

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
        self.currunt_line = None

        # TODO 代码内容可能来自前端，前端需要先将代码 POST 到后端，后端建立临时文件
        self.exe_path = "/home/lwy/project/WaterPythonFrameWork/tests/test_program2"
        
        self.gdb = pexpect.spawn(f"gdb -q {self.exe_path}")  # ! -q 以静默模式启动 gdb
        self.gdb.sendline("set style enabled off");  # ! 关闭  gdb 色彩输出

        # ! 此后的代码具有相当强的不确定性，需要增强健壮性
        gdb = self.gdb

        # gdb.sendline("y")
        gdb.expect(r"\(gdb\)", timeout = 3)

        gdb.expect(r"\(gdb\)", timeout = 3)
        
        print("* 在主函数处打断点 b main")
        gdb.sendline("b main")
        print(self.get_gdb_output())
        # .sendline("y")
        gdb.expect(r"\(gdb\)", timeout = 3)
        
        print("* 开始运行 run")
        gdb.sendline("run")
        print(self.get_gdb_output())
        # gdb.expect(r"\(session\)", timeout = 3)
        
        gdb.expect(r"Breakpoint", timeout = 3)

        print("* 获取变量值 info locals")
        # ? 为什么最关键的一步总是出错呢？
        gdb.expect(r"\(gdb\)", timeout = 3)
        gdb.sendline("info locals")
        
        print(self.get_gdb_output())

        gdb.expect(r"\(gdb\)", timeout = 3)
        
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
    
    def get_currunt_line(self, n_command_content):
        """
        获取当前正在调试的代码行数，通过 n 或者 s 命令的回显，否则无效

        ! 在使用时要注意传入的参数是否真的是代码内容
        """
        
        get_line_num = re.match(r"^\d+", n_command_content) # 只匹配行首的数字
        
        return get_line_num.group()

    def step(self):
        """
        执行后端 GDB 的中 step 命令，更新类内维护的变量列表和栈帧调用列表，需要前端来调用
        """
        # * 执行 GDB 的 step 命令，并消费此次缓冲
        self.gdb_expect_sendline(GdbCommand.step);
        next_content = self.get_gdb_output()
        
        # * 更新 viribales
        self.gdb_expect_sendline(GdbCommand.viriables)
        next_content = self.get_gdb_output()
        self.viriables = self.process_gdb_output(next_content)

        # * 更新栈帧
        self.gdb_expect_sendline(GdbCommand.stacktrace)
        next_content = self.get_gdb_output()
        self.stacktrace = self.process_gdb_output(next_content)

    # ! 这两个异步方法没能成功
    async def get_front_breaklists(self):
        """
        获取前端传来的断点，并将其设置
        """
        print("异步代码开始执行")
        asyncio.create_task(self.read_front_breaklists())  # 前端列表传来断点的时间不确定，所以要使用异步函数
    
    async def read_front_breaklists(self):
        while(True):
            if self.breakpoints != None and self.breakpoints:
                print(f"异步函数执行")
                for each_breakpoint in self.breakpoints:
                    print(each_breakpoint)
            await asyncio.sleep(0.1)

    def _test_gdb(self):
        """
        完成危险初始化之后对于 gdb 的检测
        
        * 内部采用了枚举的试验方法
        """

        # * 获取的 info locals 进行处理，使之没有违法字符。
        self.viriables = self.process_gdb_output(self.get_gdb_output())
        print(f"* 变量列表：{self.viriables}\n")
        
        # asyncio.run(self.get_front_breaklists()) # ! 异步获取失败，不过似乎也没有更好的方法了

        # 对于我的代码而言，循环五次可以到一个函数调用，看到栈帧之间的切换
        for i in range(5):
            self.gdb_expect_sendline(GdbCommand.step)
            next_content = self.get_gdb_output()
            print(f"{next_content}")

            # * 获取代码行数
            processed_next_content = self.process_gdb_output(next_content)
            self.currunt_line = self.get_currunt_line(processed_next_content[-2])
            print(f"* 当前代码行数: {self.currunt_line}")   # *! 始终获取最后倒数第二个元素（是代码信息），倒数第一个是空值

        self.gdb_expect_sendline(GdbCommand.stacktrace)
        self.stacktrace = self.process_gdb_output(self.get_gdb_output())
        print(f"* 栈帧调用：{self.stacktrace}\n")

if __name__ == "__main__":
    debugger = Debugger()