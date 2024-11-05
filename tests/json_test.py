import unittest

from happy_python import dict_to_pretty_json


class TestUtils(unittest.TestCase):
    def test_dict_to_pretty_json(self):
        s = dict_to_pretty_json({'name': 'happy-python', 'version': '1', 'cjk': '测试'}, indent=4)

        expect_value = '{\n    "cjk": "测试",\n    "name": "happy-python",\n    "version": "1"\n}'
        self.assertEqual(expect_value, s)
