#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, SYMBOL, CCOMMENT, ReToken, INDENT, DEDENT, StringToken

import re
class CSSNUMBER(ReToken):
    rx = re.compile(r'(?:\d+(?:\.\d+)?|\.\d+)(px|em|%|pt)?')

class CSSSELECTOR(ReToken):
    rx = re.compile(r'(?:[ \t]+|[.:#]?[\w-]+|[>,+&])+:(?=\n|$)')

class CSSID(ReToken):
    rx = re.compile(r'[a-zA-Z_-][a-zA-Z0-9_-]*')

class CSSCOLOR(ReToken):
    rx = re.compile(r'#(?:[\da-fA-F]{3}|[\da-fA-F]{6})')

class SYMBOL(StringToken):
    items = tuple('+-*/@(),=:.')

def start(rule):
    rule | (star(_or(statement, NEWLINE)))

def statement(rule):
    rule | assign | declare | rule_def | attribute

def assign(rule):
    rule | (ID, '=', plus(add_ex), _or(NEWLINE, EOF))

def attribute(rule):
    rule | (cssid, ':', plus(add_ex), _or(NEWLINE, EOF))

def cssid(rule):
    rule.no_white = True
    rule | (_or(('-', ID), (ID)), star('-', ID))

def declare(rule):
    rule | ('@', ID, '(', [commas(add_ex)], ')', _or(NEWLINE, EOF))

def rule_def(rule):
    rule | (CSSSELECTOR, NEWLINE, INDENT, plus(_or(statement, NEWLINE)), _or(DEDENT, EOF))

def binop(name, ops, next):
    def meta(rule):
        rule | (next, star(_or(*ops), next))
    meta.astName = name
    return meta

def atomic(rule):
    rule | (_or(paren, STRING, ID, CSSNUMBER, CSSCOLOR), star(post))

def paren(rule):
    rule | ('(', add_ex, ')')

def post(rule):
    rule | ('.', ID) | ('[', add_ex, ']') | ('(', [commas(add_ex)], ')')

def commas(item):
    return (item, star(',', item), [','])


mul_ex = binop('muldiv', '*/', atomic)
add_ex = binop('expression', '+-', mul_ex)

grammar = Grammar(start=start, indent=True, tokens=[CSSSELECTOR, STRING, ID, CSSNUMBER, CSSCOLOR, CCOMMENT, SYMBOL, NEWLINE, WHITE], ignore=[WHITE, CCOMMENT])

# vim: et sw=4 sts=4
