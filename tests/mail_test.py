#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from happy_python import EmailAddr, HappyEmail


class TestUtils(unittest.TestCase):
    def test_happy_email(self):
        he = HappyEmail(stmp_server=('smtp.qq.com', '465'),
                        stmp_auth=('10000@qq.com', '123456'),
                        recipients=[EmailAddr('收件人1名称', 'admin@foo.com>'),
                                    EmailAddr('收件人2名称', 'admin2@foo.com>')],
                        sender=EmailAddr('发件人名称', 'user@bar.com'),
                        subject='测试邮件',
                        body='邮件正文',
                        files=[])
        self.assertTrue(he.send_mail(enable_mock=True))
