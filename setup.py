#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
import sys
import os

__version__ = '0.1.1.dev'
__author__ = 'mozillazg'
__license__ = 'MIT'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = [
    'requests>=2.0.1',
    'beautifulsoup4',
    'html5lib',
]
packages = [
    'shanbay',
]


def long_description():
    readme = open('README.rst', encoding='utf8').read()
    text = readme + '\n\n' + open('CHANGELOG.rst', encoding='utf8').read()
    return text

setup(
    name='shanbay',
    version=__version__,
    description='Python wrapper for shanbay.com',
    long_description=long_description(),
    url='https://github.com/mozillazg/python-shanbay',
    download_url='https://github.com/mozillazg/python-shanbay',
    author=__author__,
    author_email='mozillazg101@gmail.com',
    license=__license__,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'shanbay': 'shanbay'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
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
