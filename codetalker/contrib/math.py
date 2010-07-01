#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or, expand, binop
from codetalker.pgm.grammar import ParseError

## TOKENS

def OP(token):
    token | '**' | _or(*'+-*/%')

def SYMBOL(token):
    token | '(' | ')'

## RUlES

'''order of operations:

    && || ; not using
    +-
    */%
    **
    ()
'''

expression = binop(list('+-'), list('*/%'), ['**'], value=NUMBER, ops_token=OP, name='BinOp')

grammar = pgm.Grammar(start=expression, tokens = [NUMBER, OP, SYMBOL, WHITE, NEWLINE], ignore = [WHITE, NEWLINE])

m = pgm.Translator(grammar)

ast = grammar.ast_classes

import operator
ops = {'**':operator.pow, '*':operator.mul, '/':operator.div, '%':operator.mod, '+':operator.add, '-':operator.sub}

@m.translates(ast.BinOp)
def binop(node, scope):
    value = m.translate(node.left, scope)
    for op, right in zip(node.ops, node.values):
        value = ops[op.value](value, m.translate(right, scope))
    return value

@m.translates(NUMBER)
def number(node, scope):
    return float(node.value)

evaluate = m.from_string

# vim: et sw=4 sts=4
