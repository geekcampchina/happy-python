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


class TestHappyConfigParser(unittest.TestCase):
    def setUp(self):
        from configparser import ConfigParser

        config = ConfigParser()
        config['foo_section'] = dict()
        config['foo_section']['example_name'] = 'abc'
        config['foo_section']['example_port'] = '5432'
        config['foo_section']['example_enable'] = 'True'

        with open('example.ini', 'w') as configfile:
            config.write(configfile)

    def tearDown(self):
        import os

        if os.path.exists('example.ini'):
            os.remove('example.ini')

    def test_load(self):
        foo_config = FooConfig()
        foo_config.section = 'foo_section'

        HappyConfigParser.load('example.ini', foo_config)

        self.assertEqual(foo_config.section, 'foo_section')
        self.assertEqual(foo_config.example_name, 'abc')
        self.assertEqual(foo_config.example_port, 5432)
        self.assertTrue(foo_config.example_enable)
