#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import os

import pytest

from shanbay.api import API
from shanbay import AuthException
current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, 'token.json')) as f:
    token = json.loads(f.read())


def test_exception():
    api = API('1333', token={})
    try:
        api.user()
    except AuthException:
        assert True


class TestAPI(object):
    # def __init__(self):   # 不能使用 __init__ 否则 py.test 会忽略这个类
    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        self.api = API('091e43d72fe4466a0433', token=token)

    def test_user(self):
        assert self.api.user()['username'] == 'mozillazg'

    def test_word(self):
        assert self.api.word('hello')['data']['id']

    def test_add_word(self):
        word_id = self.api.word('hello')['data']['id']
        assert self.api.add_word(word_id)['data']['id']

    def test_examples(self):
        word_id = self.api.word('hello')['data']['id']
        assert self.api.examples(word_id)['data'][0]['id']
        assert self.api.examples(word_id, type='sys'
                                 )['data'][0]['id']

    def test_add_example(self):
        word_id = self.api.word('hello')['data']['id']
        data = self.api.add_example(word_id, 'hello', '你好')
        assert data['data']['id']

    def test_favorite_example(self):
        word_id = self.api.word('hello')['data']['id']
        data = self.api.add_example(word_id, 'hello', '你好')
        assert self.api.favorite_example(data['data']['id']
                                         )['status_code'] == 0

    def test_delete_example(self):
        word_id = self.api.word('hello')['data']['id']
        data = self.api.add_example(word_id, 'hello', '你好')
        assert self.api.delete_example(data['data']['id'])['status_code'] == 0

    def test_notes(self):
        word_id = self.api.word('hello')['data']['id']
        assert self.api.notes(word_id)['status_code'] == 0

    def test_add_note(self):
        word_id = self.api.word('hello')['data']['id']
        assert self.api.add_note(word_id, '你好')['status_code'] == 0

    def test_favorite_note(self):
        word_id = self.api.word('hello')['data']['id']
        note_id = self.api.add_note(word_id, '你好')['data']['id']
        assert self.api.favorite_note(note_id)['status_code'] == 0

    def test_delete_note(self):
        word_id = self.api.word('hello')['data']['id']
        note_id = self.api.add_note(word_id, '你好')['data']['id']
        assert self.api.delete_note(note_id)['status_code'] == 0
