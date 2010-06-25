#!/usr/bin/env python

from tokens import EOF, Token
from errors import ParseError

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tuple(tokens)
        self.at = 0

    def current(self):
        if self.at >= len(self.tokens):
            return EOF('')
            raise ParseError('ran out of tokens')
        return self.tokens[self.at]
    
    def next(self):
        self.at += 1
        if self.at > len(self.tokens):
            return EOF('')
            raise ParseError('ran out of tokens')
    advance = next

    def hasNext(self):
        return self.at < len(self.tokens) - 1

class _AstNode(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        text = '<%s' % self.name
        for k,v in self.__dict__.iteritems():
            if k == 'name':
                continue
            if isinstance(v, Token):
                v = repr(v)
            elif isinstance(v, AstNode):
                v = repr(v)
            elif type(v) in (tuple, list):
                v = '"..."'
            else:
                v = repr(v)#'"..."'
            text += ' %s=%s' % (k, v)
        return text + '>'

    def __str__(self):
        return repr(self)

class AstNode(object):
    pass

class ParseTree(object):
    __slots__ = ('rule', 'name', 'children')
    def __init__(self, rule, name):
        self.rule = rule
        self.name = name
        self.children = []

    def add(self, child):
        self.children.append(child)

    def __repr__(self):
        text = '<%s>\n  ' % self.name
        for child in self.children:
            if isinstance(child, ParseTree):
                text += repr(child).replace('\n', '\n  ')
            else:
                text += repr(child) + '\n  '
        text = text.rstrip() + '\n' + '</%s>' % self.name
        return text

# vim: et sw=4 sts=4
