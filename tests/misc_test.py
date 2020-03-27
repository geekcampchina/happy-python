#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import tempfile
import unittest
from pathlib import PurePath
from time import sleep
from happy_python import get_exit_status_of_cmd
from happy_python import get_exit_code_of_cmd
from happy_python import get_output_of_cmd
from happy_python import non_blocking_exe_cmd
from happy_python import exe_cmd_and_poll_output
from happy_python import callback_succeed_once
from happy_python import HappyPyException

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
