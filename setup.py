#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
import re
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

requirements = [
    'requests>=2.0.1',
    'beautifulsoup4',
    'html5lib',
    'requests-oauthlib',
]
packages = [
    'shanbay',
]

current_dir = os.path.dirname(os.path.realpath(__file__))


def read_f(name):
    with open(os.path.join(current_dir, name), encoding='utf8') as f:
        return f.read()


def long_description():
    return read_f('README.rst') + '\n\n' + read_f('CHANGELOG.rst')


def meta_info(meta, filename='shanbay/__init__.py', default=''):
    meta = re.escape(meta)
    m = re.search(r"""%s\s+=\s+(?P<quote>['"])(?P<meta>.+?)(?P=quote)""" % meta,
                  read_f(filename))
    return m.group('meta') if m else default

setup(
    name='shanbay',
    version=meta_info('__version__'),
    description='Python wrapper for shanbay.com',
    long_description=long_description(),
    url='https://github.com/mozillazg/python-shanbay',
    download_url='',
    author=meta_info('__author__'),
    author_email=meta_info('__email__'),
    license=meta_info('__license__'),
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'shanbay': 'shanbay'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    keywords='shanbay, 扇贝网',
)
