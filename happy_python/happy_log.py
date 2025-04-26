# noinspection ALL
"""
模块概述
    本模块提供了 HappyLog 类和相关组件，用于简化 Python logging
    的异步日志管理。支持自定义配置文件、动态切换同步/异步模式、
    以及 TRACE 级别的细粒度跟踪。

主要组件
    - AsyncLogManager: 异步日志后台管理（线程安全单例）
    - SafeQueueListener: 带异常保护的 QueueListener
    - FallbackQueueHandler: 队列满时回落到同步处理
    - HappyLogLevel: 自定义日志级别枚举（包含 TRACE）
    - HappyLog: 日志入口，单例模式

快速开始
    >>> from happy_python import HappyLog, HappyLogLevel

    # 1) 获取或创建日志单例（不重置）
    >>> hlog = HappyLog(reset=False, log_ini='config/log.ini', logger_name='app')

    # 2) 切换同步/异步输出模式
    >>> HappyLog.set_async_mode(True)   # 启用异步模式
    >>> HappyLog.set_async_mode(False)  # 切换回同步模式

    # 3) 设置日志级别
    >>> hlog.set_level(HappyLogLevel.DEBUG)

    # 4) 记录日志
    >>> hlog.info('Application started.')
    >>> hlog.debug('Debugging details...')
    >>> hlog.trace('Entering critical section.')

    # 5) 细粒度跟踪
    >>> hlog.enter_func('process_data')
    >>> hlog.var('item_count', len(['a']))
    >>> hlog.exit_func('process_data')

构造函数参数
    reset: bool
        是否重置单例。传 True 时会丢弃旧实例并重新创建。
        默认为 False。
    log_ini: str
        日志配置文件路径（INI 格式）。为空串时使用内置默认配置。
    logger_name: str
        获取的 logger 名称，对应 logging.getLogger(name)。默认为 'root'。

注意事项
    - 在程序退出时会自动调用 atexit 注册的 cleanup() 关闭所有 handler。
    - 多线程环境下推荐使用异步模式（set_async_mode(True)）。
    - 自定义 TRACE 级别数值为 9，可通过 hlog.trace() 输出。

更多信息请参考模块内各类的 docstring 以及示例代码。
"""
import logging
import logging.config
import logging.handlers
import os
import queue
import signal
import sys
import time
import weakref
from dataclasses import dataclass, field
from enum import Enum, unique
from functools import lru_cache
from threading import Lock, Thread
from typing import TypeVar, Optional, Any, Type

from varname import argname

# 泛型类型变量
T = TypeVar('T', bound='HappyLog')

# 日志队列监控阈值和监控间隔（秒）
QUEUE_MONITOR_THRESHOLD = 1000
QUEUE_MONITOR_INTERVAL = 60

# 添加 TRACE 日志级别
TRACE_LEVEL_NUM = 9
logging.addLevelName(TRACE_LEVEL_NUM, 'TRACE')


class SafeQueueListener(logging.handlers.QueueListener):
    """带异常保护的 QueueListener"""

    def handle(self, record: logging.LogRecord) -> None:
        try:
            super().handle(record)
        except Exception as e:
            logging.getLogger('AsyncLogManager').warning('Handler %s raised exception: %s', record.name, e)


