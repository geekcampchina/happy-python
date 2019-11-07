#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
消息摘要算法相关代码
"""

import hashlib


def gen_md5_32_hexdigest(s):
    """
    # 获取字符串的MD5值
    :param s:
    :return:
    """

    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def gen_sha1_hexdigest(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def gen_sha512_hexdigest(s):
    return hashlib.sha512(s.encode('utf-8')).hexdigest()
