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
    packages=find_packages(),   # ! 这行十分危险
)
