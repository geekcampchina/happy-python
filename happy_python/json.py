#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def dict_to_pretty_json(data: dict, indent=4, sort_keys=True, ensure_ascii=False):
    """
    字典转换为JSON字符串
    :param data: 字典
    :param indent: 缩进
    :param sort_keys: 排序
    :param ensure_ascii: 中文显示
    :return:
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
