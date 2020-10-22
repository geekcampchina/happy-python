#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件（INI）转换类
"""

import os
from abc import ABCMeta

from happy_python import HappyPyException


class HappyConfigBase(object, metaclass=ABCMeta):
    _section = 'main'

    def __init__(self):
        pass

    @property
    def section(self):
        """
        使用 property + setter 注解防止用户指定无效值
        :return:
        """
        return self._section

    @section.setter
    def section(self, value):
        if value:
            self._section = value
        else:
            raise ValueError("指定的 section 属性值无效。")


class HappyConfigParser(object):
    @staticmethod
    def load(filename: str, happy_config_object: HappyConfigBase):
        if not isinstance(happy_config_object, HappyConfigBase):
            raise HappyPyException('happy_config_object 不是 HappyConfigBase 类的子类对象。')

        try:
            if not os.path.exists(filename):
                print("[Error] 配置文件 %s 不存在" % filename)
                exit(1)

            with open(filename, 'r', encoding='UTF-8') as f:
                content = f.readlines()
                HappyConfigParser._loads(''.join(content), happy_config_object)
        except Exception as e:
            print("[Error] 配置文件读取错误：%s" % str(e))
            exit(1)

    @staticmethod
    def _loads(content: str, happy_config_object: HappyConfigBase):
        from configparser import ConfigParser

        if not isinstance(happy_config_object, HappyConfigBase):
            raise HappyPyException('happy_config_object 不是 HappyConfigBase 类的子类对象。')

        try:
            cfg = ConfigParser()
            cfg.read_string(content)

            class_attrs = happy_config_object.__dict__
            section = happy_config_object.section

            for name, value in class_attrs.items():
                if name == '_section':
                    continue

                t = type(value)

                if t is str:
                    v = cfg.get(section, name)
                    exec("happy_config_object.%s='%s'" % (name, v))
                elif t is int:
                    v = cfg.getint(section, name)
                    exec("happy_config_object.%s=%d" % (name, v))
                elif t is bool:
                    v = cfg.getboolean(section, name)
                    exec("happy_config_object.%s=%s" % (name, v))
                elif t is float:
                    v = cfg.getfloat(section, name)
                    exec("happy_config_object.%s=%f" % (name, v))
                elif t is list:
                    v = cfg.get(section, name).split(',')
                    exec("happy_config_object.%s=%s" % (name, v))
                else:
                    v = cfg.getboolean(section, name)
                    exec("happy_config_object.%s=%s" % (name, v))
        except Exception as e:
            print("[Error] 配置文件读取错误：%s" % str(e))
            exit(1)

    @staticmethod
    def load_with_var(filename: str, var_dict: dict, happy_config_object: HappyConfigBase):
        try:
            if not os.path.exists(filename):
                print("[Error] 配置文件 %s 不存在" % filename)
                exit(1)

            with open(filename, 'r', encoding='UTF-8') as f:
                content = ''.join(f.readlines())

                for var, value in var_dict.items():
                    content = content.replace('${%s}' % var, value)

                HappyConfigParser._loads(content, happy_config_object)
        except Exception as e:
            print("[Error] 配置文件读取错误：%s" % str(e))
            exit(1)
