#!/usr/bin/env python

import os
import glob
HERE = os.path.dirname(__file__)

files = glob.glob(os.path.join(HERE, '../data/json/*.json'))

from codetalker import testing
import codetalker.contrib.json as json

parse_rule = testing.parse_rule(__name__, json.grammar)

def make_parse(fname):
    text = open(fname).read()
    def meta():
        if os.path.basename(fname).startswith('fail'):
            try:
                res = json.loads(text)
            except:
                pass
            else:
                raise Exception('JSON parsing of %s should have failed: %s' % (fname, text))
        else:
            res = json.loads(text)
    return meta

for fname in files:
    globals()['test_json "%s"' % fname] = make_parse(fname)

parse_rule(json.dict_, (
        '{}',
        '{"one": 3}',
        '{"one": 4, "two": "hi"}',
        ), (
        '{,}',
        '{',
        ))

parse_rule(json.list_, (
        '[]',
        '[1,2]',
        '[1,2,]',
        '["hi"]',
        '[1,"hi"]',
        ), (
        '[,]',
        '[',
        ))

# vim: et sw=4 sts=4
