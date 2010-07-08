#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class small(ReToken):
    rx = re.compile('(which)?that')

grammar = pgm.Grammar(start=start, tokens=[small,NEWLINE])

def test_one():
    tokens = grammar.get_tokens('that\nwhichthat\n')
    assert len(tokens) == 4
    assert tokens[2] == (small, 2, 1, 'whichthat')

# vim: et sw=4 sts=4
