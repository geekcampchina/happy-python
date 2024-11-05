import inspect
import os
import subprocess
from multiprocessing import Process

from happy_python import HappyLog

hlog = HappyLog.get_instance()


def get_exit_code_of_cmd(cmd: str,
                         encoding='UTF-8',
                         is_show_error=True,
                         is_show_output=False,
                         is_raise_exception=False) -> int:
    """
    执行系统命令，屏蔽标准输出，返回命令退出代码
    :cmd: 命令行
    :encoding: 指定编码
    :is_show_error: 显示错误提示信息
    :is_show_output: 打印命令输出
    :is_raise_exception: 执行失败时，抛出异常
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    if not cmd:
        hlog.critical('"cmd" 参数不能为空')
        return 1

    cp = subprocess.run(cmd, shell=True, capture_output=True, check=is_raise_exception)
    result = cp.returncode

    if result != 0 and is_show_error:
        hlog.error('error code: %d, error message: %s' % (result, str(cp.stderr, encoding=encoding).strip()))

    if is_show_output:
        hlog.info('Command output:%s%s' % (os.linesep, str(cp.stdout, encoding=encoding).strip()))

    hlog.debug("result=%d" % result)
    hlog.exit_func(func_name)

    return result


def get_exit_status_of_cmd(cmd: str,
                           encoding='UTF-8',
                           is_show_error=True,
                           is_show_output=False,
                           is_raise_exception=False) -> bool:
    """
    执行系统命令，屏蔽标准输出，根据命令退出代码返回布尔值
    :cmd: 命令行
    :encoding: 指定编码
    :is_show_error: 显示错误提示信息
    :is_show_output: 打印命令输出
    :is_raise_exception: 执行失败时，抛出异常
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    result = get_exit_code_of_cmd(cmd, encoding, is_show_error, is_show_output, is_raise_exception) == 0

    hlog.debug("Command %s" % ('succeeded' if result else 'failed'))
    hlog.exit_func(func_name)

    return result


def get_output_of_cmd(cmd: str, encoding='UTF-8', remove_white_char=False, is_raise_exception=False) -> str:
    """
    执行系统命令，返回命令执行结果字符串
    :cmd: 命令行
    :encoding: 指定返回字符串编码
    :remove_white_char: 是否移除返回字符串最后的空白字符，比如换行符
    :is_raise_exception: 执行失败时，抛出异常
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True, capture_output=True, check=is_raise_exception)
    result = str(cp.stdout, encoding)

    if remove_white_char:
        result = result.strip()

    if cp.returncode != 0:
        hlog.error('error code: %d, error message: %s' % (cp.returncode, str(cp.stderr, encoding=encoding)))
        hlog.error(result)

    hlog.debug("result=%s" % result)
    hlog.exit_func(func_name)

    return result


def execute_cmd(cmd: str, encoding='UTF-8', remove_white_char=False, is_raise_exception=False) -> (int, str):
    """
    执行系统命令，返回 命令执行结果字符串和返回代码
    :cmd: 命令行
    :encoding: 指定返回字符串编码
    :remove_white_char: 是否移除返回字符串最后的空白字符，比如换行符
    :is_raise_exception: 执行失败时，抛出异常
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.debug("cmd=%s" % cmd)

    cp = subprocess.run(cmd, shell=True, capture_output=True, check=is_raise_exception)
    result = str(cp.stdout, encoding)

    if remove_white_char:
        result = result.strip()

    if cp.returncode != 0:
        hlog.error('error code: %d, error message: %s' % (cp.returncode, str(cp.stderr, encoding=encoding)))
        hlog.error(result)

    hlog.debug("result=%s" % result)
    hlog.exit_func(func_name)

    return cp.returncode, result


def non_blocking_exe_cmd(cmd: str) -> None:
    """
    使用非阻塞的子进程执行命令
    :cmd: 命令行
    :return:
    """
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.trace("cmd=%s" % cmd)

    child_process = Process(target=get_exit_status_of_cmd, args=(cmd,))
    child_process.start()
    # 不等待子进程返回，不需要使用 child_process.join()
    hlog.exit_func(func_name)


def exe_cmd_and_poll_output(cmd, encoding='UTF-8', is_capture_output=False):
    """
    将命令输出实时打印到标准输出
    :param is_capture_output:
    :param cmd: 命令行
    :param encoding: 字符编码
    :return: 标准输出字符串列表
    """
    import shlex

    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    hlog.trace("cmd=%s" % cmd)

    output = list()
    cmd = shlex.split(cmd)

    with subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        while p.poll() is None:
            line = p.stdout.readline()
            line = str(line, encoding=encoding)
            print(line, end='')

            if is_capture_output:
                output.append(line)

    if p.returncode != 0:
        hlog.error('Command execution failed')

    hlog.exit_func(func_name)
    return output
