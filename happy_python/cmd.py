#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import subprocess
from multiprocessing import Process
from happy_python import HappyLog

hlog = HappyLog.get_instance()


def get_exit_status_of_cmd(cmd: str) -> bool:
    """
    执行系统命令，屏蔽标准输出，根据命令退出代码返回布尔值
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True)
    result = cp.returncode == 0

    hlog.debug("Command %s" % ('succeeded' if result else 'failed'))
    hlog.exit_func(func_name)

    return result


def get_output_of_cmd(cmd: str, encoding='UTF-8') -> str:
    """
    执行系统命令，返回命令执行结果字符串
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True, capture_output=True)
    result = str(cp.stdout, encoding)

    hlog.debug("result=%s" % result)
    hlog.exit_func(func_name)

    return result


def non_blocking_exe_cmd(cmd: str) -> None:
    """
    使用非阻塞的子进程执行命令
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.trace("cmd=%s" % cmd)

    child_process = Process(target=get_exit_status_of_cmd, args=(cmd, ))
    child_process.start()
    # 不等待子进程返回，不需要使用 child_process.join()
    hlog.exit_func(func_name)
