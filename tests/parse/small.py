#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | plus(value)

def value(rule):
    rule | STRING | ID | NUMBER

grammar = pgm.Grammar(start=start, tokens=[STRING, ID, NUMBER, WHITE, NEWLINE], ignore=[WHITE, NEWLINE])

def test_one():
    text = '"a string" an_id 12 14.3\n"and\\"12" .3'
    tree = grammar.process(text)
    assert str(tree) == text

if __name__ == '__main__':
    for name, fn in globals().items():
        if name.startswith('test_'):
            fn()
            print 'test passed'
    print 'Finished!'

# vim: et sw=4 sts=4
