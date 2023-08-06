import unittest

from happy_python import HappyConfigBase
from happy_python import HappyConfigParser


class FooConfig(HappyConfigBase):
    def __init__(self):
        super().__init__()

        self.section = 'main'
        self.format = ''
        self.example_name = ''
        self.example_port = 0
        self.example_enable = True
        self.example_list = list()
        self.example_var = ''


class TestHappyConfigParser(unittest.TestCase):
    def setUp(self):
        from configparser import ConfigParser

        config = ConfigParser()
        config['foo_section'] = dict()
        config['foo_section']['format'] = '%(asctime)s %(process)s [%(levelname)s] %(message)s'
        config['foo_section']['example_name'] = 'abc'
        config['foo_section']['example_port'] = '5432'
        config['foo_section']['example_enable'] = 'True'
        config['foo_section']['example_list'] = 'a,b,c,d'
        config['foo_section']['example_var'] = '/var/${log_dirname}'
        config['foo_section']['!url.foo'] = 'https://www.foo.com'
        config['foo_section']['!url.foo.status'] = '200'
        config['foo_section']['!url.foo.status.message'] = 'OK'
        config['foo_section']['!url.bar'] = 'https://www.bar.com'
        config['foo_section']['!url.bar.status'] = '200'
        config['foo_section']['!url.bar.status.message'] = 'OK'

        with open('example.ini', 'w') as configfile:
            config.write(configfile)

    def test_load(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load('example.ini', foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
        self.assertEqual(foo_config.format, '%(asctime)s %(process)s [%(levelname)s] %(message)s')
        self.assertEqual(foo_config.example_name, 'abc')
        self.assertEqual(foo_config.example_port, 5432)
        self.assertTrue(foo_config.example_enable)
        self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])

    def test_loads(self):
        with open('example.ini') as f:
            foo_config = FooConfig()
            foo_config.section = 'foo_section'
            content = ''.join(f.readlines())
            HappyConfigParser._loads(content, foo_config)

            self.assertEqual(foo_config.section, 'foo_section')
            self.assertEqual(foo_config.format, '%(asctime)s %(process)s [%(levelname)s] %(message)s')
            self.assertEqual(foo_config.example_name, 'abc')
            self.assertEqual(foo_config.example_port, 5432)
            self.assertTrue(foo_config.example_enable)
            self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])

    def test_load_with_var(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load_with_var('example.ini', {'log_dirname': 'log'}, foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
        self.assertEqual(foo_config.format, '%(asctime)s %(process)s [%(levelname)s] %(message)s')
        self.assertEqual(foo_config.example_name, 'abc')
        self.assertEqual(foo_config.example_port, 5432)
        self.assertTrue(foo_config.example_enable)
        self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])
        self.assertEqual(foo_config.example_var, '/var/log')

    def test_load_with_xlist(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load('example.ini', foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
        self.assertEqual(foo_config.format, '%(asctime)s %(process)s [%(levelname)s] %(message)s')
        self.assertEqual(foo_config.example_name, 'abc')
        self.assertEqual(foo_config.example_port, 5432)
        self.assertTrue(foo_config.example_enable)
        self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])

        item = foo_config.xlist_key('url')
        self.assertEqual(item, ['url.foo', 'url.bar'])

        self.assertEqual(foo_config.xlist_get(prefix=item[0]), 'https://www.foo.com')
        self.assertEqual(foo_config.xlist_get(prefix=item[0], key='status'), '200')
        self.assertEqual(foo_config.xlist_get(prefix=item[0], key='status.message'), 'OK')

        self.assertEqual(foo_config.xlist_get(prefix=item[1]), 'https://www.bar.com')
        self.assertEqual(foo_config.xlist_get(prefix=item[1], key='status'), '200')
        self.assertEqual(foo_config.xlist_get(prefix=item[1], key='status.message'), 'OK')

        self.assertIsNone(foo_config.xlist_get(prefix='url'))
        self.assertIsNone(foo_config.xlist_get(prefix='url.foo', key='status1'))
        self.assertIsNone(foo_config.xlist_get(prefix='url.foo', key='status1.message'))

    def tearDown(self):
        import os

        if os.path.exists('example.ini'):
            os.remove('example.ini')
