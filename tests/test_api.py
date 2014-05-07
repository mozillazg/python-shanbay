#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from shanbay import Shanbay

s = Shanbay('root', 'root')
s.login()
api = s.api


def test_user_info():
    assert api.user_info['result'] == 1


def test_query_word():
    assert 'learning_id' in api.query_word('hello')


def test_add_word():
    assert 'id' in api.add_word('hello')


def test_examples():
    learn_id = api.add_word('hello')['id']
    assert api.examples(learn_id)['examples_status'] != -1


def test_add_example():
    learn_id = api.add_word('hello')['id']
    assert api.add_example(learn_id, 'hello', '你好')['example_status'] == 1


def test_add_note():
    learn_id = api.add_word('hello')['id']
    assert api.add_note(learn_id, '你好')['note_status'] == 1
