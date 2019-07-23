#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import time


def get_current_datetime():
    """
    获取当前时间字符串，比如 '2018-09-03 13：36：02'
    :return: 时间字符串
    """

    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


def get_current_datetime2():
    """
    获取当前时间字符串，比如 '2018_09_03_13_36_02'
    :return: 时间字符串
    """

    now = datetime.now()
    return now.strftime('%Y_%m_%d_%H_%M_%S')


def get_current_timestamp():
    """
    获取当前时间戳
    :return:
    """

    return time.time()
