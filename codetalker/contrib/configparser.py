#!/usr/bin/env python

from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.tokens import *

def start(rule):
    rule | star(_or(section, NEWLINE))
    rule.astAttrs = {'sections':[section]}

def section(rule):
    rule | (head, star(_or(define, NEWLINE)))
    rule.astAttrs = {'head':head, 'body':[define]}

def head(rule):
    rule | ('[', name, ']')
    rule.pass_single = True

def define(rule):
    rule | (name, _or(':', '='), value)
    rule.astAttrs = {'name':name, 'value':value}

def name(rule):
    rule | plus(_or(ID, NUMBER, WHITE))
    rule.astAttrs = {'words':[ID, NUMBER, WHITE]}

not_newline = (ANY, WHITE, ID, NUMBER)

def value(rule):
    rule | (star(_or(*not_newline)), _or(EOF, (NEWLINE, [INDENT, star(star(_or(*not_newline)), _or(NEWLINE, EOF)), _or(DEDENT, EOF)])))
    rule.astAttrs = {'text':list(not_newline)+[NEWLINE]}

grammar = Grammar(start=start, indent=True, tokens=[ID, NUMBER, NEWLINE, WHITE, ANY], idchars='-')

class RecursionError(Exception):pass

class Config:
    def __init__(self, sections={}):
        self.sections = sections

    def add_section(self, name, vbls):
        self.sections[name] = vbls

    def get_item(self, section, name, check=()):
        if not section in self.sections:
            raise KeyError('invalid section: %s' % section)
        elif name not in self.sections[section]:
            raise KeyError('undefined vbl: %s for section %s' % (name, section))
        elif name in check:
            raise RecursionError('recursive interpolation detected %s' % (check + (name,),))
        value = self.sections[section][name]
        if '%' not in value: # no need to interpolate
            return value
        vbls = {}
        for i in xrange(1000): # just in case something goes wrong...
            try:
                return value % vbls
            except KeyError, e:
                vbls[e.args[0]] = self.get_item(section, e.args[0], check + (name,))
        raise RecursionError('resursive interpolation...')

ast = grammar.ast_classes

t = Translator(grammar)

@t.translates(ast.Start)
def _start(node):
    return Config(dict(t.translate(section) for section in node.sections))

@t.translates(ast.Section)
def _section(node):
    return t.translate(node.head), dict(t.translate(line) for line in node.body)

@t.translates(ast.Define)
def _define(node):
    return t.translate(node.name), t.translate(node.value)

@t.translates(ast.Name)
def _name(node):
    return ''.join(tok.value for tok in node.words).strip()

@t.translates(ast.Value)
def _value(node):
    return ''.join(tok.value for tok in node.text).strip()

parse = t.from_string

# vim: et sw=4 sts=4
