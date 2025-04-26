import logging
import logging.config
import os
import weakref
from enum import Enum, unique
from functools import lru_cache
from threading import Lock
from typing import TypeVar, Type

from varname import argname

# 泛型类型变量用于类型提示
T = TypeVar('T', bound='HappyLog')

# 添加 TRACE 日志级别
TRACE_LEVEL_NUM = 9
logging.addLevelName(TRACE_LEVEL_NUM, 'TRACE')


class HappyLogLevelInt(Enum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5


@unique
class HappyLogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = TRACE_LEVEL_NUM

    @staticmethod
    def get_list() -> list[int]:
        return [level.value for level in HappyLogLevel]


@lru_cache(maxsize=None)
def to_happy_log_level(level: int) -> HappyLogLevel:
    mapping: dict[int, HappyLogLevel] = {
        HappyLogLevelInt.CRITICAL.value: HappyLogLevel.CRITICAL,
        HappyLogLevelInt.ERROR.value: HappyLogLevel.ERROR,
        HappyLogLevelInt.WARNING.value: HappyLogLevel.WARNING,
        HappyLogLevelInt.INFO.value: HappyLogLevel.INFO,
        HappyLogLevelInt.DEBUG.value: HappyLogLevel.DEBUG,
        HappyLogLevelInt.TRACE.value: HappyLogLevel.TRACE,
    }
    if level in mapping:
        return mapping[level]

    raise ValueError('建议使用 HappyLogLevel 枚举设置日志等级')


class SingletonMeta(type):
    """线程安全的单例元类，使用弱引用减少全局状态"""
    _instances: weakref.WeakValueDictionary[type[T], T] = weakref.WeakValueDictionary()
    _lock: Lock = Lock()

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        with cls._lock:
            instance = cls._instances.get(cls)
            if instance is None:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return instance


class HappyLog(metaclass=SingletonMeta):
    def __init__(self, log_ini: str = '', logger_name: str = '') -> None:
        self.logger: logging.Logger | None = None
        self._validate_ini_path(log_ini)
        self.log_ini = log_ini
        self.logger_name = logger_name
        self.log_level = HappyLogLevel.INFO
        self._init_logging_system()
        self.load_config()

    @staticmethod
    def _validate_ini_path(path: str) -> None:
        if path and not os.path.exists(path):
            raise FileNotFoundError('日志配置文件不存在: %s' % path)

    @staticmethod
    def _init_logging_system() -> None:
        def trace(self, msg, *args, **kwargs):
            if self.isEnabledFor(TRACE_LEVEL_NUM):
                self._log(TRACE_LEVEL_NUM, msg, args, **kwargs)

        logging.Logger.trace = trace

    @classmethod
    def get_instance(cls: type[T], log_ini: str = '', logger_name: str = '', reset: bool = False) -> T:
        """获取或重置单例实例"""
        if reset:
            with cls._lock:
                if cls in cls._instances:
                    del cls._instances[cls]

        return cls(log_ini, logger_name)

    def get_logger(self, logger_name: str = '') -> logging.Logger:
        return logging.getLogger(logger_name or self.logger_name)

    def set_level(self, log_level: int | HappyLogLevel) -> None:
        if isinstance(log_level, int):
            log_level = to_happy_log_level(log_level)

        self.log_level = log_level

        if self.logger:
            self.logger.setLevel(log_level.value)

    def load_config(self) -> None:
        if self.log_ini:
            self._load_ini_config()
        else:
            self._load_default_config()

    def _load_ini_config(self) -> None:
        self._clean_handlers()

        logging.config.fileConfig(self.log_ini, disable_existing_loggers=False)

        self.logger = logging.getLogger(self.logger_name)
        self.logger.info(f'日志配置文件 "{self.log_ini}" 加载成功')

    def _load_default_config(self) -> None:
        self._clean_handlers()
        self.logger = logging.getLogger(self.logger_name)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s %(process)s [%(levelname)s] %(module)s: %(message)s',
                                               '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(handler)
        self.logger.setLevel(self.log_level.value)

    def _clean_handlers(self) -> None:
        if self.logger:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                handler.close()

    # 日志接口
    def enter_func(self, func_name: str) -> None:
        self.logger.trace(f"Enter function: {func_name}")

    def exit_func(self, func_name: str) -> None:
        self.logger.trace(f"Exit function: {func_name}")

    def var(self, var_name: str, var_value: object) -> None:
        self.logger.trace(f'var->{var_name}={var_value}')

    def critical(self, *args: object, sep: str = ' ') -> None:
        self.logger.critical(sep.join(str(arg) for arg in args))

    def error(self, *args: object, sep: str = ' ') -> None:
        self.logger.error(sep.join(str(arg) for arg in args))

    def warning(self, *args: object, sep: str = ' ') -> None:
        self.logger.warning(sep.join(str(arg) for arg in args))

    def info(self, *args: object, sep: str = ' ') -> None:
        self.logger.info(sep.join(str(arg) for arg in args))

    def debug(self, *args: object, sep: str = ' ') -> None:
        self.logger.debug(sep.join(str(arg) for arg in args))

    def trace(self, *args: object, sep: str = ' ') -> None:
        self.logger.trace(sep.join(str(arg) for arg in args))

    def input(self, var_name: str, var_value: object) -> None:
        self.logger.trace(f'input->{var_name}={var_value}')

    def output(self, var_name: str, var_value: object) -> None:
        self.logger.trace(f'output->{var_name}={var_value}')

    def vardump(self, var: object) -> None:
        """使用 varname 自动获取变量名"""
        self.logger.trace('var->%s=%s', argname('var'), var)

    def inputdump(self, var: object) -> None:
        """使用 varname 自动获取输入变量名"""
        self.logger.trace('input->%s=%s', argname('var'), var)

    def outputdump(self, var: object) -> None:
        """使用 varname 自动获取输出变量名"""
        self.logger.trace('output->%s=%s', argname('var'), var)
