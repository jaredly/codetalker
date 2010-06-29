#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

def SMALL(token):
    token | plus('hello')

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('\n')
    assert tokens == [(NEWLINE, 1, 1, '\n')]

def test_two():
    tokens = grammar.get_tokens('hello')
    assert tokens == [(SMALL, 1, 1, 'hello')]

def test_three():
    tokens = grammar.get_tokens('hellohellohello\nhellohello\nhello\n\n')
    assert len(tokens) == 7
    assert tokens[0] == (SMALL, 1, 1, 'hellohellohello')

# vim: et sw=4 sts=4
