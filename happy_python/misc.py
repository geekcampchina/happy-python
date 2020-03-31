#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from happy_python import HappyLog

hlog = HappyLog.get_instance()


def callback_succeed_once(callback, max_time=100, is_sleep=True, interval=0.1, **kwargs):
    """
    保证方法必须成功执行一次，如果出现异常则重试。
    :param interval: sleep间隔时间，单位秒
    :param is_sleep: 是否使用time.sleep
    :param max_time: 最大尝试次数
    :param callback:
    :param kwargs:
    :return:
    """
    n = 1
    result = None

    while True:
        if n >= max_time:
            hlog.critical('回调函数（%s）已经执行失败%s次，终止执行' % (callback, max_time))
            break

        try:
            n += 1
            result = callback(**kwargs)
            break
        except Exception as e:
            if is_sleep:
                time.sleep(interval)

            hlog.critical(e)

    return result
