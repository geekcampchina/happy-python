#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime


def str_to_datetime(date_string: str, format_string: str = '%Y-%m-%d %H:%M:%S'):
    """
    将时间字符串转换为datetime对象
    :param date_string: 时间字符串，如2018-08-27 02:09:34
    :param format_string: 格式化字符串
    :return:
    """

    return datetime.strptime(date_string, format_string)


def datetime_to_str(datetime_obj: datetime, format_string: str = '%Y-%m-%d %H:%M:%S'):
    """
    将datetime对象转换为指定格式的字符串
    :param datetime_obj: 时间对象
    :param format_string: 格式化字符串
    :return:
    """

    return datetime_obj.strftime(format_string)


def get_current_datetime():
    """
    获取当前时间字符串，比如 '2018-09-03 13：36：02'
    :return: 时间字符串
    """

    now = datetime.now()
    return datetime_to_str(now)


def get_current_datetime2():
    """
    获取当前时间字符串，比如 '2018_09_03_13_36_02'
    :return: 时间字符串
    """

    now = datetime.now()
    return datetime_to_str(now, '%Y_%m_%d_%H_%M_%S')


def get_current_timestamp():
    """
    获取当前时间戳
    :return:
    """

    return time.time()
