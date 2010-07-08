#!/usr/bin/env python

from token import Token

from codetalker.pgm.cgrammar.tokens import STRING, ID, WHITE, NEWLINE, NUMBER

import re

class StringToken(Token):
    '''a token that accepts one of many strings'''
    items = []

    @classmethod
    def check(cls, text):
        for item in cls.items:
            if text[:len(item)] == item:
                return len(item)
        return 0

class ReToken(Token):
    '''a token that is based off of a regular expression'''
    rx = None

    @classmethod
    def check(cls, text):
        m = cls.rx.match(text)
        if m:
            return len(m.group())
        return 0

class SpecialToken(Token):
    '''a special token which is automatically provided by the parser'''
    @classmethod
    def check(cls, text):
        return 0

class EOF(SpecialToken):
    '''singleton -- special token for signifying the end of file'''

class INDENT(SpecialToken):
    '''used by the preprocessor to indicate the start of an indented block'''

class DEDENT(SpecialToken):
    '''used by the preprocessor to indicate the end of an indented block'''

# class STRING(ReToken):
    # rx = re.compile(r'"(?:\\"|[^"])*"|' + r"'(?:\\'|[^'])*'")

# class ID(ReToken):
    # rx = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')

# class NUMBER(ReToken):
 #    rx = re.compile(r'-?(?:\d+(?:\.\d+)?|\.\d+)')

# class WHITE(ReToken):
    # rx = re.compile(r'[ \t]+')

# class NEWLINE(StringToken):
    # rx = re.compile(r'\n')
    # items = ['\n']

class CCOMMENT(ReToken):
    rx = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)

from text import Text
# vim: et sw=4 sts=4
