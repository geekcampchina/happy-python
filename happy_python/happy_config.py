"""
配置文件（INI）转换类
"""

import os
from abc import ABCMeta
from dataclasses import dataclass

from typing import List

from happy_python import HappyPyException


@dataclass
class HappyConfigXListNode:
    prefix: str
    keys: List[str]


@dataclass
class HappyConfigXList:
    section: str
    node: HappyConfigXListNode


class HappyConfigBase(object, metaclass=ABCMeta):
    _section = 'main'
    _xlist: List[HappyConfigXList] = []

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

    def xlist_add(self, prefix: str, key: str, section: str = ''):
        __section = self._section if section == '' else section
        _key = '%s.%s' % (prefix, key)

        if len(self._xlist) == 0:
            self._xlist.append(HappyConfigXList(section=__section,
                                                node=HappyConfigXListNode(prefix=prefix,
                                                                          keys=[_key])))
        else:
            for xlist in self._xlist:
                if xlist.section == __section and xlist.node.prefix == prefix:
                    if _key not in xlist.node.keys:
                        xlist.node.keys.append(_key)

    def xlist_key(self, prefix: str, section: str = '') -> List[str]:
        __section = self._section if section == '' else section

        for xlist in self._xlist:
            if xlist.section == __section and xlist.node.prefix == prefix:
                return xlist.node.keys

        return []

    def xlist_get(self, prefix: str, key: str = ''):
        key = prefix + ('.' + key if key else '')

        return self.__dict__[key] if key in self.__dict__ else None


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
                content = f.read()
                HappyConfigParser._loads(content, happy_config_object)
        except Exception as e:
            print("[Error] 配置文件读取错误：%s" % str(e))
            exit(1)

    @staticmethod
    def _loads(content: str, happy_config_object: HappyConfigBase):
        def set_attr(t, _name, _new_name):
            if t is str:
                v = cfg.get(section, _name)
            elif t is int:
                v = cfg.getint(section, _name)
            elif t is bool:
                v = cfg.getboolean(section, _name)
            elif t is float:
                v = cfg.getfloat(section, _name)
            elif t is list:
                v = cfg.get(section, _name).split(',')
            else:
                v = cfg.getboolean(section, _name)

            setattr(happy_config_object, _new_name, v)

        from configparser import RawConfigParser

        if not isinstance(happy_config_object, HappyConfigBase):
            raise HappyPyException('happy_config_object 不是 HappyConfigBase 类的子类对象。')

        try:
            cfg = RawConfigParser()
            cfg.read_string(content)

            class_attrs = happy_config_object.__dict__
            section = happy_config_object.section

            for name, value in class_attrs.items():
                if name == '_section':
                    continue
                set_attr(type(value), name, name)
            for section, section_obj in cfg.items():
                if section == '_section':
                    continue

                for name, value in section_obj.items():
                    if not name.startswith('!'):
                        continue

                    new_name = name[1:]
                    parts = new_name.split('.')

                    if len(parts) >= 2:
                        happy_config_object.xlist_add(section=section, prefix=parts[0], key=parts[1])
                        set_attr(type(value), name, new_name)
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
