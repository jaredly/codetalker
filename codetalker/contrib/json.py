#!/usr/bin/env python

from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, NUMBER, EOF, NEWLINE, WHITE, SYMBOL, ReToken, StringToken

class TFN(StringToken):
    items = ['true', 'false', 'null']

def value(rule):
    rule | dict_ | list_ | STRING | TFN | NUMBER

def dict_(rule):
    rule | ('{', [commas((STRING, ':', value))], '}')
    rule.astAttrs = {'keys': {'token':STRING},
            'values': {'rule': value}}

def list_(rule):
    rule | ('[', [commas(value)], ']')
    rule.astAttrs = {'values': {'rule': value}}

grammar = Grammar(start=value,
                  tokens=[STRING, NUMBER, NEWLINE, WHITE, SYMBOL, TFN],
                  ignore=[WHITE],
                  ast_tokens=[STRING, TFN, NUMBER])

JSON = Translator(grammar)

@JSON.translates(dict_)
def t_dict(node, scope):
    return dict((JSON.translate(key, scope), JSON.translate(value, scope))\
                 for (key, value) in zip(node.keys, node.values))

@JSON.translates(list_)
def t_list(node, scope):
    return list(JSON.translate(value, scope) for value in node.values)

@JSON.translates(STRING)
def t_string(node, scope):
    return node.value[1:-1].decode('string_escape')

@JSON.translates(NUMBER)
def t_number(node, scope):
    if '.' in node.value:
        return float(node.value)
    return int(node.value)

@JSON.translates(TFN)
def t_tfn(node, scope):
    return {'true':True, 'false':False, 'null':None}

# vim: et sw=4 sts=4
