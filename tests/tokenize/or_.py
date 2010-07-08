#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile('one|two')

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('one')
    assert tuple(tokens) == ((SMALL, 1, 1, 'one'),)

def test_two():
    tokens = grammar.get_tokens('twoonetwo\noneone')
    assert len(tokens) == 6
    assert list(tokens[:3]) == [(SMALL, 1, 1, 'two'), (SMALL, 1, 4, 'one'), (SMALL, 1, 7, 'two')]

# vim: et sw=4 sts=4
