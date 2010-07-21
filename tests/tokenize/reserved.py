#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE, IdToken
from codetalker.pgm.special import star

class RESERVED(IdToken):
    strings = ['for', 'in', 'and']

def start(rule):
    rule | (RESERVED, star(ID, RESERVED))

grammar = Grammar(start=start, tokens=[RESERVED, ID, WHITE])

def test_1():
    tks = grammar.get_tokens('for unto in foreign')
    assert len(tks) == 7
    assert isinstance(tks[0], RESERVED)
    assert isinstance(tks[-1], ID)

def test_2():
    tks = grammar.get_tokens('int in2 in teger')
    assert len(tks) == 7
    assert isinstance(tks[0], ID)
    assert isinstance(tks[2], ID)
    assert isinstance(tks[4], RESERVED)
    assert isinstance(tks[6], ID)

def test_3():
    tks = grammar.get_tokens('at the end for')
    assert len(tks) == 7
    assert isinstance(tks[-1], RESERVED)

# vim: et sw=4 sts=4
