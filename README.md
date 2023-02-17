# happy-python

Happy-Python是一个简单易用的Python库，让编程轻松愉快

## 从 pip 安装

`pip install happy-python`

## 单元测试

基于 `test` 文件夹中的 `\\__init__.py` -> `load_tests` 自动发现：

`python -m unittest tests`

## 使用方法

### 使用

比如：

`from happy_python import HappyLog`

## 本地打包安装

### 打包

安装依赖包：

`pip install -U setuptools wheel`

运行：

`python setup.py bdist_wheel`

在 `dist` 目录下会生成类似 `happy_python-0.2.6-py3-none-any.whl` 的安装包。


### 本地安装

全局安装：
     
`pip install -U happy_python-0.2.6-py3-none-any.whl`
 
用户目录安装：
    
`pip install --user -U happy_python-0.2.6-py3-none-any.whl`

### 卸载

`pip uninstall happy-python`
