#!/usr/bin/env python

import os
import glob
HERE = os.path.dirname(__file__)

files = glob.glob(os.path.join(HERE, '../data/json/*.json'))

from codetalker.contrib.json import loads

def make_parse(fname):
    text = open(fname).read()
    def meta():
        res = loads(text)
    return meta

for fname in files:
    globals()['test_json "%s"' % fname] = make_parse(fname)


# vim: et sw=4 sts=4
