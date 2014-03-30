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


class ServerException(ShanbayException):
    """扇贝网服务出现异常情况"""
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
            raise ServerException

    def _response(self, url, method, mode='json', **kwargs):
        r = self._request(url, method, **kwargs)
        if r.url.startswith('http://www.shanbay.com/accounts/login/'):
            raise AuthException
        try:
            if mode == 'json':
                return r.json()
            elif mode == 'text':
                return r.text
            else:
                return r.content
        except:
            raise ServerException

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
        self._response(url, 'post', mode='text', data=data)

    @property
    def api(self):
        return API(self)


class API(object):
    def __init__(self, shanbay):
        self.shanbay = shanbay

    def user_info(self, **kwargs):
        url = 'http://www.shanbay.com/api/user/info/'
        return self.shanbay._response(url, 'get')

    def query_word(self, word, **kwargs):
        url = 'http://www.shanbay.com/api/word/%s' % quote(word)
        return self.shanbay._response(url, 'get')

    def add_word(self, word, **kwargs):
        url = 'http://www.shanbay.com/api/learning/add/%s' % word
        return self.shanbay._response(url, 'get')

    def examples(self, learn_id, **kwargs):
        url = 'http://www.shanbay.com/api/learning/examples/%s'
        url = url % learn_id
        return self.shanbay._response(url, 'get')

    def add_example(self, learn_id, question, answer, **kwargs):
        url = 'http://www.shanbay.com/api/example/add/%s?sentence=%s&translation=%s'
        url = url % (learn_id, question, answer)
        return self.shanbay._response(url, 'get')

    def add_note(self, learn_id, note, **kwargs):
        url = 'http://www.shanbay.com/api/note/add/%s?note=%s'
        url = url % (learn_id, quote(note))
        return self.shanbay._response(url, 'get')
