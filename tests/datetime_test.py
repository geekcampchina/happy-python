#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from happy_python import str_to_datetime
from happy_python import datetime_to_str
from happy_python import get_current_datetime
from happy_python import get_current_datetime2
from happy_python import get_current_timestamp


class TestUtils(unittest.TestCase):
    def test_str_to_datetime(self):
        dt = str_to_datetime('2020-04-19 20:04:14')

        self.assertEqual(2020, dt.year)
        self.assertEqual(4, dt.month)
        self.assertEqual(19, dt.day)
        self.assertEqual(20, dt.hour)
        self.assertEqual(4, dt.minute)
        self.assertEqual(14, dt.second)

    def test_datetime_to_str(self):
        dts_src = '2020-04-19 20:04:14'
        dt = str_to_datetime(dts_src)
        dts_dst = datetime_to_str(dt)

        self.assertEqual(dts_src, dts_dst)
