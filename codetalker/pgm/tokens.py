#!/usr/bin/env python
import re
from special import star, plus, _or, expand

EOF = object()
INDENT = object()
DEDENT = object()

class Token(object):
    def __init__(self, rule, value, lineno, charno):
        self.rule = rule
        self.value = value
        self.lineno = lineno
        self.charno = charno

def STRING(token):
    token | ('"', star(_or(('\\', _or('\n','"')), expand('^\n"'))), '"')

def ID(token):
    token | (expand('a-zA-Z_'), star(expand('a-zA-Z0-9_')))

def NUMBER(token):
    token | (['-'], _or((plus(expand('0-9')), ['.', expand('0-9')]), ('.', plus(expand('0-9')))))

def WHITE(token):
    token | plus(_or(*' \t'))

def NEWLINE(token):
    token | '\n'

# vim: et sw=4 sts=4
