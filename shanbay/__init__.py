#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python API for shanbay.com"""

__title__ = 'shanbay'
__version__ = '0.1.0'
__author__ = 'mozillazg'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 mozillazg'

from functools import wraps
from urllib2 import quote

import requests


class ShanbayException(Exception):
    pass


class AuthException(ShanbayException):
    """未登录或登录已过期"""
    pass


class APIServerException(ShanbayException):
    """扇贝网 API 服务出现异常情况"""
    pass


class Shanbay(object):
    USER_AGENT = 'python-shanbay/%s' % __version__

    def __init__(self, username, password):
        self.request = requests.Session()
        self.username = username
        self.password = password

    def _attr(self, name):
        return getattr(self.__class__, name)

    def _request(self, url, method, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('User-Agent', self._attr('USER_AGENT'))
        try:
            return getattr(self.request, method)(url, **kwargs)
        except requests.RequestException:
            raise APIServerException

    def login(self, **kwargs):
        url = 'http://www.shanbay.com/accounts/login/'
        r = self._request(url, 'get', **kwargs)
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
        r = self._request(url, 'post', data=data)
        if r.url == 'http://www.shanbay.com/accounts/login/':
            raise AuthException

    def _api_wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            url, method, self = func(*args, **kwargs)
            r = self._request(url, method, allow_redirects=False, **kwargs)
            if r.url == 'http://www.shanbay.com/accounts/login/':
                raise AuthException
            try:
                return r.json()
            except:
                raise APIServerException
        return _wrapper

    @_api_wrapper
    def user_info(self, **kwargs):
        url = 'http://www.shanbay.com/api/user/info/'
        return url, 'get', self

    @_api_wrapper
    def query_word(self, word, **kwargs):
        url = 'http://www.shanbay.com/api/word/%s' % quote(word)
        return url, 'get', self

    @_api_wrapper
    def add_word(self, word, **kwargs):
        url = 'http://www.shanbay.com/api/learning/add/%s' % word
        return url, 'get', self

    @_api_wrapper
    def examples(self, learn_id, **kwargs):
        url = 'http://www.shanbay.com/api/learning/examples/%s'
        url = url % learn_id
        return url, 'get', self._request

    @_api_wrapper
    def add_example(self, learn_id, question, answer, **kwargs):
        url = 'http://www.shanbay.com/api/example/add/%s?sentence=%s&translation=%s'
        url = url % (learn_id, question, answer)
        return url, 'get', self

    @_api_wrapper
    def add_note(self, learn_id, note, **kwargs):
        url = 'http://www.shanbay.com/api/note/add/%s?note=%s'
        url = url % (learn_id, quote(note))
        return url, 'get', self
