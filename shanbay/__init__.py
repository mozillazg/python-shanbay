#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

"""Python API for shanbay.com"""

__title__ = 'shanbay'
__version__ = '0.3.2'
__author__ = 'mozillazg'
__email__ = 'mozillazg101@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 mozillazg'

import datetime

import requests

from .exceptions import ShanbayException, AuthException, ConnectException
from .message import Message
from .team import Team
from .api import API

all = ['ShanbayException', 'AuthException', 'ConnectException',
       'Shanbay', 'Message', 'Team', 'API']


class Shanbay(object):
    """
    :param username: 用户名
    :param password: 密码

    ::

     >>> from shanbay import Shanbay
     >>> s = Shanbay('username', 'password')
     >>> s.login()
     True
    """
    USER_AGENT = 'python-shanbay/%s' % __version__

    def __init__(self, username, password):
        self._request = requests.Session()
        self.username = username
        self.password = password

    def _attr(self, name):
        return getattr(self.__class__, name)

    def request(self, url, method='get', **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('User-Agent', self._attr('USER_AGENT'))
        try:
            r = getattr(self._request, method)(url, **kwargs)
        except requests.exceptions.RequestException as e:
            raise ConnectException(e)
        if r.url.startswith('http://www.shanbay.com/accounts/login/'):
            raise AuthException('Need login')
        return r

    def login(self, **kwargs):
        """登录"""
        url = 'http://www.shanbay.com/accounts/login/'
        try:
            r = self._request.get(url, **kwargs)
        except requests.exceptions.RequestException as e:
            raise ConnectException(e)
        token = r.cookies.get('csrftoken')
        data = {
            'csrfmiddlewaretoken': token,
            'username': self.username,
            'password': self.password,
            'login': '',
            'continue': 'home',
            'u': 1,
            'next': '',
        }
        return self.request(url, 'post', data=data, **kwargs).ok

    def server_date_utc(self):
        """获取扇贝网服务器时间（UTC 时间）"""
        date_str = self.request('http://www.shanbay.com', 'head'
                                ).headers['date']
        date_utc = datetime.datetime.strptime(date_str,
                                              '%a, %d %b %Y %H:%M:%S GMT')
        return date_utc

    def server_date(self):
        """获取扇贝网服务器时间（北京时间）"""
        date_utc = self.server_date_utc()
        # 北京时间 = UTC + 8 hours
        return date_utc + datetime.timedelta(hours=8)
