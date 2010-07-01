#!/usr/bin/env python

from codetalker.contrib.math import m, grammar
from codetalker.pgm.grammar import TokenError

import py.test

def _ttoken(text):
    tk = grammar.get_tokens(text)
    assert ''.join(token[-1] for token in tk) == text
    return tk

def test_one():
    py.test.raises(TokenError, grammar.get_tokens, '')

def test_two():
    tk = _ttoken('3')

def test_three():
    tk = _ttoken('+')

def test_4():
    tk = _ttoken('1 2 3 4 5')

def test_5():
    tk = _ttoken('()+-')

def test_6():
    tk = _ttoken('1 () 3.4+2')

# vim: et sw=4 sts=4
