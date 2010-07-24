#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError, AstError

def start(rule):
    rule | plus(_or(STRING, ID, NUMBER))
    rule.astAttrs = {'values':[STRING, ID, NUMBER]}

grammar = pgm.Grammar(start=start, tokens=[STRING, ID, NUMBER, WHITE, NEWLINE], ignore=[WHITE, NEWLINE])

def test_one():
    text = '"a string" an_id 12 14.3\n"and\\"12" .3'
    tree = grammar.get_ast(text)
    assert len(tree.values) == 6

def start2(rule):
    rule | plus(_or(STRING, ID, NUMBER))
    rule.astAttrs = {'values':(STRING, ID, NUMBER)}

g2 = pgm.Grammar(start=start2, tokens=[STRING, ID, NUMBER, WHITE, NEWLINE], ignore=[WHITE, NEWLINE])

def test_two():
    text = '"a string" an_id 12 14.3\n"and\\"12" .3'
    tree = g2.get_ast(text)
    assert len(tree.values) == 6

def start3(rule):
    rule | 'hi'
    rule.astAttrs = {'bogus':5}

def test_three():
    try:
        g3 = pgm.Grammar(start=start3, tokens=[], ignore=[])
    except AstError, e:
        pass
    else:
        raise AssertionError('was supposed to fail -- invalid ast type')

if __name__ == '__main__':
    for name, fn in globals().items():
        if name.startswith('test_'):
            fn()
            print 'test passed'
    print 'Finished!'


# vim: et sw=4 sts=4
