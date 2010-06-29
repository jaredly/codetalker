#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or, expand
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

def SMALL(token):
    token | plus(expand('0-9'))

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('123\n456\n43')
    assert len(tokens) == 5
    assert tokens[2] == (SMALL, 2, 1, '456')

def test_two():
    try:
        tokens = grammar.get_tokens('wont tokenize')
    except:
        print 'excepted'
    assert tokens == 0


# vim: et sw=4 sts=4
