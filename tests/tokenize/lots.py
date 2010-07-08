#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or, expand
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

grammar = pgm.Grammar(start=start, tokens=[STRING, ID, NUMBER, WHITE, NEWLINE])

def test_one():
    text = '"a string" an_id 12 14.3\n"and\\"12" .3'
    tokens = grammar.get_tokens(text)
    assert len(tokens) == 11
    assert ''.join(a.value for a in tokens) == text

# vim: et sw=4 sts=4
