import time
from datetime import datetime

from enum import Enum


class HappyDatetimeFormat(Enum):
    Ymd_HMS = '%Y-%m-%d %H:%M:%S'
    YmdHMS = '%Y%m%d%H%M%S'
    Ymd = '%Y%m%d'
    HMS = '%H%M%S'
    Y_m_d_H_M_S = '%Y_%m_%d_%H_%M_%S'


def str_to_datetime(date_string: str, custom_format: HappyDatetimeFormat = HappyDatetimeFormat.Ymd_HMS) -> datetime:
    """
    将时间字符串转换为datetime对象
    :param date_string: 时间字符串，如2018-08-27 02:09:34
    :param custom_format: 日期格式
    :return:
    """

    return datetime.strptime(date_string, custom_format.value)


def datetime_to_str(datetime_obj: datetime, custom_format: HappyDatetimeFormat = HappyDatetimeFormat.Ymd_HMS) -> str:
    """
    将datetime对象转换为指定格式的字符串
    :param datetime_obj: 时间对象
    :param custom_format: 日期格式
    :return:
    """

    return datetime_obj.strftime(custom_format.value)


def get_current_datetime(custom_format: HappyDatetimeFormat = HappyDatetimeFormat.Ymd_HMS) -> str:
    """
    获取当前时间字符串
    :param custom_format: 日期格式，默认 2018-09-03 13:36:02
    :return: 时间字符串
    """

    now = datetime.now()
    return datetime_to_str(now, custom_format)


def get_current_timestamp() -> float:
    """
    获取当前时间戳
    :return:
    """

    return time.time()
