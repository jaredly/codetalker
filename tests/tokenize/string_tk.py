#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or, expand
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

grammar = pgm.Grammar(start=start, tokens=[STRING,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('"one"')
    assert tuple(tokens) == ((STRING, 1, 1, '"one"'),)

def test_two():
    tokens = grammar.get_tokens('"esca\\"pe"')
    assert len(tokens) == 1

def test_three():
    tokens = grammar.get_tokens('"and"\n"more\\\nescape"\n')
    assert len(tokens) == 4
    assert tokens[-2] == (STRING, 2, 1, '"more\\\nescape"')

# vim: et sw=4 sts=4
