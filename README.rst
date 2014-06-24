python-shanbay
==============

提供一系列操纵扇贝网 (www.shanbay.com) 的 api

|Build| |Pypi version| |Pypi downloads|



* Documentation: http://python-shanbay.rtfd.org
* GitHub: https://github.com/mozillazg/python-shanbay
* Free software: MIT license
* PyPI: https://pypi.python.org/pypi/shanbay
* Python version: 2.6, 2.7, pypy, 3.3, 3.4


Features
--------

* send/reply message
* manage team


Installation
------------

To install python-shanbay, simply:

.. code-block:: bash

    $ pip install shanbay


Basic Usage
-----------

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
.. .. |Coverage| image:: https://coveralls.io/repos/mozillazg/python-shanbay/badge.png?branch=master
..    :target: https://coveralls.io/r/mozillazg/python-shanbay
.. |Pypi version| image:: https://pypip.in/v/shanbay/badge.png
   :target: https://crate.io/packages/shanbay
.. |Pypi downloads| image:: https://pypip.in/d/shanbay/badge.png
   :target: https://crate.io/packages/shanbay
