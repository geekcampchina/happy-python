import inspect
import logging
import os
import tempfile
import unittest
from logging.handlers import RotatingFileHandler

from happy_python import HappyLog
from happy_python.happy_log import HappyLogLevel, SingletonMeta, AsyncLogManager

class TestHappyLog(unittest.TestCase):
    def setUp(self):
        SingletonMeta._instances.clear()
        AsyncLogManager().set_async_enabled(False)
        self.log_dir = tempfile.TemporaryDirectory()
        self.test_ini = os.path.join(self.log_dir.name, 'test_log.ini')
        self._create_test_ini()

    def tearDown(self):
        self.log_dir.cleanup()

    def _create_test_ini(self):
        with open(self.test_ini, 'w') as f:
            f.write('''
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
''')

    def test_singleton_instance(self):
        instance1 = HappyLog()
        instance2 = HappyLog()
        self.assertIs(instance1, instance2)

    def test_custom_config_instance(self):
        instance1 = HappyLog(log_ini=self.test_ini, logger_name='root')
        instance2 = HappyLog(log_ini=self.test_ini, logger_name='root')
        self.assertIs(instance1, instance2)

    def test_invalid_ini_path(self):
        with self.assertRaises(FileNotFoundError):
            HappyLog(log_ini='invalid_path.ini', logger_name='root')

    def test_log_level_settings(self):
        hlog = HappyLog()

        for level in HappyLogLevel:
            hlog.set_level(level)
            self.assertEqual(hlog.logger.level, level.value)

    def test_handler_management(self):
        hlog = HappyLog()
        initial_handlers = len(hlog.logger.handlers)
        self.assertGreaterEqual(initial_handlers, 1)

        hlog.load_config()
        handlers_after_load = len(hlog.logger.handlers)

        test_handler = RotatingFileHandler(os.path.join(self.log_dir.name, 'test.log'))
        hlog.logger.addHandler(test_handler)
        final_handlers = len(hlog.logger.handlers)
        self.assertEqual(handlers_after_load + 1, final_handlers)

    def test_file_handler_creation(self):
        test_file = os.path.join(self.log_dir.name, 'test.log')
        hlog = HappyLog()
        hlog.log_ini = ''
        hlog.load_config()

        file_handler = logging.FileHandler(test_file)
        hlog.logger.addHandler(file_handler)
        hlog.logger.info('Test message')

        self.assertTrue(os.path.exists(test_file))
        self.assertGreater(os.path.getsize(test_file), 0)

    def test_invalid_log_level(self):
        hlog = HappyLog()

        with self.assertRaises(ValueError):
            hlog.set_level(100)

    def test_trace_logging(self):
        hlog = HappyLog()
        hlog.set_level(HappyLogLevel.TRACE)

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.logger.trace('Test trace message')

        self.assertIn('TRACE', cm.output[0])

    def assert_log(self, hlog, func, level):
        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            func('%s info' % level, 'message')

        expected = ['%s:root:%s info message' % (level.upper(), level)]
        self.assertEqual(cm.output, expected)

    def test_var(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.var('foo', foo)

        self.assertEqual(cm.output, ['TRACE:root:var->foo=1'])

    def test_critical(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.critical, 'critical')

    def test_error(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.error, 'error')

    def test_warning(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.warning, 'warning')

    def test_info(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.info, 'info')

    def test_debug(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.debug, 'debug')

    def test_trace(self):
        hlog = HappyLog()
        self.assert_log(hlog, hlog.trace, 'trace')

    def test_input(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.input('foo', foo)

        self.assertEqual(cm.output, ['TRACE:root:input->foo=1'])

    def test_output(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.output('foo', foo)

        self.assertEqual(cm.output, ['TRACE:root:output->foo=1'])

    def test_enter_func(self):
        func_name = inspect.stack()[0][3]
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.enter_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Enter function: %s' % func_name])

    def test_exit_func(self):
        func_name = inspect.stack()[0][3]
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.exit_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Exit function: %s' % func_name])

    def test_vardump(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.vardump(foo)

        self.assertEqual(cm.output, ['TRACE:root:var->foo=1'])

    def test_inputdump(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.inputdump(foo)

        self.assertEqual(cm.output, ['TRACE:root:input->foo=1'])

    def test_outputdump(self):
        foo = 1
        hlog = HappyLog()

        with self.assertLogs(hlog.logger, level='TRACE') as cm:
            hlog.outputdump(foo)

        self.assertEqual(cm.output, ['TRACE:root:output->foo=1'])

if __name__ == '__main__':
    unittest.main()
