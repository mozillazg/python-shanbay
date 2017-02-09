#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

"""Python API for shanbay.com"""

import datetime

import requests

from .exceptions import ShanbayException, AuthException, ConnectException  # noqa
from .message import Message  # noqa
from .team import Team  # noqa
from .api import API  # noqa

__title__ = 'shanbay'
__version__ = '0.3.6'
__author__ = 'mozillazg'
__email__ = 'mozillazg101@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2016 mozillazg'

__all__ = ['ShanbayException', 'AuthException', 'ConnectException',
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
        self.csrftoken = ''

    def _attr(self, name):
        return getattr(self.__class__, name)

    def request(self, url, method='get', **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('User-Agent', self._attr('USER_AGENT'))
        headers.setdefault('X-CSRFToken', self.csrftoken)
        headers.setdefault('X-Requested-With', 'XMLHttpRequest')
        try:
            r = getattr(self._request, method)(url, **kwargs)
        except requests.exceptions.RequestException as e:
            raise ConnectException(e)
        self.csrftoken = r.cookies.get('csrftoken', '')

        content_type = r.headers.get('Content-Type', '')
        if r.url.endswith('/accounts/login/') or \
            (content_type.startswith('application/json') and
                r.json()['status_code'] == 401):
            raise AuthException('Need login')
        return r

    def login(self, **kwargs):
        """登录"""
        payload = {
            'username': self.username,
            'password': self.password,
        }
        headers = kwargs.setdefault('headers', {})
        headers.setdefault(
            'Referer',
            'https://www.shanbay.com/web/account/login'
        )
        url = 'https://www.shanbay.com/api/v1/account/login/web/'
        response = self.request(url, 'put', json=payload, **kwargs)
        r_json = response.json()
        return r_json['status_code'] == 0

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
