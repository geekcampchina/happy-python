#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def bytes_to_str(b: bytes, encoding='UTF-8'):
    return str(b, encoding=encoding)


def bytearray_to_str(b: bytearray, encoding='UTF-8'):
    return str(b, encoding=encoding)


def str_to_dict(value: str):
    return json.loads(value)


def dict_to_str(value: dict, indent=None):
    return json.dumps(value, ensure_ascii=False, indent=indent)
