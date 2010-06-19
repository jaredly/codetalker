#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, SYMBOL

def start(rule):
    rule | (star(statement), EOF)

def statement(rule):
    rule | assign

def assign(rule):
    rule | (ID, '=', plus(ID), NEWLINE)

grammar = Grammar(start=start, tokens=[STRING, ID, NUMBER, SYMBOL, WHITE], ignore=[WHITE])

# vim: et sw=4 sts=4