@dataclass(init=False)
class AsyncLogManager:
    """异步日志全局管理器（线程安全单例）"""
    _instance: Optional['AsyncLogManager'] = None
    _lock: Lock = Lock()

    log_queue: queue.Queue = field(init=False)
    queue_listener: Optional[SafeQueueListener] = field(init=False, default=None)
    active_handlers: dict[str, list[logging.Handler]] = field(init=False, default_factory=dict)
    handler_pool: dict[str, logging.Handler] = field(init=False, default_factory=dict)
    async_enabled: bool = field(init=False, default=True)

    def __new__(cls) -> 'AsyncLogManager':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__init__()

            return cls._instance

    def __init__(self) -> None:
        # 防止重复初始化
        if hasattr(self, 'log_queue'):
            return

        self.log_queue = queue.Queue(maxsize=10000)
        self.queue_listener = None
        self.active_handlers = {}
        self.handler_pool = {}
        self.async_enabled = True

        # 启动监控线程
        monitor = Thread(target=self._monitor_loop, daemon=True, name='AsyncLogMonitor')
        monitor.start()

    def _monitor_loop(self) -> None:
        while True:
            size = self.log_queue.qsize()

            if size > QUEUE_MONITOR_THRESHOLD:
                logging.getLogger('AsyncLogManager').warning(
                    'Log queue size %d exceeds threshold %d',
                    size, QUEUE_MONITOR_THRESHOLD
                )

            time.sleep(QUEUE_MONITOR_INTERVAL)

    def fallback(self, record: logging.LogRecord) -> None:
        # 异步关闭或队列满时，同步处理
        handlers = self.active_handlers.get(record.name, [])
        for h in handlers:
            # noinspection PyBroadException
            try:
                h.handle(record)
            except Exception:
                pass

    def start_listener(self, handlers: list[logging.Handler]) -> None:
        if not self.async_enabled:
            return

        with self._lock:
            if self.queue_listener is None:
                lst = SafeQueueListener(self.log_queue, *handlers, respect_handler_level=True)
                lst.start()
                self.queue_listener = lst
            else:
                # handlers 为元组，合并新的 handlers
                old = self.queue_listener.handlers
                new = tuple(h for h in handlers if h not in old)

                if new:
                    self.queue_listener.handlers = old + new

    def stop_listener(self) -> None:
        with self._lock:
            if self.queue_listener is not None:
                self.queue_listener.stop()
                self.queue_listener = None

    def register_handlers(self, logger_name: str, handlers: list[logging.Handler]) -> None:
        self.active_handlers[logger_name] = handlers

    def unregister_handlers(self, logger_name: str) -> None:
        if logger_name in self.active_handlers:
            for h in self.active_handlers[logger_name]:
                # noinspection PyBroadException
                try:
                    h.close()
                except Exception:
                    pass
            del self.active_handlers[logger_name]

        if not self.active_handlers:
            self.stop_listener()

    def get_or_create_handler(self, key: str, factory: Any) -> logging.Handler:
        if key not in self.handler_pool:
            self.handler_pool[key] = factory()

        return self.handler_pool[key]

    def set_async_enabled(self, enabled: bool) -> None:
        self.async_enabled = enabled

        if not enabled:
            self.stop_listener()


class FallbackQueueHandler(logging.handlers.QueueHandler):
    """自定义 QueueHandler，队列满时回退到同步处理"""

    def enqueue(self, record: logging.LogRecord) -> None:
        try:
            if not AsyncLogManager().async_enabled:
                raise queue.Full

            super().enqueue(record)
        except queue.Full:
            AsyncLogManager().fallback(record)


# 优雅关停

# noinspection PyUnusedLocal
def _graceful_shutdown(signum: int, frame: Any) -> None:
    AsyncLogManager().stop_listener()
    sys.exit(0)


signal.signal(signal.SIGTERM, _graceful_shutdown)
signal.signal(signal.SIGINT, _graceful_shutdown)


@unique
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
        return [lvl.value for lvl in HappyLogLevel]


@lru_cache(maxsize=None)
def to_happy_log_level(level: int) -> HappyLogLevel:
    mapping = {
        HappyLogLevelInt.CRITICAL.value: HappyLogLevel.CRITICAL,
        HappyLogLevelInt.ERROR.value: HappyLogLevel.ERROR,
        HappyLogLevelInt.WARNING.value: HappyLogLevel.WARNING,
        HappyLogLevelInt.INFO.value: HappyLogLevel.INFO,
        HappyLogLevelInt.DEBUG.value: HappyLogLevel.DEBUG,
        HappyLogLevelInt.TRACE.value: HappyLogLevel.TRACE,
    }

    if level in mapping:
        return mapping[level]

    raise ValueError('建议使用 HappyLogLevel 枚举设置日志等级: %d' % level)


class SingletonMeta(type):
    _instances: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
    _lock = Lock()

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        # 1) 看看用户有没有传 reset=True
        reset_flag = kwargs.get('reset', False)

        with cls._lock:
            if reset_flag:
                # 删除旧实例，下次创建新的
                cls._instances.pop(cls, None)

            inst = cls._instances.get(cls)

            if inst is None:
                # 第一次创建或被 reset 后重新创建
                inst = super().__call__(*args, **kwargs)
                cls._instances[cls] = inst

        return inst


