import re
import unittest

from happy_python import get_current_datetime
from happy_python import get_current_timestamp
from happy_python import str_to_datetime, HappyDatetimeFormat


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
        dt_str = '2020-04-19 20:04:14'
        dt = str_to_datetime(dt_str)

        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 19)
        self.assertEqual(dt.hour, 20)
        self.assertEqual(dt.minute, 4)
        self.assertEqual(dt.second, 14)

    def test_get_current_datetime(self):
        value = get_current_datetime(HappyDatetimeFormat.Ymd_HMS)
        result = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', value)
        self.assertTrue(result)

        value = get_current_datetime(HappyDatetimeFormat.Y_m_d_H_M_S)
        result = re.match(r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}', value)
        self.assertTrue(result)

        value = get_current_datetime(HappyDatetimeFormat.YmdHMS)
        result = re.match(r'\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}', value)
        self.assertTrue(result)

        value = get_current_datetime(HappyDatetimeFormat.Ymd)
        result = re.match(r'\d{4}\d{2}\d{2}', value)
        self.assertTrue(result)

        value = get_current_datetime(HappyDatetimeFormat.HMS)
        result = re.match(r'\d{2}\d{2}\d{2}', value)
        self.assertTrue(result)

    def test_get_current_timestamp(self):
        value = get_current_timestamp()

        self.assertTrue(type(value) == float)
