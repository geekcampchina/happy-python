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


def to_hex_str_with_delimiter(s: str, delimiter: str) -> str:
    """
    将字符串转换为十六进制表示的字符串
    :param s:
    :param delimiter: 分隔符
    :return:
    """
    hex_str = s.encode('utf-8').hex()

    output = ''
    i = 0
    max_len = len(hex_str)

    while i < max_len:
        output += hex_str[i]

        length_postion = i + 1

        if length_postion % 2 == 0 and length_postion < max_len:
            output += delimiter

        i += 1

    return output


def from_hex_str(s: str, delimiter: str = '0x') -> bytes:
    """
    将十六进制表示的字符串转为bytes。比如 0x0E0x0A0x5D。
    :param s: 十六进制表示的字符串，可以带分隔符。比如 0E 0A
    :param delimiter: 分隔符
    :return:
    """

    _s = s

    # 删除分隔符
    if delimiter:
        _s = _s.replace(delimiter, '')

    return bytes.fromhex(_s)


def is_ascii_str(s):
    """
    判断是否是ASCII字符串
    :param s:
    :return:
    """
    return all(ord(c) < 128 for c in s)
