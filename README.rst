python-shanbay
==============

提供一系列操纵扇贝网 (www.shanbay.com) 的 API

|Build| |PyPI version|



* Documentation: http://python-shanbay.rtfd.org
* GitHub: https://github.com/mozillazg/python-shanbay
* Free software: MIT license
* PyPI: https://pypi.python.org/pypi/shanbay
* Python version: 2.6, 2.7, pypy, 3.3, 3.4, 3.5


Features
--------

* send/reply message
* manage team
* support shanbay api v1


Installation
------------

To install python-shanbay, simply:

.. code-block:: bash

    $ pip install shanbay


Basic Usage
-----------

OAuth2 认证 API（可以通过 `这个脚本`__ 获取 token)

__ https://gist.github.com/mozillazg/4af649ff88612b2de7c7

.. code-block:: python

    >>> from shanbay import API
    >>> token = {
    "access_token": "7ANNoQFY02rJkqqm8Zi67aQ9N6ES8G",
    "expires_in": "1592000", "expires_at": 1328664099.868803,
    "token_type": "Bearer", "state": "H3rTN84NG2TdunSt9bG02acEkSNWiW",
    "scope": [ "read", "write" ]
    }
    >>>
    >>> api = API('client_id_xxyyyx', token)
    >>> api.user()
    {u'avatar': u'http://qstatic.shanbay.com/avatar/media_store/3034aee41d32d464aac362cf608cb735.png?imageView/1/w/80/h/80/',
 u'id': 1279912,
    u'nickname': u'\u266b mozillazg',
    u'username': u'mozillazg'}
    >>>

用户名密码认证 API（不支持 REST API）

.. code-block:: python

    >>> from shanbay import Shanbay, Message
    >>> shanbay = Shanbay('username', 'password')
    >>> shanbay.login()
    True
    >>> message = Message(shanbay)
    >>> message.send_message(['mozillazg'], 'hello', 'hello')
    True


.. |Build| image:: https://api.travis-ci.org/mozillazg/python-shanbay.png?branch=master
   :target: https://travis-ci.org/mozillazg/python-shanbay
.. |PyPI version| image:: https://img.shields.io/pypi/v/shanbay.svg
   :target: https://pypi.python.org/pypi/shanbay
