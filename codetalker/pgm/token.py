#!/usr/bin/env python

class Token(object):
    '''Base token class'''
    # __slots__ = ('lineno', 'charno', 'value', 'special')
    def __init__(self, value, lineno=-1, charno=-1):
        self.lineno = lineno
        self.charno = charno
        self.value = value

    def __repr__(self):
        return u'<%s token "%s" at (%d, %d)>' % (self.__class__.__name__,
                self.value.encode('string_escape'), self.lineno, self.charno)

    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        if type(other) in (tuple, list):
            return tuple(other) == (self.__class__, self.lineno, self.charno, self.value)

    @classmethod
    def check(cls, at, text):
        '''test to see if a token matches the current text'''
        raise NotImplementedError

class ReToken(Token):
    '''a token that is based off of a regular expression'''
    rx = None

    @classmethod
    def check(cls, text):
        m = cls.rx.match(text)
        if m:
            return len(m.group())
        return 0

# vim: et sw=4 sts=4
