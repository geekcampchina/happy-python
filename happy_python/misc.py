#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect

from happy_python import HappyLog

hlog = HappyLog.get_instance()


def callback_succeed_once(callback, max_time=10, **kwargs) -> bool:
    """
    保证方法必须成功执行一次，如果出现异常则重试。
    :param max_time:
    :param callback:
    :param kwargs:
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

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
            hlog.critical(e)

    hlog.var('result', result)
    hlog.exit_func(func_name)
    return result
