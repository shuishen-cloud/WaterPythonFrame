"""
为了包的引用

- 首先，写好 setup.py
- 再将项目
    - # 在项目根目录下执行
        pip install -e .  # -e 表示 editable 模式，代码修改后无需重新安装
"""

from setuptools import setup, find_packages

setup(
    name="WaterFrameWork",
    version="0.1.0",
    packages=find_packages(where="WaterPythonFrameWork"),   # ? 这个是查找所有包吗？我想还是不要检索 tests 里的包为好

    # packages=find_packages(where="src"),  # 查找 src 下的所有包
    # package_dir={"": "src"},  # 指定包的根目录为 src
)
