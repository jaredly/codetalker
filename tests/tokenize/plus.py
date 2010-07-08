#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile('(hello)+')

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('\n')
    assert tuple(tokens) == ((NEWLINE, 1, 1, '\n'),)

def test_two():
    tokens = grammar.get_tokens('hello')
    assert tuple(tokens) == ((SMALL, 1, 1, 'hello'),)

def test_three():
    tokens = grammar.get_tokens('hellohellohello\nhellohello\nhello\n\n')
    assert len(tokens) == 7
    assert tokens[0] == (SMALL, 1, 1, 'hellohellohello')

# vim: et sw=4 sts=4
