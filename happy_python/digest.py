"""
消息摘要算法相关代码
"""
import base64
import hashlib
import hmac


def gen_md5_32_hexdigest(s):
    """
    # 获取字符串的MD5值
    :param s:
    :return:
    """

    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def gen_sha1_hexdigest(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def gen_sha512_hexdigest(s):
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def _sign_shax_digest(algorithm, secret: str, s: str, is_base64=False):
    """
    签名字符串

    :param algorithm: 签名算法
    :param secret: 密码
    :param s: 输入字符串
    :param is_base64: 是否输出Base64
    :return:
    """
    hashed = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), algorithm)

    if is_base64:
        return base64.b64encode(hashed.digest()).decode().rstrip('\n')
    else:
        return hashed.hexdigest()


def sign_sha1_digest(secret, s, is_base64=False):
    return _sign_shax_digest(hashlib.sha1, secret, s, is_base64)


def sign_sha224_digest(secret, s, is_base64=False):
    return _sign_shax_digest(hashlib.sha224, secret, s, is_base64)


def sign_sha256_digest(secret, s, is_base64=False):
    return _sign_shax_digest(hashlib.sha256, secret, s, is_base64)


def sign_sha384_digest(secret, s, is_base64=False):
    return _sign_shax_digest(hashlib.sha384, secret, s, is_base64)


def sign_sha512_digest(secret, s, is_base64=False):
    return _sign_shax_digest(hashlib.sha512, secret, s, is_base64)
