#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class HappyPyException(Exception):
    def __init__(self, err='Happy Python Error'):
        Exception.__init__(self, err)
