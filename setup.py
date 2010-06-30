#!/usr/bin/env python
from setuptools import setup
import os

try:
    fp = open(os.path.join(os.path.dirname(__file__), "README.rst"))
    readme_text = fp.read()
    fp.close()
except IOError:
    readme_text = ''

setup(
    name='CodeTalker',
    author='Jared Forsyth',
    author_email='jared@jaredforsyth.com',
    version='0.3',
    url='http://jaredforsyth.com/projects/codetalker/',
    download_url='http://github.com/jabapyth/codetalker/tree',
    description='a module for dynamic, pythonic language parsing',
    long_description=readme_text,
    classifiers=[
        'Programming Language :: Python'
    ],
    test_suite = 'tests.all_tests',
)

# vim: et sw=4 sts=4
