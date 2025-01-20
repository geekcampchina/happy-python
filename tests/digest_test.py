import unittest

from happy_python import gen_md5_32_hexdigest, sign_sha1_digest, sign_sha224_digest, sign_sha256_digest, \
    sign_sha384_digest, sign_sha512_digest
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

    def test_sign_sha1_digest(self):
        result = sign_sha1_digest('123456', 'abc', is_base64=False)
        size = 40

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'f1ae6a48d467345aa63e72a8cbd8baba92417ce5')

        result = sign_sha1_digest('123456', 'abc', is_base64=True)
        size = 28

        self.assertEqual(len(result), size)
        self.assertEqual(result, '8a5qSNRnNFqmPnKoy9i6upJBfOU=')

    def test_sign_sha224_digest(self):
        result = sign_sha224_digest('123456', 'abc', is_base64=False)
        size = 56

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'a1083990356121fb87ecfb5c8204792ffb2b94be951714c771fcd2c7')

        result = sign_sha224_digest('123456', 'abc', is_base64=True)
        size = 40

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'oQg5kDVhIfuH7PtcggR5L/srlL6VFxTHcfzSxw==')

    def test_sign_sha256_digest(self):
        result = sign_sha256_digest('123456', 'abc', is_base64=False)
        size = 64

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'f6ced6f4883ffc0981a6b9945819f680102b43097ad8ef7a0df9bde06fb3d2e4')

        result = sign_sha256_digest('123456', 'abc', is_base64=True)
        size = 44

        self.assertEqual(len(result), size)
        self.assertEqual(result, '9s7W9Ig//AmBprmUWBn2gBArQwl62O96Dfm94G+z0uQ=')

    def test_sign_sha384_digest(self):
        result = sign_sha384_digest('123456', 'abc', is_base64=False)
        size = 96

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'bd31dbd1073ceca7cb43c96a7cbd02e1df33e6ce276601bdc6178ba8e20b1832'
                                 '3b29422de92a9180932ef8f49a4873fe')

        result = sign_sha384_digest('123456', 'abc', is_base64=True)
        size = 64

        self.assertEqual(len(result), size)
        self.assertEqual(result, 'vTHb0Qc87KfLQ8lqfL0C4d8z5s4nZgG9xheLqOILGDI7KUIt6SqRgJMu+PSaSHP+')

    def test_sign_sha512_digest(self):
        result = sign_sha512_digest('123456', 'abc', is_base64=False)
        size = 128

        self.assertEqual(len(result), size)
        self.assertEqual(result,
                         '7842485b1a55745a9823c3e155986ec9bde5b140691678c5d202a4e1f4664f130ac4fc4dc7'
                         '5c8a51d47b9a8fb43bdcf30652143da696fe79407032ce48aba2f8')

        result = sign_sha512_digest('123456', 'abc', is_base64=True)
        size = 88

        self.assertEqual(len(result), size)
        self.assertEqual(result,
                         'eEJIWxpVdFqYI8PhVZhuyb3lsUBpFnjF0gKk4fRmTxMKxPxNx1yKUdR7mo+0O9zzBlIUPaaW/nlAcDLOSKui+A==')
