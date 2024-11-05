import unittest

from happy_python import HappyPyException
from happy_python import callback_succeed_once

max_n = 6
current_n = 1


class TestUtils(unittest.TestCase):
    def test_callback_succeed_once(self):
        def foo(message):
            global current_n

            if message != 'hello':
                raise HappyPyException('callback_succeed_once参数测试')

            if current_n < max_n:
                current_n += 1
                raise HappyPyException('callback_succeed_once用于测试的异常')

            return current_n

        result = callback_succeed_once(foo, max_time=7, message='hello')
        self.assertEqual(result, 6)
