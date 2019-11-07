#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from happy_python import gen_md5_32_hexdigest
from happy_python import gen_sha1_hexdigest
from happy_python import gen_sha512_hexdigest


class TestUtils(unittest.TestCase):
    def test_gen_md5_32_hexdigest(self):
        hex_digest = gen_md5_32_hexdigest('abc')
        size = 32

        self.assertEqual(len(hex_digest), size)
        self.assertEqual(hex_digest, '900150983cd24fb0d6963f7d28e17f72')

    def test_gen_sha1_hexdigest(self):
        hex_digest = gen_sha1_hexdigest('abc')
        size = 40

        self.assertEqual(len(hex_digest), size)
        self.assertEqual(hex_digest, 'a9993e364706816aba3e25717850c26c9cd0d89d')

    def test_gen_sha512_hexdigest(self):
        hex_digest = gen_sha512_hexdigest('abc')
        size = 128

        self.assertEqual(len(hex_digest), size)
        self.assertEqual(hex_digest,
                         'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a'
                         '2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f')
