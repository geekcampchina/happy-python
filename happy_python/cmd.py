#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import subprocess
from multiprocessing import Process
from happy_python import HappyLog

hlog = HappyLog.get_instance()


def get_exit_code_of_cmd(cmd: str) -> int:
    """
    执行系统命令，屏蔽标准输出，返回命令退出代码
    :cmd: 命令行
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True)
    result = cp.returncode

    hlog.debug("result=%d" % result)
    hlog.exit_func(func_name)

    return result


def get_exit_status_of_cmd(cmd: str) -> bool:
    """
    执行系统命令，屏蔽标准输出，根据命令退出代码返回布尔值
    :cmd: 命令行
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    result = get_exit_code_of_cmd(cmd) == 0

    hlog.debug("Command %s" % ('succeeded' if result else 'failed'))
    hlog.exit_func(func_name)

    return result


def get_output_of_cmd(cmd: str, encoding='UTF-8', remove_white_char=False) -> str:
    """
    执行系统命令，返回命令执行结果字符串
    :cmd: 命令行
    :encoding: 指定返回字符串编码
    :remove_white_char: 是否移除返回字符串最后的空白字符，比如换行符
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True, capture_output=True)
    result = str(cp.stdout, encoding)

    if remove_white_char:
        result = result.strip()

    hlog.debug("result=%s" % result)
    hlog.exit_func(func_name)

    return result


def non_blocking_exe_cmd(cmd: str) -> None:
    """
    使用非阻塞的子进程执行命令
    :cmd: 命令行
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.trace("cmd=%s" % cmd)

    child_process = Process(target=get_exit_status_of_cmd, args=(cmd, ))
    child_process.start()
    # 不等待子进程返回，不需要使用 child_process.join()
    hlog.exit_func(func_name)
