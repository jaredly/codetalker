#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile('hello')

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('hello')
    assert len(tokens) == 1
    assert list(tokens) == [(SMALL, 1, 1, 'hello')]

def test_two():
    tokens = grammar.get_tokens('hello\nhello')
    assert len(tokens) == 3
    assert tokens[2] == (SMALL, 2, 1, 'hello')

def test_three():
    tokens = grammar.get_tokens('hello\nhello\n\nhellohello')
    assert len(tokens) == 7
    assert tokens[-1] == (SMALL, 4, 6, 'hello')

# vim: et sw=4 sts=4
