#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


class Message(object):
    """站内消息"""

    def __init__(self, shanbay):
        self.shanbay = shanbay
        self._request = shanbay._request
        self.request = shanbay.request

    def send_message(self, recipient_list, subject, body):
        """发送站内消息

        :param recipient_list: 收件人列表
        :param subject: 标题
        :param body: 内容（不能超过 1024 个字符）
        """
        url = 'http://www.shanbay.com/message/compose/'
        recipient = ','.join(recipient_list)
        data = {
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'csrfmiddlewaretoken': self._request.cookies.get('csrftoken')
        }
        response = self.request(url, 'post', data=data)
        return response.url == 'http://www.shanbay.com/message/'

    def __call__(self, recipient_list, subject, body):
        """发送站内消息

        :param recipient_list: 收件人列表
        :param subject: 标题
        :param body: 内容（不能超过 1024 个字符）
        """
        return self.send_message(recipient_list, subject, body)
