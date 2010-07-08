#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile("'(hello)*")

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

def test_one():
    tokens = grammar.get_tokens("''hellohello'hello\n'\n")
    assert len(tokens) == 6
    assert tokens[1] == (SMALL, 1, 2, "'hellohello")

# vim: et sw=4 sts=4
