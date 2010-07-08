#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, INDENT, DEDENT, ReToken, re
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile('hello')

grammar = pgm.Grammar(start=start, tokens=[SMALL, WHITE, NEWLINE], indent=True, ignore=[WHITE])

def test_indent():
    tokens = grammar.get_tokens('hello\n  hello')
    assert len(tokens) == 5
    assert isinstance(tokens[2], INDENT) # tokens[2][0] == INDENT

def test_dedent():
    tokens = grammar.get_tokens('hello\n hello\nhello')
    assert len(tokens) == 8
    assert isinstance(tokens[2], INDENT) # tokens[6][0] == DEDENT


# vim: et sw=4 sts=4
