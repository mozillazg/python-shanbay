#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from functools import wraps
import logging

from oauthlib.oauth2 import FatalClientError, OAuth2Error, TokenExpiredError
from requests_oauthlib import OAuth2Session, TokenUpdated

from .exceptions import AuthException

logger = logging.getLogger(__name__)


def _catch_token_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TokenExpiredError, TokenUpdated, OAuth2Error,
                FatalClientError) as e:
            raise AuthException(e)
    return wrapper


class API(object):
    def __init__(self, client_id, token):
        self.api = OAuth2Session(client_id, token=token)

    def _request(self, url, method='get', params=None, data=None):
        logger.debug('method: {0}'.format(method))
        logger.debug('params: {0}'.format(params))
        logger.debug('data: {0}'.format(data))
        kwargs = {}
        if method in ('get', 'delete'):
            kwargs['params'] = params
        elif method in ('post',):
            kwargs['data'] = data
        logger.debug('kwargs: {0}'.format(kwargs))

        return getattr(self.api, method)(url, **kwargs)

    @_catch_token_error
    def user(self, url='https://api.shanbay.com/account/'):
        """获取用户信息"""
        return self._request(url).json()

    @_catch_token_error
    def word(self, word, url='https://api.shanbay.com/bdc/search/'):
        """查询单词"""
        params = {
            'word': word
        }
        return self._request(url, params=params).json()

    @_catch_token_error
    def add_word(self, word_id, url='https://api.shanbay.com/bdc/learning/'):
        """添加单词"""
        data = {
            'id': word_id
        }
        return self._request(url, method='post', data=data).json()

    @_catch_token_error
    def examples(self, word_id, type=None,
                 url='https://api.shanbay.com/bdc/example/'):
        """获取单词的例句"""
        params = {
            'vocabulary_id': word_id
        }
        if type is not None:
            params['type'] = type
        return self._request(url, params=params).json()

    @_catch_token_error
    def add_example(self, word_id, original, translation,
                    url='https://api.shanbay.com/bdc/example/'):
        """创建例句"""
        data = {
            'vocabulary': word_id,
            'original': original,
            'translation': translation
        }
        return self._request(url, method='post', data=data).json()

    @_catch_token_error
    def favorite_example(self, example_id,
                         url='https://api.shanbay.com/bdc/learning_example/'):
        """收藏例句"""
        data = {
            'example_id': example_id
        }
        return self._request(url, method='post', data=data).json()

    @_catch_token_error
    def delete_example(self, example_id,
                       url='https://api.shanbay.com/bdc/example/{example_id}/'):
        """删除例句"""
        url = url.format(example_id=example_id)
        return self._request(url, method='delete').json()

    @_catch_token_error
    def notes(self, word_id, url='https://api.shanbay.com/bdc/note/'):
        """获取笔记"""
        params = {
            'vocabulary_id': word_id
        }
        return self._request(url, params=params).json()

    @_catch_token_error
    def add_note(self, word_id, note,
                 url='https://api.shanbay.com/bdc/note/'):
        """创建笔记"""
        data = {
            'vocabulary': word_id,
            'note': note
        }
        return self._request(url, method='post', data=data).json()

    @_catch_token_error
    def favorite_note(self, note_id,
                      url='https://api.shanbay.com/bdc/learning_note/'):
        """收藏笔记"""
        data = {
            'note_id': note_id
        }
        return self._request(url, method='post', data=data).json()

    @_catch_token_error
    def delete_note(self, note_id,
                    url='https://api.shanbay.com/bdc/note/{note_id}/'):
        """删除笔记"""
        url = url.format(note_id=note_id)
        return self._request(url, method='delete').json()
