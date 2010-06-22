#!/usr/bin/env python
import re
from text import Text

class Token:
    def __init__(self, value, *more):
        if len(more) == 1 and isinstance(more[0], Text):
            self.lineno = more[0].lineno
            self.charno = more[0].charno
        elif len(more) == 2:
            self.lineno = more[0]
            self.charno = more[1]
        elif not more:
            self.lineno = self.charno = -1
        else:
            raise ValueError('invalid line/char arguments')
        self.value = value

    def __repr__(self):
        return u'<%s token "%s" at (%d, %d)>' % (self.__class__.__name__,
                self.value.encode('string_escape'), self.lineno, self.charno)

    @classmethod
    def check(cls, text):
        '''test to see if a token matches the current text'''
        raise NotImplementedError

class StringToken(Token):
    '''a token that accepts one of many strings'''
    items = []

    @classmethod
    def check(cls, text):
        for item in cls.items:
            if text.text[text.at:text.at + len(item)] == item:
                return cls(item, text)

class ReToken(Token):
    '''a token that is based off of a regular expression'''
    rx = None

    @classmethod
    def check(cls, text):
        m = cls.rx.match(text.text[text.at:])
        if m:
            return cls(m.group(), text)

class EOF(Token):
    '''singleton -- special token for signifying the end of file'''

    @classmethod
    def check(cls, text):
        if not len(text.text[text.at:]):
            return cls('', text)

class STRING(ReToken):
    rx = re.compile(r'"[^"]*"|' + r"'[^']*'")

class ID(ReToken):
    rx = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')

class NUMBER(ReToken):
    rx = re.compile(r'\d+(?:\.\d+)?|\.\d+')

## WHITE = CharToken(' \t')
class WHITE(ReToken):
    rx = re.compile(r'[ \t]+')
class SYMBOL(StringToken):
    items = list('~!@#$%^&*()_+-=[]{}|\\<>?,./;\':"')
class NEWLINE(StringToken):
    items = ['\n']
class CCOMMENT(ReToken):
    rx = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)


# vim: et sw=4 sts=4
