#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, INDENT, DEDENT, ReToken, re, INT
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

from codetalker.cgrammar import TokenError

def start(rule):
    rule | 'what'

class SMALL(ReToken):
    rx = re.compile('hello')

grammar = pgm.Grammar(start=start, tokens=[SMALL, WHITE, NEWLINE], indent=True, ignore=[WHITE])

g2 = pgm.Grammar(start=start, tokens=[INT, WHITE, NEWLINE], indent=True, ignore=[WHITE])

def test_indent():
    tokens = grammar.get_tokens('hello\n  hello')
    assert len(tokens) == 5
    assert isinstance(tokens[2], INDENT) # tokens[2][0] == INDENT

def test_dedent():
    tokens = grammar.get_tokens('hello\n hello\nhello')
    assert len(tokens) == 8
    assert isinstance(tokens[2], INDENT) # tokens[6][0] == DEDENT

def test_c_indent():
    tokens = g2.get_tokens('23\n 32')
    assert len(tokens) == 5
    assert isinstance(tokens[2], INDENT)

def test_c_dedent():
    tokens = g2.get_tokens('3\n 4\n5')
    assert len(tokens) == 8
    assert isinstance(tokens[2], INDENT) # tokens[6][0] == DEDENT

import textwrap

def test_badindent():
    text = textwrap.dedent('''\
    hello
            hello
        hello
    ''')
    try:
        grammar.get_tokens(text)
    except TokenError:
        return True
    raise AssertionError('was supposed to fail')


# vim: et sw=4 sts=4
