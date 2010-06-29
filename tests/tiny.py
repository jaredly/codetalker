#!/usr/bin/env python

from magictest import MagicTest as TestCase, suite

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | 'what'

def SMALL(token):
    token | '33' | 'hello' | '3'

grammar = pgm.Grammar(start=start, tokens=[SMALL,NEWLINE])

grammar.process('33333\n\nhello\n')

# vim: et sw=4 sts=4
