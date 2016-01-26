#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_telegrambot

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_telegrambot.__version__

if sys.argv[-1] == 'publish':
    try:
        import wheel
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-telegrambot',
    version=version,
    description="""A simple app to develop Telegram bot with Django""",
    long_description=readme + '\n\n' + history,
    author='django-telegrambot',
    author_email='francesco.scarlato@gmail.com',
    url='https://github.com/JungDev/django-telegrambot',
    packages=[
        'django_telegrambot',
    ],
    include_package_data=True,
    install_requires=[
        'python-telegram-bot',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-telegrambot',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',        
    ],
)
