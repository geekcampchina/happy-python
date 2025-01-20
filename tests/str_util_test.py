import unittest

from happy_python import bytearray_to_str, gen_random_str, to_hex_str1, is_ascii_str, to_hex_str2, \
    from_hex_str, is_printable_ascii_str
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

    def test_random_str(self):
        result = gen_random_str(11)
        self.assertEqual(11, len(result))

    def test_to_hex_str1(self):
        self.assertEqual(to_hex_str1('abcde'), '6162636465')
        self.assertEqual(to_hex_str1('abcde', True, ' '), '61 62 63 64 65')

    def test_to_hex_str2(self):
        self.assertEqual(to_hex_str2('abcde'.encode('utf-8')), '6162636465')
        self.assertEqual(to_hex_str2('Hello World'.encode('utf-8')), '48656C6C6F20576F726C64')

        self.assertEqual(to_hex_str2('abcde'.encode('utf-8'), True, ' '), '61 62 63 64 65')
        self.assertEqual(to_hex_str2(
            'Hello World'.encode('utf-8'), True, ' '), '48 65 6C 6C 6F 20 57 6F 72 6C 64')

    def test_is_ascii_str(self):
        self.assertTrue(is_ascii_str('ab123--'))
        self.assertFalse(is_ascii_str('测试'))

    def test_is_printable_ascii_str(self):
        self.assertFalse(is_printable_ascii_str('A\n'))
        self.assertTrue(is_printable_ascii_str('ab123--'))
        self.assertFalse(is_printable_ascii_str('测试'))

    def test_from_hex_str(self):
        self.assertEqual(from_hex_str('0x0E0x0A'), b'\x0e\n')
        self.assertEqual(from_hex_str('0E 0A', ' '), b'\x0e\n')
