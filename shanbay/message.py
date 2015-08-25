#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import re


class Message(object):
    """站内消息

    :param shanbay: :class:`~shanbay.Shanbay` 实例对象

    ::

     >>> from shanbay import Shanbay, Message
     >>> s = Shanbay('username', 'password')
     >>> s.login()
     >>> m = Message(s)
    """

    def __init__(self, shanbay):
        """ ::

            from shanbay import Shanbay, Message
            s = Shanbay('username', 'password')
            s.login()
            m = Message(s)
        """
        self.shanbay = shanbay
        self._request = shanbay._request
        self.request = shanbay.request

    def send_message(self, recipient_list, subject, body):
        """发送站内消息

        :param recipient_list: 收件人列表
        :param subject: 标题
        :param body: 内容（不能超过 1024 个字符）
        """
        url = 'http://www.shanbay.com/api/v1/message/'
        recipient = ','.join(recipient_list)
        data = {
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'csrfmiddlewaretoken': self._request.cookies.get('csrftoken')
        }
        response = self.request(url, 'post', data=data)
        return response.ok

    def reply_message(self, message_url, body):
        """回复某条站内消息

        :param message_url: 该条消息的页面 URL
        :param body: 内容（不能超过 1024 个字符）
        """
        id = re.findall(r'(\d+)/?$', message_url)[0]
        api = 'http://www.shanbay.com/api/v1/message/%s/reply/'
        url = api % id
        data = {
            'body': body
        }
        response = self.request(url, 'post', data=data)
        return response.json()['status_code'] == 0
