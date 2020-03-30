#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from happy_python import HappyConfigBase
from happy_python import HappyConfigParser


class FooConfig(HappyConfigBase):
    """
    配置文件模板
    """
    def __init__(self):
        super().__init__()

        self.section = 'main'
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
        config['foo_section']['example_name'] = 'abc'
        config['foo_section']['example_port'] = '5432'
        config['foo_section']['example_enable'] = 'True'
        config['foo_section']['example_list'] = 'a,b,c,d'
        config['foo_section']['example_var'] = '/var/${log_dirname}'

        with open('example.ini', 'w') as configfile:
            config.write(configfile)

    def test_load(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load('example.ini', foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
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
            self.assertEqual(foo_config.example_name, 'abc')
            self.assertEqual(foo_config.example_port, 5432)
            self.assertTrue(foo_config.example_enable)
            self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])

    def test_load_with_var(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load_with_var('example.ini', {'log_dirname': 'log'}, foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
        self.assertEqual(foo_config.example_name, 'abc')
        self.assertEqual(foo_config.example_port, 5432)
        self.assertTrue(foo_config.example_enable)
        self.assertEqual(foo_config.example_list, ['a', 'b', 'c', 'd'])
        self.assertEqual(foo_config.example_var, '/var/log')

    def tearDown(self):
        import os

        if os.path.exists('example.ini'):
            os.remove('example.ini')