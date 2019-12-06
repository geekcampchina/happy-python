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


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = str(PurePath(tempfile.gettempdir()) / 'foo')

        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_get_exit_code_of_cmd(self):
        result = get_exit_code_of_cmd('exit 0')
        self.assertEqual(result, 0)

        result = get_exit_code_of_cmd('exit 1')
        self.assertEqual(result, 1)

    def test_get_exit_status_of_cmd(self):
        result = get_exit_status_of_cmd('exit 0')
        self.assertTrue(result)

        result = get_exit_status_of_cmd('exit 1')
        self.assertFalse(result)

    def test_get_output_of_cmd(self):
        line_sep = os.linesep

        result = get_output_of_cmd('echo foo')
        self.assertEqual(result, 'foo' + line_sep)

        result = get_output_of_cmd('echo bar')
        self.assertEqual(result, 'bar' + line_sep)

        result = get_output_of_cmd('echo foo', remove_white_char=True)
        self.assertEqual(result, 'foo')

    def test_non_blocking_exe_cmd(self):
        non_blocking_exe_cmd('mkdir ' + self.test_dir)
        sleep(1)
        self.assertTrue(os.path.exists(self.test_dir))

    def tearDown(self) -> None:
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
