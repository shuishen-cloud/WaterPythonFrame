# 框架使用文档

## Module - Logger

### Class - WLogger()

- 日志器。

```Python
# 使用方法
from WaterFrameWork.core.Logger import WLogger

main_logger = WLogger()
main_logger = main_logger.get_defualt_logger()

main_logger.info("主函数日志 info 测试")
main_logger.warning("主函数日志 warning 测试")
```

## Module - JsonParser

### Class - JsonParser()

- Json 解析器。

```python
# 使用方法
from WaterFrameWork.core.JsonParser import JsonParser

json_parser = JsonParser()
json_content = json_parser.load_from_json_file("config.json")

main_logger.info(f"配置读取成功，配置项为 {json_content}")

json_content["platform"] = "wsl2"
json_parser.write_to_json_file(json_content)
```

## Module - Exception

### Class - WException

- 框架自定义错误

```python
    raise WException("test_exception 的异常为 A")
```

### Method - handle_error

- 异常处理注解。支持简单的回调函数和日志输出。

```python
def error_handle_func(log):
    log.info("这是来自 error_handle func 的异常处理")

@handle_error(default_error_return = False, error_handle = error_handle_func, 
              logger_info = "test_exception 函数捕获到异常")
def test_exception(log):
    raise WException("test_exception 的异常为 A")

test_exception(main_logger)
```
