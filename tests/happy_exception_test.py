#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from happy_utils import HappyPyException


class TestHappyPyException(unittest.TestCase):
    def test_hpe(self):
        try:
            raise HappyPyException('自定义错误')
        except HappyPyException as e:
            self.assertEqual('自定义错误', str(e))
