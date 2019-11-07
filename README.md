# happy-python

Happy-Python 是一个简单易用的 Python 库，让写代码成为一件轻松、愉快的事情。

## 从 pip 安装

    pip install happy-python

## 单元测试

`python -m unittest tests`

    基于 `test` 文件夹中的 `\\__init__.py` -> `load_tests` 自动发现。


## 使用方法

### 使用

    from happy_python import HappyLog

## 本地打包安装

### 打包

安装依赖包 `pip install -U setuptools wheel`。

运行 `python setup.py bdist_wheel`，在 `dist` 目录下会生成类似 `Happy_Python-0.0.4-py3-none-any.whl` 的安装包。


### 本地安装

全局环境::
    `pip install -U Happy_Python-0.0.4-py3-none-any.whl`

用户环境::
    `pip install --user -U Happy_Python-0.0.4-py3-none-any.whl`

### 卸载

`pip uninstall Happy-Python`