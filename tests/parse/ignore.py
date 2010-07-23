#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import INT, WHITE, CharToken, ID
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.errors import ParseError

class SYMBOL(CharToken):
    chars = ':-'

def start(rule):
    rule | (ID, ':', value)

def value(rule):
    rule | (ID, star('-', _or(INT, ID)))
    rule.dont_ignore = True

strings = (
    (
        'name : value',
        'name : value-2',
        'name : value-or-34-others',
        'name:        lots-of-white    '
    ),(
        'name: -value',
        '32: hi',
        'name: value - 2',
        'name : some-value- end'
    )
)

g = pgm.Grammar(start=start, tokens=[SYMBOL, ID, INT, WHITE], ignore=[WHITE])

def mpass(what):
    def meta():
        g.process(what)
    return meta

def mfail(what):
    def meta():
        try:
            g.process(what)
        except ParseError:
            pass
        else:
            raise AssertionError('was supposed to fail on \'%s\'' % what.encode('string_escape'))
    return meta

for i, st in enumerate(strings[0]):
    globals()['test_pass #%d' % i] = mpass(st)
for i, st in enumerate(strings[1]):
    globals()['test_fail #%d' % i] = mfail(st)
        

# vim: et sw=4 sts=4
