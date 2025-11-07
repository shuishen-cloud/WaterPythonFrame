# 此项目后端开发

## Module : Debugger

### Class : GdbCommand():

    将会用到的 GDB 的命令封装成为类，易读，也更容易控制。

### Class : Debugger()
    
    gdb 的容器，用来封装 pexpect 和 gdb 的交互，装载进入 Flask。


#### Viriables

- **核心变量**（*维护类正常运行*）

```Python
self.exe_path = "/home/lwy/project/WaterPythonFrameWork/tests/test_program2"
self.gdb = pexpect.spawn(f"gdb -q {self.exe_path}")
```

#### Method 

```Python
def __init__(self)
```

***

```Python
def gdb_expect_sendline(self, sendline = "n", expect = r"\(gdb\)", timeout = 3)
```

    进行一次完整的 pexpect 输入输出，并且将缓冲区提取出来

***

```Python
def get_gdb_output(self) -> str:
```
    pexpect 捕获 gdb 的输出

***

```Python
def process_gdb_output(self, gdb_output):
```
    处理命令行输出的 Gdb 回显，按行解析为列表，需要显式地写出获得的字符串

***

```python
def _test_gdb(self):
```    
    完成危险初始化之后对于 gdb 的检测

