#!/usr/bin/env python

class Token(object):
    '''Base token class'''
    __slots__ = ('lineno', 'charno', 'value', 'special')
    def __init__(self, value, *more):
        if len(more) == 1 and hasattr(more[0], 'lineno') and hasattr(more[0], 'charno'):
            self.lineno = more[0].lineno
            self.charno = more[0].charno
        elif len(more) == 2:
            self.lineno = more[0]
            self.charno = more[1]
        elif not more:
            self.lineno = self.charno = -1
        else:
            raise ValueError('invalid line/char arguments: %s' % (more,))
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

# vim: et sw=4 sts=4
