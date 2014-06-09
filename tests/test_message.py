#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shanbay import Shanbay, Message

s = Shanbay('root', 'root')
s.login()
message = Message(s)


def test_send_message():
    assert message.send_message(['mozillazg'], 'test_send_message',
                                'test_send_message')


def test_reply_message():
    url = 'http://www.shanbay.com/message/thread/2687980/'
    assert message.reply_message(url, 'test_reply_message')
