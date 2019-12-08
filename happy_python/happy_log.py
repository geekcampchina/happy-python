#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.config
import os

_HappyLogSingletonObj = None
_HappyLogSingletonDefaultObj = None

TRACE_LEVEL_NUM = 9
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


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

    def __init__(self, log_ini='', logger_name=''):
        self.logger_name = logger_name
        self.log_ini = log_ini

        logging.Logger.trace = trace_log_func
        self.load_config()

    @staticmethod
    def get_instance(log_ini='', logger_name=''):
        """
        单例模式
        :param log_ini:
        :param logger_name:
        :return:
        """
        global _HappyLogSingletonObj
        global _HappyLogSingletonDefaultObj

        if _HappyLogSingletonObj:
            return _HappyLogSingletonObj

        if os.path.exists(log_ini):
            _HappyLogSingletonObj = HappyLog(log_ini, logger_name)

            obj = _HappyLogSingletonObj
        else:
            if not _HappyLogSingletonDefaultObj:
                _HappyLogSingletonDefaultObj = HappyLog(log_ini, logger_name)

            obj = _HappyLogSingletonDefaultObj

        return obj

    def get_logger(self):
        return self.logger

    def load_default_config(self):
        """
        载入默认日志配置
        :return:
        """
        import sys

        self.logger = logging.getLogger()
        self.logger.setLevel('INFO')
        self.default_file_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(process)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        self.default_file_handler.setFormatter(formatter)
        self.logger.addHandler(self.default_file_handler)

        self.logger.debug('未启用日志配置文件，加载默认设置。')

    def load_config(self):
        if os.path.exists(self.log_ini):
            logging.config.fileConfig(self.log_ini)
            self.logger = logging.getLogger()

            if self.default_file_handler:
                self.logger.removeHandler(self.default_file_handler)

            self.logger.info('日志配置文件 \'%s\' 加载成功。' % self.log_ini)

            if self.logger_name:
                self.logger = logging.getLogger(self.logger_name)
        else:
            self.load_default_config()

    def enter_func(self, func_name: str):
        self.logger.trace("Enter function: %s" % func_name)

    def exit_func(self, func_name: str):
        self.logger.trace("Exit function: %s" % func_name)

    def var(self, var_name: str, var_value):
        self.logger.trace('%s=%s' % (var_name, var_value))

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
