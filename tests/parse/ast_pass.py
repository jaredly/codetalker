#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import *
from codetalker.pgm.special import star, plus, _or

def start(rule):
    rule | plus(sub)
    rule.astAttrs = {'items':[NUMBER]}

def sub(rule):
    rule | (NUMBER, NUMBER)

g = pgm.Grammar(start=start, tokens=[NUMBER, WHITE], ignore=[WHITE])

def test_one():
    ast = g.get_ast('1 2')
    assert len(ast.items) == 2

def test_two():
    ast = g.get_ast('1 2 3 4 234 43')
    assert len(ast.items) == 6


# vim: et sw=4 sts=4
