#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or, expand
from codetalker.pgm.grammar import ParseError

## TOKENS

def SYMBOL(token):
    token | '**' | _or(*'+-*/%()')

## RUlES

'''order of operations:

    && || ; not using
    +-
    */%
    **
    ()
'''

def expression(rule):
    rule | (muldiv, star(_or('+-'), muldiv))

def muldiv(rule):
    rule | (pow, star(_or('*/%'), pow))

def pow(rule):
    rule | (paren, star('**', paren))

def paren(rule):
    rule | ('(', expression, ')') | value

def value(rule):
    rule | NUMBER

grammar = pgm.Grammar(start=start, tokens = [NUMBER, SYMBOL, WHITE, NEWLINE], ignore = [WHITE, NEWLINE])

# vim: et sw=4 sts=4
