#!/usr/bin/env python
import re

class TokenMatcher:
    def check(self, text):
        '''test to see if a token matches the current text'''
        raise NotImplementedError

class StringToken(TokenMatcher):
    '''a token that accepts one of many strings'''
    def __init__(self, *items):
        self.items = items
    
    def check(self, text):
        for item in self.items:
            if text.startswith(item):
                return item

class CharToken(StringToken):
    '''a token that accepts a single character'''
    def __init__(self, chars):
        self.items = list(chars)

class ReToken(TokenMatcher):
    '''a token that is based off of a regular expression'''
    def __init__(self, regex):
        self.rx = re.compile(regex)

    def check(self, text):
        m = self.rx.match(text)
        if m:
            return m.group()

class EOFToken(TokenMatcher):
    '''singleton -- special token for signifying the end of file'''

    def check(self, text):
        if not len(text):
            return ''

# TODO: \' \"
STRING = ReToken(r'"[^"]*"|' + r"'[^']*'")
ID = ReToken(r'[a-zA-Z_][a-zA-Z0-9_]*')
NUMBER = ReToken(r'\d+(?:\.\d+)?|\.\d+')

## WHITE = CharToken(' \t')
WHITE = ReToken('[ \t]+')

SYMBOL = CharToken('=.:')
NEWLINE = CharToken('\n')
EOF = EOFToken()

# vim: et sw=4 sts=4
