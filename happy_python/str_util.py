#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import string
import random


def bytes_to_str(b: bytes, encoding='UTF-8'):
    return str(b, encoding=encoding)


def bytearray_to_str(b: bytearray, encoding='UTF-8'):
    return str(b, encoding=encoding)


def str_to_dict(value: str):
    return json.loads(value)


def dict_to_str(value: dict, indent=None):
    return json.dumps(value, ensure_ascii=False, indent=indent)


def gen_random_str(str_len: int = 10) -> str:
    """
    生成随机字符串，默认长度10
    :param str_len:
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=str_len))


def to_hex_str(s: str) -> str:
    """
    将字符串转换为十六进制表示的字符串
    :param s:
    :return:
    """
    return s.encode('utf-8').hex()


def is_ascii_str(s):
    """
    判断是否是ASCII字符串
    :param s:
    :return:
    """
    return all(ord(c) < 128 for c in s)
