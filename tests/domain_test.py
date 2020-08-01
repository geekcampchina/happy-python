#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from happy_python import to_domain_obj


class TestUtils(unittest.TestCase):
    def test_DomainHandler(self):
        domain = to_domain_obj('foobar.com')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, 'foobar')
        self.assertEqual(domain.feild_top_level_domains, ['.com'])
        self.assertEqual(domain.feild_hosts, [])

        domain = to_domain_obj('www.foobar.com')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, 'foobar')
        self.assertEqual(domain.feild_top_level_domains, ['.com'])
        self.assertEqual(domain.feild_hosts, ['www'])

        domain = to_domain_obj('foobar.com.cn')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, 'foobar')
        self.assertEqual(domain.feild_top_level_domains, ['.com', '.cn'])
        self.assertEqual(domain.feild_hosts, [])

        domain = to_domain_obj('www.foobar.com.cn')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, 'foobar')
        self.assertEqual(domain.feild_top_level_domains, ['.com', '.cn'])
        self.assertEqual(domain.feild_hosts, ['www'])

        domain = to_domain_obj('www.test.foobar.com.cn')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, 'foobar')
        self.assertEqual(domain.feild_top_level_domains, ['.com', '.cn'])
        self.assertEqual(domain.feild_hosts, ['www', 'test'])

        domain = to_domain_obj('时尚.中国')
        self.assertIsNotNone(domain)
        self.assertEqual(domain.feild_domain_name, '时尚')
        self.assertEqual(domain.feild_top_level_domains, ['.中国'])
        self.assertEqual(domain.feild_hosts, [])

        tmp_domain = to_domain_obj('www.foobar.1com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('foobar.foobar')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('.foobar.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('-.foobar.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('baz-.foobar.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('-baz.foobar.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('%.foobar.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('f.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('foobar%.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('foobar.baz')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('aekui5phea2Eeyeelaijiex5ahniefaitied5Cohpei1Yoh6chaingohwie9pao123.com')
        self.assertIsNone(tmp_domain)

        tmp_domain = to_domain_obj('aekui5phea2Eeyeelaijiex5ahniefaitied5Cohpei1Yoh6chaingohwie9pao.'
                                   'aekui5phea2Eeyeelaijiex5ahniefaitied5Cohpei1Yoh6chaingohwie9pao.'
                                   'aekui5phea2Eeyeelaijiex5ahniefaitied5Cohpei1Yoh6chaingohwie9pao.'
                                   'aekui5phea2Eeyeelaijiex5ahniefaitied5Cohpei1Yoh6chaingohwie9pao.com')
        self.assertIsNone(tmp_domain)
