#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, SYMBOL, CCOMMENT, ReToken

import re
class CSSNUMBER(ReToken):
    rx = re.compile(r'(?:\d+(?:\.\d+)?|\.\d+)(px|em|%|pt)?')

def start(rule):
    rule | (star(_or(statement, NEWLINE)))

def statement(rule):
    rule | assign | declare

def assign(rule):
    rule | (ID, '=', plus(add_ex), _or(NEWLINE, EOF))

def declare(rule):
    rule | ('@', ID, '(', commas(add_ex), ')', _or(NEWLINE, EOF))

def rule_def(rule):
    rule | (selector, INDENT, plus(_or(statement, NEWLINE)), DEDENT)

def binop(name, ops, next):
    def meta(rule):
        rule | (next, star(_or(*ops), next))
    meta.astName = name
    return meta

def atomic(rule):
    rule | (_or(paren, STRING, ID, CSSNUMBER), star(post))

def paren(rule):
    rule | ('(', add_ex, ')')

def post(rule):
    rule | ('.', ID) | ('[', add_ex, ']') | ('(', commas(add_ex), ')')

def commas(item):
    return (item, star(',', item), [','])


mul_ex = binop('muldiv', '*/', atomic)
add_ex = binop('expression', '+-', mul_ex)

grammar = Grammar(start=start, tokens=[STRING, ID, CSSNUMBER, CCOMMENT, SYMBOL, NEWLINE, WHITE, EOF], ignore=[WHITE, CCOMMENT])

# vim: et sw=4 sts=4
