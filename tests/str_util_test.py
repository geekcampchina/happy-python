#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from happy_python import bytearray_to_str
from happy_python import bytes_to_str
from happy_python import dict_to_str
from happy_python import str_to_dict


class TestUtils(unittest.TestCase):
    def test_bytes_to_str(self):
        result = bytes_to_str(b'test')
        self.assertEqual(result, 'test')

    def test_bytearray_to_str(self):
        result = bytearray_to_str(bytearray(b'test'))
        self.assertEqual(result, 'test')

    def test_str_to_dict(self):
        result = str_to_dict('{"code": 1}')
        self.assertEqual(result, {"code": 1})

    def test_dict_to_str(self):
        result = dict_to_str({"code": 1})
        self.assertEqual(result, '{"code": 1}')
