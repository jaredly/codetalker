#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, IdToken
from codetalker.pgm.special import star
from codetalker.pgm.errors import TokenError

def start(rule): rule | ID

g1 = Grammar(start=start, tokens=[ID,WHITE], idchars='$')

def test_1():
    tks = g1.get_tokens('some body on$e to$d $me')
    assert len(tks) == 9

g2 = Grammar(start=start, tokens=[ID, WHITE], idchars='-')

def test_2():
    tks = g2.get_tokens('so-me body on-ce told me-')
    assert len(tks) == 9

def test_3():
    try:
        g2.get_tokens('som$one and me')
    except TokenError:
        pass
    else:
        raise AssertionError('was supposed to fail')

# vim: et sw=4 sts=4
