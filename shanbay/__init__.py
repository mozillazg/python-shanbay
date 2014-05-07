#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python API for shanbay.com"""

__title__ = 'shanbay'
__version__ = '0.1.1.dev'
__author__ = 'mozillazg'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 mozillazg'

import requests

from .api import API

all = ['ShanbayException', 'AuthException', 'ServerException', 'Shanbay']


class ShanbayException(Exception):
    pass


class AuthException(ShanbayException):
    """未登录或登录已过期"""
    pass


class ConnectException(ShanbayException):
    """网络连接出现异常情况"""
    pass


class Shanbay(object):
    USER_AGENT = 'python-shanbay/%s' % __version__

    def __init__(self, username, password):
        self._request = requests.Session()
        self.username = username
        self.password = password

    def _attr(self, name):
        return getattr(self.__class__, name)

    def request(self, url, method, **kwargs):
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
        self.request(url, 'post', data=data)

    @property
    def api(self):
        return API(self)
