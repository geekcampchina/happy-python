import logging
import logging.config
import os
from enum import Enum, unique
from typing import Union

_HappyLogSingletonObj = None
_HappyLogSingletonDefaultObj = None


@unique
class HappyLogLevel(Enum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5

    @staticmethod
    def get_list():
        """
        返回日志等级数字列表
        :return:
        """
        return [*range(HappyLogLevel.CRITICAL.value, HappyLogLevel.CRITICAL.TRACE.value + 1)]


TRACE_LEVEL_NUM = 9
logging.addLevelName(TRACE_LEVEL_NUM, HappyLogLevel.TRACE.name)


def trace_log_func(self, message, *args, **kws):
    """
    增加自定义日志等级
    """
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


class HappyLog(object):
    log_ini = ''
    logger_name = ''
    logger = None
    default_file_handler = None
    default_stream_handler = None
    default_handler_count = 0

    def __init__(self, log_ini='', logger_name=''):
        self.log_level: HappyLogLevel = HappyLogLevel.INFO
        self.logger_name = logger_name
        self.log_ini = log_ini

        logging.Logger.trace = trace_log_func
        self.load_config()

    @staticmethod
    def get_instance(log_ini='', logger_name=''):
        """
        单例模式
        """
        global _HappyLogSingletonObj
        global _HappyLogSingletonDefaultObj

        if len(log_ini) > 0 and not os.path.exists(log_ini):
            logger = logging.getLogger()
            logger.error("日志配置文件 %s 不存在" % log_ini)
            exit(1)

        if _HappyLogSingletonObj:
            if len(log_ini) > 0:
                _HappyLogSingletonObj.load_config()

            return _HappyLogSingletonObj

        if len(log_ini) > 0:
            _HappyLogSingletonObj = HappyLog(log_ini, logger_name)
            obj = _HappyLogSingletonObj
        else:
            if not _HappyLogSingletonDefaultObj:
                _HappyLogSingletonDefaultObj = HappyLog(log_ini, logger_name)

            obj = _HappyLogSingletonDefaultObj

        return obj

    def get_logger(self):
        return self.logger

    def set_level(self, log_level: int = HappyLogLevel.INFO.value):
        """
        :param log_level: 有效范围0~5
        :return:
        """
        self.log_level = HappyLogLevel(log_level)
        self.logger.setLevel(self.log_level.name)

    def build_default_config(self, handler: Union[logging.StreamHandler, logging.FileHandler], _formatter: logging.Formatter):
        self.default_handler_count += 1

        self.logger = logging.getLogger()

        self.logger.setLevel(self.log_level.name)
        handler.setFormatter(_formatter)
        self.logger.addHandler(handler)

        if self.default_handler_count == 1:
            self.logger.info('未启用日志配置文件，加载默认设置')

    def load_stream_default_config(self, formatter: logging.Formatter = logging.Formatter(
        '%(asctime)s %(process)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')):
        """
        载入默认日志配置
        :return:
        """
        import sys

        if self.logger and self.default_stream_handler:
            self.logger.removeHandler(self.default_stream_handler)

        self.default_stream_handler = logging.StreamHandler(sys.stdout)
        self.build_default_config(handler=self.default_stream_handler, _formatter=formatter)

    def load_file_default_config(self,
                                 filename: str,
                                 formatter: logging.Formatter = logging.Formatter(
                                     '%(asctime)s %(process)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')):
        """
        载入默认日志配置
        :return:
        """
        from pathlib import Path

        if filename:
            Path(filename).parent.mkdir(parents=True, exist_ok=True)

            if self.logger and self.default_file_handler:
                self.logger.removeHandler(self.default_file_handler)

            self.default_file_handler = logging.FileHandler(filename)
            self.build_default_config(handler=self.default_file_handler, _formatter=formatter)
        else:
            self.logger.error('必须指定日志文件名')

    def load_config(self):
        if os.path.exists(self.log_ini):
            logging.config.fileConfig(self.log_ini)
            self.logger = logging.getLogger()

            if self.default_file_handler:
                self.logger.removeHandler(self.default_file_handler)

            if self.default_stream_handler:
                self.logger.removeHandler(self.default_stream_handler)

            self.logger.info('日志配置文件 \'%s\' 加载成功' % self.log_ini)

            if self.logger_name:
                self.logger = logging.getLogger(self.logger_name)
        else:
            self.load_stream_default_config()

    def enter_func(self, func_name: str):
        self.logger.trace("Enter function: %s" % func_name)

    def exit_func(self, func_name: str):
        self.logger.trace("Exit function: %s" % func_name)

    def var(self, var_name: str, var_value):
        self.logger.trace('var->%s=%s' % (var_name, var_value))

    def critical(self, s: str):
        self.logger.critical(s)

    def error(self, s: str):
        self.logger.error(s)

    def warning(self, s: str):
        self.logger.warning(s)

    def info(self, s: str):
        self.logger.info(s)

    def debug(self, s: str):
        self.logger.debug(s)

    def trace(self, s: str):
        self.logger.trace(s)

    def input(self, var_name: str, var_value):
        self.logger.trace('input->%s=%s' % (var_name, var_value))

    def output(self, var_name: str, var_value):
        self.logger.trace('output->%s=%s' % (var_name, var_value))
