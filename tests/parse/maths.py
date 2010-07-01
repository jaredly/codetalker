#!/usr/bin/env python

from codetalker.contrib.math import m, grammar
from codetalker.pgm.grammar import TokenError

import py.test

def _parse(text):
    tree = grammar.process(text)
    ss = str(tree)
    assert ss == text
    return tree

def _test_1():
    assert 5 == m.from_string('2+3')

def test_2():
    tree = _parse('2+3')




# vim: et sw=4 sts=4
