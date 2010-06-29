#!/usr/bin/env python

from magictest import MagicTest as TestCase, suite

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

def SMALL(token):
    token | 'hello'

print 'gram'
grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

tokens = grammar.process('hello')
print tokens
tokens = grammar.process('hellohello')
print tokens
tokens = grammar.process('hellohellohellohello')
print tokens
'''
def test_one():
    print 'one'
    tokens = grammar.process('hello')
    assert len(tokens) == 1
    assert tokens[0][-1] == 'hello'

def test_two():
    tokens = grammar.process('hellohello')
    assert len(tokens) == 2
'''

# vim: et sw=4 sts=4
