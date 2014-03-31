#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shanbay import ShanbayException, AuthException, ServerException, Shanbay


def test_login():
    s = Shanbay('root', 'root')
    s.login()

    try:
        Shanbay('rxxxoot', 'axxbcd').login()
    except AuthException:
        pass

    try:
        proxies = {
            "http": "http://10.10.1.10:3128",
            "https": "http://10.10.1.10:1080",
        }
        Shanbay('rooxxt', 'abcxx').login(proxies=proxies, timeout=3)
    except ServerException:
        pass
