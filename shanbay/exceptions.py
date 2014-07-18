#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


class ShanbayException(Exception):
    """异常基类"""
    pass


class AuthException(ShanbayException):
    """未登录或登录已过期"""
    pass


class ConnectException(ShanbayException):
    """网络连接出现异常情况"""
    pass
