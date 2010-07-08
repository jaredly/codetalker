#!/usr/bin/env python

class Special:
    '''a special sub-rule for doing more complicated regular expression-like stuff'''
    def __init__(self, *items):
        self.items = items

class star(Special):
    char = '*'
class plus(Special):
    char = '+'
class _or(Special):
    char = '|'
class qstart(Special):
    char = '*?'
class qplus(Special):
    char = '+?'

import string
def expand(crange):
    '''expand a regex-like character crange. supported escapes:
    \w a-zA-Z_0-9
    \s whitespace
    \. all printable'''
    items = []
    i = 0
    exclude = False
    if crange[0] == '^':
        i += 1
        exclude = True
    while i < len(crange):
        char = crange[i]
        if char == '\\':
            next = crange[i+1]
            if next == 'w':
                items += list(string.ascii_letters + string.digits + '_')
            elif next == '.':
                items += list(string.printable)
            elif next == 's':
                items += list(' \t\n\r\x0b\x0c')
            elif next in '-][':
                items.append(next)
            elif next in 'xo':
                octal = crange[i:i+4]
                try:
                    de = octal.decode('string_escape')
                except ValueError:
                    raise BNFError, 'invalid escape: %s' % octal
                items.append(de)
                i += 4
                continue
            elif next in 'uU':
                width = {'u':4, 'U':8}[next]
                uni = crange[i:i+width]
                try:
                    de = uni.decode('unicode_escape')
                except ValueError:
                    raise BNFError, 'invalid unicode escape: %s' % uni
                items.append(de)
                i += 2 + width
            else:
                de = (char+next).decode('string_escape')
                if len(de)==2:
                    raise BNFError, 'invalid escape "%s"; the only valid escapes are \\n \\t \\w \\. \\s \\- \\[ \\]' % next
                items.append(de)
            i += 2
            continue
        elif char == '-':
            if i < 1 or i >= len(crange)-1: raise BNFError
            cs = ord(items[-1])
            ce = ord(crange[i+1])
            if ce<cs:raise BNFError
            for a in range(cs,ce):
                items.append(chr(a+1))
            i += 2
            continue
        items.append(char)
        i += 1
    if exclude:
        return _or(*(a for a in string.printable if a not in items))
    return _or(*items)

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
        rule.astAttrs = {'left': {'type':value, 'single':True}, 'ops': ops_token, 'values': {'type':value, 'start':1}}
    meta.astName = name
    return meta

def commas(item, trailing=True):
    res = (item, star(',', item))
    if trailing:
        return res + ([','],)
    return res

# vim: et sw=4 sts=4
