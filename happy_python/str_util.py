import json
import random
import string


def bytes_to_str(b: bytes, encoding='UTF-8'):
    return str(b, encoding=encoding)


def bytearray_to_str(b: bytearray, encoding='UTF-8'):
    return str(b, encoding=encoding)


def str_to_dict(value: str):
    return json.loads(value)


def dict_to_str(value: dict, indent=None):
    return json.dumps(value, ensure_ascii=False, indent=indent)


def gen_random_str(str_len: int = 10) -> str:
    """
    生成随机字符串，默认长度10
    :param str_len:
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=str_len))


def to_hex_str1(s: str, is_upper: bool = True, delimiter='') -> str:
    """
    将字符串转换为十六进制表示的字符串
    :param is_upper: 是否大写
    :param delimiter: 分隔符
    :param s:
    :return:
    """
    if is_upper:
        return s.encode('utf-8').hex(delimiter).upper() if delimiter else s.encode('utf-8').hex().upper()

    return s.encode('utf-8').hex(delimiter) if delimiter else s.encode('utf-8').hex()


def to_hex_str2(bb: bytes, is_upper: bool = True, delimiter='') -> str:
    """
    将bytes转换为十六进制表示的字符串
    :param is_upper: 是否大写
    :param delimiter: 分隔符
    :param bb:
    :return:
    """
    if is_upper:
        return bb.hex(delimiter).upper() if delimiter else bb.hex().upper()

    return bb.hex(delimiter) if delimiter else bb.hex()


def from_hex_str(s: str, delimiter: str = '0x') -> bytes:
    """
    将十六进制表示的字符串转为bytes。比如 0x0E0x0A0x5D。
    :param s: 十六进制表示的字符串，可以带分隔符。比如 0E 0A
    :param delimiter: 分隔符
    :return:
    """
    _s = s

    # 删除分隔符
    if delimiter:
        _s = _s.replace(delimiter, '')

    return bytes.fromhex(_s)


def is_ascii_str(s):
    """
    判断是否是ASCII字符串
    :param s:
    :return:
    """
    return all(ord(c) < 128 for c in s)


def is_printable_ascii_str(s):
    """
    判断是否是可见ASCII字符组成的字符串
    :param s:
    :return:
    """
    return all(32 <= ord(c) <= 127 for c in s)
