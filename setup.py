# -*- coding: utf-8 -*-
"""
    setup
    ~~~~
    Happy-Python 是一个简单易用的 Python 库，让写代码成为一件轻松、愉快的事情。
    :copyright: (c) 2018 by Chengdu Geek Camp.
    :license: MIT, see LICENSE for more details.
"""

from setuptools import setup
from os.path import join, dirname
from happy_python.version import __version__

with open(join(dirname(__file__), 'happy_python/version.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

with open(join(dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    pkgs = f.read()
    print('pkgs', pkgs)
    install_requires = pkgs.split("\n")

setup(
    name='Happy-Python',
    version=__version__,
    url='https://github.com/geekcampchina/happy-python',
    license='GPL',
    author='Chengdu Geek Camp',
    author_email='info@cdgeekcamp.com',
    description="一个简单易用的 Python 库，让写代码成为一件轻松、愉快的事情。",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=['happy_python'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