@dataclass
class HappyLog(metaclass=SingletonMeta):
    reset: bool = False
    log_ini: str = ''
    logger_name: str = 'root'
    log_level: HappyLogLevel = HappyLogLevel.INFO
    logger: logging.Logger | None = field(default=None, init=False)
    _async_mgr: AsyncLogManager = field(default_factory=AsyncLogManager, init=False, repr=False)

    def __post_init__(self) -> None:
        self._validate_ini_path(self.log_ini)
        self._init_logging_system()
        self.load_config()

    @staticmethod
    def _validate_ini_path(path: str) -> None:
        if path and not os.path.exists(path):
            raise FileNotFoundError('日志配置文件不存在: %s' % path)

    @staticmethod
    def _init_logging_system() -> None:
        def trace(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            if self.isEnabledFor(TRACE_LEVEL_NUM):
                self._log(TRACE_LEVEL_NUM, msg, args, **kwargs)

        logging.Logger.trace = trace

    @classmethod
    def set_async_mode(cls, enabled: bool) -> None:
        AsyncLogManager().set_async_enabled(enabled)

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
        self._setup_logging(self.logger.handlers.copy())
        self.logger.info('异步日志已启用，配置文件 "%s" 加载成功', self.log_ini)

    def _load_default_config(self) -> None:
        self._clean_handlers()
        self.logger = logging.getLogger(self.logger_name)
        console = self._async_mgr.get_or_create_handler('console', lambda: logging.StreamHandler())
        console.setFormatter(logging.Formatter(
            '%(asctime)s %(process)d [%(levelname)s] %(module)s: %(message)s',
            '%Y-%m-%d %H:%M:%S'
        ))
        self._setup_logging([console])
        self.logger.setLevel(self.log_level.value)

    def _setup_logging(self, handlers: list[logging.Handler]) -> None:
        self._async_mgr.register_handlers(self.logger_name, handlers)

        if self._async_mgr.async_enabled:
            self._async_mgr.start_listener(handlers)
            queue_handler = FallbackQueueHandler(self._async_mgr.log_queue)
            self._clean_handlers()
            self.logger.addHandler(queue_handler)
        else:
            self._clean_handlers()

            for h in handlers:
                self.logger.addHandler(h)

    def _clean_handlers(self) -> None:
        if self.logger:
            for h in list(self.logger.handlers):
                self.logger.removeHandler(h)

                # noinspection PyBroadException
                try:
                    h.close()
                except Exception:
                    pass

    def cleanup(self) -> None:
        self._async_mgr.unregister_handlers(self.logger_name)
        self._clean_handlers()

    # 日志接口
    def enter_func(self, func_name: str) -> None:
        self.logger.trace('Enter function: %s', func_name)

    def exit_func(self, func_name: str) -> None:
        self.logger.trace('Exit function: %s', func_name)

    def var(self, var_name: str, var_value: Any) -> None:
        self.logger.trace('var->%s=%s', var_name, var_value)

    def critical(self, *args: Any, sep: str = ' ') -> None:
        self.logger.critical(sep.join(str(arg) for arg in args))

    def error(self, *args: Any, sep: str = ' ') -> None:
        self.logger.error(sep.join(str(arg) for arg in args))

    def warning(self, *args: Any, sep: str = ' ') -> None:
        self.logger.warning(sep.join(str(arg) for arg in args))

    def info(self, *args: Any, sep: str = ' ') -> None:
        self.logger.info(sep.join(str(arg) for arg in args))

    def debug(self, *args: Any, sep: str = ' ') -> None:
        self.logger.debug(sep.join(str(arg) for arg in args))

    def trace(self, *args: Any, sep: str = ' ') -> None:
        self.logger.trace(sep.join(str(arg) for arg in args))

    def input(self, var_name: str, var_value: Any) -> None:
        self.logger.trace('input->%s=%s', var_name, var_value)

    def output(self, var_name: str, var_value: Any) -> None:
        self.logger.trace('output->%s=%s', var_name, var_value)

    def vardump(self, var: Any) -> None:
        self.logger.trace('var->%s=%s', argname('var'), var)

    def inputdump(self, var: Any) -> None:
        self.logger.trace('input->%s=%s', argname('var'), var)

    def outputdump(self, var: Any) -> None:
        self.logger.trace('output->%s=%s', argname('var'), var)


# 程序退出时自动清理
import atexit

atexit.register(HappyLog().cleanup)
