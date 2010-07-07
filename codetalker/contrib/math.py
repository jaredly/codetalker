#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, ReToken, re
from codetalker.pgm.special import star, plus, _or, expand, binop
from codetalker.pgm.grammar import ParseError

## TOKENS

class OP(ReToken):
    rx = re.compile('\\*\\*|[-+*/%]')

class SYMBOL(ReToken):
    rx = re.compile('[()]')

## RUlES

'''order of operations:

    && || ; not using
    +-
    */%
    **
    ()
'''

expression = binop(list('-+'), list('*/%'), ['**'], value=NUMBER, ops_token=OP, name='BinOp', paren=True)

grammar = pgm.Grammar(start=expression, tokens = [OP, NUMBER, SYMBOL, WHITE, NEWLINE], ignore = [WHITE, NEWLINE], ast_tokens=[NUMBER])

m = pgm.Translator(grammar)

ast = grammar.ast_classes

import operator
ops = {'**':operator.pow, '*':operator.mul, '/':operator.div, '%':operator.mod, '+':operator.add, '-':operator.sub}

@m.translates(ast.BinOp)
def binop(node, scope):
    value = m.translate(node.left, scope)
    for op, right in zip(node.ops, node.values):
        nv = m.translate(right, scope)
        value = ops[op.value](value, nv)
    return value

@m.translates(NUMBER)
def number(node, scope):
    return float(node.value)

evaluate = m.from_string

# vim: et sw=4 sts=4
