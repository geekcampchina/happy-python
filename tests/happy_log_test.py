import inspect
import logging
import unittest

from happy_python import HappyLog


class TestHappyLog(unittest.TestCase):
    hlog = None
    logger = None

    def setUp(self):
        self.hlog = HappyLog.get_instance()
        self.logger = self.hlog.get_logger()

    def tearDown(self):
        for handler in self.logger.root.handlers:
            if type(handler) is logging.handlers.RotatingFileHandler:
                # if os.path.exists(handler.baseFilename):
                #     os.remove(handler.baseFilename)

                handler.close()

            elif type(handler) is logging.FileHandler:
                # if os.path.exists(handler.baseFilename):
                #     os.remove(handler.baseFilename)

                handler.close()
            else:
                pass

    def assert_log(self, func, level: str):
        with self.assertLogs(self.logger, level='TRACE') as cm:
            func('%s info' % level, 'message')

        self.assertEqual(cm.output, [('%s:root:%s info message' % (level.upper(), level))])

    def test_var(self):
        def assert_var_log(func, var_name: str, var_value):
            with self.assertLogs(self.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:var->%s=%s' % (var_name, var_value))])

        foo = 1
        assert_var_log(self.hlog.var, 'foo', foo)

    def test_critical(self):
        self.assert_log(self.hlog.critical, 'critical')

    def test_error(self):
        self.assert_log(self.hlog.error, 'error')

    def test_warning(self):
        self.assert_log(self.hlog.warning, 'warning')

    def test_info(self):
        self.assert_log(self.hlog.info, 'info')

    def test_debug(self):
        self.assert_log(self.hlog.debug, 'debug')

    def test_trace(self):
        self.assert_log(self.hlog.trace, 'trace')

    def test_input(self):
        def assert_var_log(func, var_name: str, var_value):
            with self.assertLogs(self.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:input->%s=%s' % (var_name, var_value))])

        foo = 1
        assert_var_log(self.hlog.input, 'foo', foo)

    def test_output(self):
        def assert_var_log(func, var_name: str, var_value):
            with self.assertLogs(self.logger, level='TRACE') as cm:
                func(var_name, var_value)

            self.assertEqual(cm.output, [('TRACE:root:output->%s=%s' % (var_name, var_value))])

        foo = 1
        assert_var_log(self.hlog.output, 'foo', foo)

    def test_enter_func(self):
        func_name = inspect.stack()[0][3]

        with self.assertLogs(self.logger, level='TRACE') as cm:
            self.hlog.enter_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Enter function: test_enter_func'])

    def test_exit_func(self):
        func_name = inspect.stack()[0][3]

        with self.assertLogs(self.logger, level='TRACE') as cm:
            self.hlog.exit_func(func_name)

        self.assertEqual(cm.output, ['TRACE:root:Exit function: test_exit_func'])

    def test_vardump(self):
        foo = 1

        with self.assertLogs(self.logger, level='TRACE') as cm:
            self.hlog.vardump(foo)

        self.assertEqual(cm.output, [('TRACE:root:var->%s=%s' % ('foo', foo))])

    def test_inputdump(self):
        foo = 1

        with self.assertLogs(self.logger, level='TRACE') as cm:
            self.hlog.inputdump(foo)

        self.assertEqual(cm.output, [('TRACE:root:input->%s=%s' % ('foo', foo))])

    def test_outputdump(self):
        foo = 1

        with self.assertLogs(self.logger, level='TRACE') as cm:
            self.hlog.outputdump(foo)

        self.assertEqual(cm.output, [('TRACE:root:output->%s=%s' % ('foo', foo))])