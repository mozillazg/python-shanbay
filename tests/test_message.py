#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shanbay import Shanbay

s = Shanbay('root', 'root')
s.login()
message = s.message


def test_send_message():
    assert message.send_message(['mozillazg'], 'test_send_message',
                                'test_send_message')
