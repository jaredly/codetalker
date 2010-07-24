#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import INT, WHITE, CharToken, ID, STRING, SSTRING
from codetalker.pgm.special import star, plus, _or, no_ignore, _not
from codetalker.pgm.errors import ParseError

class SYMBOL(CharToken):
    chars = '@;{}'

def many(rule):
    rule | ('{', plus(at), '}')

def at(rule):
    rule | (no_ignore('@', ID), _or(STRING, SSTRING, star(_not(_or(';','}')))), ';')
    rule | star(_not(_or(';','}')))

g = pgm.Grammar(start=many, tokens=[SYMBOL, ID, STRING, SSTRING, WHITE], ignore=[WHITE])

from codetalker import testing

parse_rule = testing.parse_rule(__name__, g)

parse_rule(many, (
    '{@one "hi";}',
    '{@two "ho" ;}',
    '{@three lots of stuff;}',
    '{@four many" m"ore;}',
    '{random junk}',
    '{@I know you can}',
    '{@do "it" yes}',
    ))

if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            print 'testing', name
            fn()
            print 'test passed'
    print 'Finished!'


# vim: et sw=4 sts=4
