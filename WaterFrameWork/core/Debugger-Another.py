import pexpect
import re
import logging
from typing import Optional, Dict, Set, List

# 配置日志（方便调试交互过程）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pexpect_gdb")


class GDBDebugger:
    def __init__(self, exe_path: str, timeout: int = 10):
        """初始化调试器并加载目标程序"""
        self.exe_path = exe_path  # 可执行文件路径
        self.timeout = timeout    # 交互超时时间（秒）
        self.gdb = None           # pexpect 进程对象
        self.breakpoints: Set[int] = set()  # 已设置的断点行号
        self.current_line: Optional[int] = None  # 当前执行行
        self._init_gdb()

    def _init_gdb(self) -> None:
        """启动 gdb 并加载目标程序"""
        try:
            # 启动 gdb 进程
            self.gdb = pexpect.spawn(f"gdb {self.exe_path}", encoding="utf-8")
            self._expect_prompt()  # 等待初始提示符 (gdb)

            # 显式加载程序（确保符号表正确加载）
            self._send_command(f"file {self.exe_path}")
            logger.info(f"已加载程序: {self.exe_path}")
        except pexpect.TIMEOUT:
            raise RuntimeError("初始化 gdb 超时，请检查程序路径是否正确")
        except Exception as e:
            raise RuntimeError(f"初始化 gdb 失败: {str(e)}")

    def _send_command(self, cmd: str, expect_prompt: bool = True) -> str:
        """发送命令到 gdb 并返回输出（不含提示符）"""
        if not self.gdb:
            raise RuntimeError("gdb 未初始化，请先创建调试器实例")

        logger.debug(f"发送命令: {cmd}")
        self.gdb.sendline(cmd)

        if expect_prompt:
            # 等待 gdb 提示符，返回命令输出
            self._expect_prompt()
            output = self.gdb.before.strip()
            logger.debug(f"命令输出: {output}")
            return output
        return ""

    def _expect_prompt(self) -> None:
        """等待 gdb 提示符 (gdb)"""
        try:
            self.gdb.expect(r"\(gdb\) ", timeout=self.timeout)
        except pexpect.TIMEOUT:
            buffer = self.gdb.before.strip()
            raise RuntimeError(f"等待 gdb 提示符超时，缓冲区内容: {buffer}")

    def set_breakpoint(self, line: int) -> bool:
        """在指定行设置断点"""
        if line in self.breakpoints:
            logger.warning(f"行 {line} 已存在断点，无需重复设置")
            return True

        try:
            output = self._send_command(f"break {line}")
            # 处理断点挂起询问（共享库加载时）
            if "Make breakpoint pending on future shared library load?" in output:
                self._send_command("y")  # 确认挂起
                self.breakpoints.add(line)
                logger.info(f"已设置断点（挂起）: 行 {line}")
                return True
            # 验证断点是否设置成功
            if re.search(r"Breakpoint \d+ at 0x[0-9a-fA-F]+: file .*, line \d+", output):
                self.breakpoints.add(line)
                logger.info(f"已设置断点: 行 {line}")
                return True
            logger.error(f"设置断点失败: {output}")
            return False
        except Exception as e:
            logger.error(f"设置断点出错: {str(e)}")
            return False

    def remove_breakpoint(self, line: int) -> bool:
        """移除指定行的断点"""
        if line not in self.breakpoints:
            logger.warning(f"行 {line} 不存在断点，无需移除")
            return True

        try:
            output = self._send_command(f"delete {line}")
            if "No breakpoint number" not in output:
                self.breakpoints.remove(line)
                logger.info(f"已移除断点: 行 {line}")
                return True
            logger.error(f"移除断点失败: {output}")
            return False
        except Exception as e:
            logger.error(f"移除断点出错: {str(e)}")
            return False

    def start(self) -> bool:
        """启动程序执行（直到第一个断点）"""
        try:
            output = self._send_command("run", expect_prompt=False)
            # 等待断点命中
            self.gdb.expect(r"Breakpoint \d+, .* at .*:(\d+)", timeout=self.timeout)
            self.current_line = int(self.gdb.match.group(1))  # 提取当前行号
            self._expect_prompt()  # 回到提示符
            logger.info(f"程序启动，命中断点: 行 {self.current_line}")
            return True
        except pexpect.TIMEOUT:
            buffer = self.gdb.before.strip()
            logger.error(f"程序启动超时，缓冲区: {buffer}")
            return False
        except Exception as e:
            logger.error(f"启动程序出错: {str(e)}")
            return False

    def step(self) -> Optional[int]:
        """单步执行（进入函数）"""
        return self._execute_step_command("step")

    def next(self) -> Optional[int]:
        """单步执行（跳过函数）"""
        return self._execute_step_command("next")

    def _execute_step_command(self, cmd: str) -> Optional[int]:
        """执行单步命令（内部通用实现）"""
        try:
            self._send_command(cmd, expect_prompt=False)
            # 匹配行号（正常执行）或程序结束
            match = self.gdb.expect(
                [r"at .*:(\d+)", r"Program exited"],
                timeout=self.timeout
            )
            if match == 0:  # 正常执行到下一行
                self.current_line = int(self.gdb.match.group(1))
                self._expect_prompt()
                logger.info(f"单步执行后，当前行: {self.current_line}")
                return self.current_line
            else:  # 程序已退出
                self.current_line = None
                logger.info("程序已退出")
                return None
        except Exception as e:
            logger.error(f"单步执行出错: {str(e)}")
            return None

    def get_variable(self, var_name: str) -> Optional[Dict[str, str]]:
        """获取变量信息（值、地址）"""
        try:
            # 获取变量值和指向的地址（适用于指针）
            output = self._send_command(f"p {var_name}")
            # 解析输出（如: $1 = 0x7fffffffde40 "hello" 或 $2 = 10）
            value_match = re.search(r"= (.*)", output)
            if not value_match:
                logger.warning(f"未找到变量 {var_name} 的值")
                return None

            value = value_match.group(1).strip()
            # 获取变量自身的地址
            addr_output = self._send_command(f"p &{var_name}")
            addr_match = re.search(r"= (0x[0-9a-fA-F]+)", addr_output)
            addr = addr_match.group(1) if addr_match else "未知"

            return {
                "name": var_name,
                "value": value,
                "address": addr
            }
        except Exception as e:
            logger.error(f"获取变量 {var_name} 出错: {str(e)}")
            return None

    def inspect_memory(self, address: str, count: int = 4, format: str = "x") -> List[str]:
        """检查指定地址的内存（默认显示4个16进制值）"""
        # gdb x命令格式: x/数量格式单位，如 x/4xw 0x7fffffffde40
        try:
            output = self._send_command(f"x/{count}{format}w {address}")
            # 解析内存内容（如: 0x7fffffffde40: 0x0000000a 0x00000000 0x00400526 0x00000000）
            memory_lines = output.split("\n")
            result = []
            for line in memory_lines:
                if ":" in line:
                    result.extend(line.split(":")[1].strip().split())
            logger.info(f"内存检查结果（地址 {address}）: {result}")
            return result[:count]  # 返回指定数量的内存值
        except Exception as e:
            logger.error(f"检查内存 {address} 出错: {str(e)}")
            return []

    def quit(self) -> None:
        """退出 gdb 调试"""
        if self.gdb:
            self._send_command("quit", expect_prompt=False)
            self.gdb.wait()
            self.gdb = None
            logger.info("已退出 gdb 调试")


# 使用示例
if __name__ == "__main__":
    # 示例程序（test.cpp）需提前编译为 debug 模式: g++ -g test.cpp -o test
    # test.cpp 内容参考：
    # #include <iostream>
    # int main() {
    #     int a = 10;
    #     int* p = &a;
    #     std::cout << *p << std::endl; // 第4行
    #     return 0;
    # }
    debugger = GDBDebugger(exe_path="./test_program")

    try:
        # 设置断点（第4行）
        debugger.set_breakpoint(4)

        # 启动程序
        debugger.start()

        # 查看变量 a 和指针 p
        print("变量 a 信息:", debugger.get_variable("a"))
        print("指针 p 信息:", debugger.get_variable("p"))

        # 检查指针 p 指向的内存（即 a 的值）
        p_info = debugger.get_variable("p")
        if p_info:
            p_address = p_info["value"].split()[0]  # 提取指针指向的地址
            print(f"指针 p 指向的内存（{p_address}）:", debugger.inspect_memory(p_address))

        # 单步执行（next）
        next_line = debugger.next()
        print(f"单步执行后当前行: {next_line}")

    finally:
        # 退出调试
        debugger.quit()