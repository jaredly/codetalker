#!/usr/bin/env python

from codetalker.contrib.math import m, grammar, evaluate
from codetalker.pgm.grammar import TokenError

def _parse(text):
    tree = grammar.process(text)
    ss = str(tree)
    assert ss == text
    return tree

def test_1():
    r = m.from_string('2+3')
    assert 5 == r

def test_2():
    tree = _parse('2+3')

def test_3():
    assert 4 == m.from_string('2*2')

def test_4():
    assert m.from_string('1+(4/2)') == 3

def test_5():
    assert m.from_string('2**3 - 1') == 7

def test_6():
    assert evaluate('4+2-3*2 - 8 * (3/4 + 0)') == -6

def test_7():
    assert evaluate('3-1') == 2

def test_8():
    assert evaluate('4%3') == 1

if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            print 'testing', name
            fn()
            print 'test passed'
    print 'Finished!'

# vim: et sw=4 sts=4
