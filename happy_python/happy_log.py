import logging
import logging.config
import os
from enum import Enum, unique
from threading import Lock
from typing import Union

from varname import argname

_HappyLogSingletonObj = None
_HappyLogSingletonDefaultObj = None
_singleton_lock = Lock()

TRACE_LEVEL_NUM = 9
logging.addLevelName(TRACE_LEVEL_NUM, 'TRACE')


@unique
class HappyLogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = TRACE_LEVEL_NUM

    @staticmethod
    def get_list():
        return [level.value for level in HappyLogLevel]

class HappyLog:
    def __init__(self, log_ini='', logger_name=''):
        self.logger = None
        self._validate_ini_path(log_ini)
        self.log_ini = log_ini
        self.logger_name = logger_name
        self.log_level = HappyLogLevel.INFO
        self._init_logging_system()
        self.load_config()

    @staticmethod
    def _validate_ini_path(path):
        if path and not os.path.exists(path):
            raise FileNotFoundError('日志配置文件不存在：%s' % path)

    @staticmethod
    def _init_logging_system():
        logging.Logger.trace = lambda self, msg, *args, **kwargs: \
            self._log(TRACE_LEVEL_NUM, msg, args, **kwargs) if self.isEnabledFor(TRACE_LEVEL_NUM) else None

    @classmethod
    def get_instance(cls, log_ini='', logger_name='', is_new_instance=False):
        global _HappyLogSingletonObj, _HappyLogSingletonDefaultObj

        if is_new_instance:
            _HappyLogSingletonObj = None
            _HappyLogSingletonDefaultObj = None

        with _singleton_lock:
            if log_ini:
                if not _HappyLogSingletonObj:
                    _HappyLogSingletonObj = cls(log_ini, logger_name)

                return _HappyLogSingletonObj

            if not _HappyLogSingletonDefaultObj:
                _HappyLogSingletonDefaultObj = cls(log_ini, logger_name)

            return _HappyLogSingletonDefaultObj

    def get_logger(self):
        return self.logger

    def set_level(self, log_level: Union[int, HappyLogLevel]):
        if isinstance(log_level, int):
            log_level = HappyLogLevel(log_level)

        self.log_level = log_level
        self.logger.setLevel(log_level.value)

    def load_config(self):
        if self.log_ini:
            self._load_ini_config()
        else:
            self._load_default_config()

    def _load_ini_config(self):
        self._clean_handlers()  # 加载前清理handler

        logging.config.fileConfig(
            self.log_ini,
            disable_existing_loggers=False
        )
        self.logger = logging.getLogger(self.logger_name)
        self._clean_handlers()
        self.logger.info('日志配置文件 "%s" 加载成功' % self.log_ini)

    def _load_default_config(self):
        self._clean_handlers()  # 加载前清理handler

        self.logger = logging.getLogger(self.logger_name)
        self._clean_handlers()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(process)s [%(levelname)s] %(module)s: %(message)s',
            '%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(self.log_level.value)

    def _clean_handlers(self):
        if self.logger:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                handler.close()

    def enter_func(self, func_name: str):
        self.logger.trace("Enter function: %s" % func_name)

    def exit_func(self, func_name: str):
        self.logger.trace("Exit function: %s" % func_name)

    def var(self, var_name: str, var_value):
        self.logger.trace('var->%s=%s' % (var_name, var_value))

    def critical(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.critical(sep.join(_args))

    def error(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.error(sep.join(_args))

    def warning(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.warning(sep.join(_args))

    def info(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.info(sep.join(_args))

    def debug(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.debug(sep.join(_args))

    def trace(self, *args, sep=' '):
        _args = [str(arg) for arg in args]
        self.logger.trace(sep.join(_args))

    def input(self, var_name: str, var_value):
        self.logger.trace('input->%s=%s' % (var_name, var_value))

    def output(self, var_name: str, var_value):
        self.logger.trace('output->%s=%s' % (var_name, var_value))

    def vardump(self, var):
        self.logger.trace('var->%s=%s' % (argname('var'), var))

    def inputdump(self, var):
        self.logger.trace('input->%s=%s' % (argname('var'), var))

    def outputdump(self, var):
        self.logger.trace('output->%s=%s' % (argname('var'), var))
