#!/usr/bin/env python

from codetalker.contrib.math import m, grammar
from codetalker.pgm.grammar import TokenError

import py.test

def test_one():
    py.test.raises(TokenError, grammar.get_tokens, '')

def test_two():
    tk = grammar.get_tokens('3')

def test_three():
    tk = grammar.get_tokens('+')

def test_4():
    tk = grammar.get_tokens('1 2 3 4 5')

def test_5():
    tk = grammar.get_tokens('()+-')

def test_6():
    tk = grammar.get_tokens('1 () 3.4+2')


# vim: et sw=4 sts=4
