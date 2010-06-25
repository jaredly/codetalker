#!/usr/bin/env python
'''
Testing for the codetalker.contrib.json grammar
'''

from magictest import MagicTest as TestCase, suite
from codetalker.contrib.json import grammar, JSON

class Basic(TestCase):
    pass

def make_func(func, *args, **kwargs):
    def meta(self):
        func(*args, **kwargs)
    return meta

def make_token(string):
    def meta(self):
        list(grammar.get_tokens(string))
    return meta

def make_trans(a, b):
    def meta(self):
        nw = JSON.from_string(a)
        self.assertEqual(nw, b)
    return meta

to_parse = ['[]','{}','[1,2,3]','{"hello":5, "man":[23,43,"yo"]}', "'he\\'llo'", '"double\\" \'escape"']
for i, string in enumerate(to_parse):
    setattr(Basic, 'parse_%d' % i, make_func(grammar.process, string))
parsed = [[], {}, [1,2,3], {'hello':5, 'man':[23, 43, 'yo']}, "he'llo", 'double" \'escape']
for i, (string, py) in enumerate(zip(to_parse, parsed)):
    setattr(Basic, 'translate_%d' % i, make_trans(string, py))

all_tests = suite(__name__)

# vim: et sw=4 sts=4
