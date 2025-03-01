import inspect
import logging
import os
import tempfile
import unittest
from logging.handlers import RotatingFileHandler

from happy_python.happy_log import HappyLogLevel

from happy_python import HappyLog


class TestHappyLog(unittest.TestCase):
    def setUp(self):
        print()
        self.log_dir = tempfile.TemporaryDirectory()
        self.test_ini = os.path.join(self.log_dir.name, 'test_log.ini')
        self._create_test_ini()

    def tearDown(self):
        self.log_dir.cleanup()

    def _create_test_ini(self):
        with open(self.test_ini, 'w') as f:
            f.write("""
    [loggers]
    keys=root

    [handlers]
    keys=consoleHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleFormatter
    args=(sys.stdout,)

    [formatter_simpleFormatter]
    format=%(asctime)s [%(levelname)s] %(message)s
    datefmt=%Y-%m-%d %H:%M:%S
    """)

    def test_singleton_instance(self):
        instance1 = HappyLog.get_instance()
        instance2 = HappyLog.get_instance()
        self.assertIs(instance1, instance2)

    def test_custom_config_instance(self):
        instance1 = HappyLog.get_instance(self.test_ini)
        instance2 = HappyLog.get_instance(self.test_ini)
        self.assertIs(instance1, instance2)

    def test_invalid_ini_path(self):
        with self.assertRaises(FileNotFoundError):
            HappyLog.get_instance('invalid_path.ini', is_new_instance=True)

    def test_log_level_settings(self):
        hlog = HappyLog.get_instance()

        for level in HappyLogLevel:
            hlog.set_level(level)
            self.assertEqual(hlog.logger.level, level.value)

    def test_handler_management(self):
        hlog = HappyLog.get_instance()
        initial_handlers = len(hlog.logger.handlers)
        self.assertEqual(3, initial_handlers)

        hlog.load_config()

        # 添加测试handler
        test_handler = RotatingFileHandler(os.path.join(self.log_dir.name, 'test.log'))
        hlog.logger.addHandler(test_handler)

        final_handlers = len(hlog.logger.handlers)

        self.assertEqual(2, final_handlers)

    def test_file_handler_creation(self):
        test_file = os.path.join(self.log_dir.name, 'test.log')
        hlog = HappyLog.get_instance()
        hlog.log_ini = ''  # 强制使用默认配置

        # 测试文件handler创建
        file_handler = logging.FileHandler(test_file)
        hlog.logger.addHandler(file_handler)
        hlog.logger.info('Test message')

        self.assertTrue(os.path.exists(test_file))
        self.assertGreater(os.path.getsize(test_file), 0)

    def test_invalid_log_level(self):
        hlog = HappyLog.get_instance()

        with self.assertRaises(ValueError):
            hlog.set_level(100)

    def test_trace_logging(self):
        hlog = HappyLog.get_instance()
        hlog.set_level(HappyLogLevel.TRACE)

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.logger.trace('Test trace message')

        self.assertIn('TRACE', cm.output[0])

    def assert_log(self, hlog: HappyLog, func, level: str):
        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            func('%s info' % level, 'message')

        self.assertEqual(cm.output, [('%s:root:%s info message' % (level.upper(), level))])

    def test_var(self):
        def assert_var_log(_hlog: HappyLog, func, var_name: str, var_value):
            with self.assertLogs(_hlog.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:var->%s=%s' % (var_name, var_value))])

        foo = 1

        hlog = HappyLog.get_instance()
        assert_var_log(hlog, hlog.var, 'foo', foo)

    def test_critical(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.critical, 'critical')

    def test_error(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.error, 'error')

    def test_warning(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.warning, 'warning')

    def test_info(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.info, 'info')

    def test_debug(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.debug, 'debug')

    def test_trace(self):
        hlog = HappyLog.get_instance()
        self.assert_log(hlog, hlog.trace, 'trace')

    def test_input(self):
        def assert_var_log(_hlog: HappyLog, func, var_name: str, var_value):
            with self.assertLogs(_hlog.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:input->%s=%s' % (var_name, var_value))])

        foo = 1

        hlog = HappyLog.get_instance()
        assert_var_log(hlog, hlog.input, 'foo', foo)

    def test_output(self):
        def assert_var_log(_hlog: HappyLog, func, var_name: str, var_value):
            with self.assertLogs(_hlog.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:output->%s=%s' % (var_name, var_value))])

        foo = 1
        hlog = HappyLog.get_instance()
        assert_var_log(hlog, hlog.output, 'foo', foo)

    def test_enter_func(self):
        func_name = inspect.stack()[0][3]
        hlog = HappyLog.get_instance()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.enter_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Enter function: test_enter_func'])

    def test_exit_func(self):
        func_name = inspect.stack()[0][3]
        hlog = HappyLog.get_instance()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.exit_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Exit function: test_exit_func'])

    def test_vardump(self):
        foo = 1
        hlog = HappyLog.get_instance()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.vardump(foo)

        self.assertEqual(cm.output, [('TRACE:root:var->%s=%s' % ('foo', foo))])

    def test_inputdump(self):
        foo = 1
        hlog = HappyLog.get_instance()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.inputdump(foo)

        self.assertEqual(cm.output, [('TRACE:root:input->%s=%s' % ('foo', foo))])

    def test_outputdump(self):
        foo = 1
        hlog = HappyLog.get_instance()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.outputdump(foo)

        self.assertEqual(cm.output, [('TRACE:root:output->%s=%s' % ('foo', foo))])