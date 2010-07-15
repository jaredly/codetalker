#!/usr/bin/env python

try:
    from distutils.core import setup
    from distutils.extension import Extension
except ImportError:
    print 'distutils is required to install this module. If you have pip installed, run: pip instal distutils'
    raise

try:
    from Cython.Distutils import build_ext
except ImportError:
    print 'Cython is required to install this module'
    raise

import os
import glob

try:
    fp = open(os.path.join(os.path.dirname(__file__), "README.rst"))
    readme_text = fp.read()
    fp.close()
except IOError:
    readme_text = ''

pyx_mods = []

for filen in glob.glob('codetalker/pgm/cgrammar/*.pyx'):
    if filen.split('/')[-1].startswith('_'):
        continue
    if filen.endswith('/tokens.pyx') or filen.endswith('/tokenize.pyx'):
        extra = ['codetalker/pgm/cgrammar/_speed_tokens.c']
    else:
        extra = []
    pyx_mods.append(Extension(filen.replace('/','.')[:-4], [filen]+extra))

from test_cmd import test

setup(
    name='CodeTalker',
    author='Jared Forsyth',
    author_email='jared@jaredforsyth.com',
    version='0.5',
    url='http://jaredforsyth.com/projects/codetalker/',
    download_url='http://github.com/jabapyth/codetalker/tree',
    description='a module for dynamic, pythonic language parsing',
    long_description=readme_text,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    options={
        'test':{
            'test_dir':['tests/parse', 'tests/tokenize']
        },
    },
    requires=['cython'],

    cmdclass = {'build_ext': build_ext , 'test':test},
    ext_modules = pyx_mods,
    include_dirs = 'codetalker',
    packages = ['codetalker', 'codetalker.pgm', 'codetalker.contrib', 'codetalker.pgm.cgrammar'],
)

# vim: et sw=4 sts=4
