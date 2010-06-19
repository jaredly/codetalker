#!/usr/bin/env python
import re

class Token:
    def __init__(self, type, val, lineno=-1, charno=-1):
        self.type = type
        self.val = val
        self.lineno = lineno
        self.charno = charno

    def __repr__(self):
        return u'<%s token "%s" at (%d, %d)>' % (self.type, self.val, self.lineno, self.charno)

class TokenMatcher:
    def __init__(self, name):
        self.name = name

    def check(self, text):
        '''test to see if a token matches the current text'''
        raise NotImplementedError

class StringToken(TokenMatcher):
    '''a token that accepts one of many strings'''
    def __init__(self, name, *items):
        TokenMatcher.__init__(self, name)
        self.items = items
    
    def check(self, text):
        for item in self.items:
            if text.text[text.at:].startswith(item):
                return item

class CharToken(StringToken):
    '''a token that accepts a single character'''
    def __init__(self, name, chars):
        StringToken.__init__(self, name, *chars)

class ReToken(TokenMatcher):
    '''a token that is based off of a regular expression'''
    def __init__(self, name, regex):
        TokenMatcher.__init__(self, name)
        self.rx = re.compile(regex)

    def check(self, text):
        m = self.rx.match(text.text[text.at:])
        if m:
            return m.group()

class EOFToken(TokenMatcher):
    '''singleton -- special token for signifying the end of file'''

    def check(self, text):
        if not len(text.text[text.at:]):
            return ''

# TODO: \' \"
STRING = ReToken('String', r'"[^"]*"|' + r"'[^']*'")
ID = ReToken('Identifier', r'[a-zA-Z_][a-zA-Z0-9_]*')
NUMBER = ReToken('Number', r'\d+(?:\.\d+)?|\.\d+')

## WHITE = CharToken(' \t')
WHITE = ReToken('White', '[ \t]+')

SYMBOL = CharToken('Symbol', '=.:')
NEWLINE = CharToken('Newline', '\n')
EOF = EOFToken('EOF')

# vim: et sw=4 sts=4
