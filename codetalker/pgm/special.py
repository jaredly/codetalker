#!/usr/bin/env python

class Special:
    '''a special sub-rule for doing more complicated regular expression-like stuff'''
    def __init__(self, *items):
        self.items = items

class star(Special):
    '''Greedy zero-or-more'''
    char = '*'
class plus(Special):
    '''Greedy one-or-more'''
    char = '+'
class _or(Special):
    char = '|'
    def __init__(self, *items):
        if len(items) == 1 and type(items[0]) in (tuple, list):
            items = list(items[0])
        self.items = items
class qstar(Special):
    '''Non-greedy zero-or-more'''
    char = '*?'
class qplus(Special):
    '''Non-greedy one-or-more'''
    char = '+?'
class no_ignore(Special):
    char = 'i'
class _not(Special):
    char = '!'

import string

def binop(*items, **args):
    '''binop(ops1, ops2, ops3, ..., name='BinOp', paren = False, value = [rule or token]) -> rule

    example:
        expression = binop(list('+-'), list('*/%'), paren=True, value=NUMBER)
    '''
    last = args['value']
    def paren(rule):
        rule | ('(', tmp, ')') | args['value']
        rule.pass_single = True
    if args.get('paren', False):
        last = paren
    tmp = make_bop(items[-1], last, args.get('name', 'BinOp'), args['ops_token'])
    for ops in reversed(items[:-1]):
        tmp = make_bop(ops, tmp, args.get('name', 'BinOp'), args['ops_token'])
    return tmp

def make_bop(ops, value, name, ops_token):
    def meta(rule):
        rule | (value, star(_or(*ops), value))
        rule.astAttrs = {
            'left': value,
            'ops': [ops_token],
            'values': {
                'type':[value],
                'start':1,
            },
        }
    meta.astName = name
    return meta

def commas(item, trailing=True, char=','):
    res = (item, star(char, item))
    if trailing:
        return res + ([char],)
    return res

# vim: et sw=4 sts=4
