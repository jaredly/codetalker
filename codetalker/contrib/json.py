#!/usr/bin/env python

from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, NUMBER, EOF, NEWLINE, WHITE, ReToken, re

'''Man this looks sweet. It really should be
this easy to write a json parser.'''

# special tokens

class SYMBOL(ReToken):
    rx = re.compile('[{},[\\]:]')

class TFN(ReToken):
    rx = re.compile('true|false|null')

# rules (value is the start rule)
def value(rule):
    rule | dict_ | list_ | STRING | TFN | NUMBER
    rule.pass_single = True

def dict_(rule):
    rule | ('{', [commas((STRING, ':', value))], '}')
    rule.astAttrs = {'keys': STRING, 'values': value}
dict_.astName = 'Dict'

def list_(rule):
    rule | ('[', [commas(_or(dict_, list_, STRING, TFN, NUMBER))], ']')
    rule.astAttrs = {'values': [dict_, list_, STRING, TFN, NUMBER]}
list_.astName = 'List'

grammar = Grammar(start=value,
                  tokens=[STRING, NUMBER, NEWLINE, WHITE, SYMBOL, TFN],
                  ignore=[WHITE, NEWLINE],
                  ast_tokens=[STRING, TFN, NUMBER])

# translator stuff
JSON = Translator(grammar)

ast = grammar.ast_classes

@JSON.translates(ast.Dict)
def t_dict(node, scope):
    return dict((JSON.translate(key, scope), JSON.translate(value, scope))\
                 for (key, value) in zip(node.keys, node.values))

@JSON.translates(ast.List)
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
