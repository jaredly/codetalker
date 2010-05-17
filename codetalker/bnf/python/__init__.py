#!/usr/bin/env python
import ..generic
from codetalker.bnf.parsers import jbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = jbnf.Grammar(open(lfile('python.tokens.bnf')), extends = generic.tokens)
main = jbnf.Grammar(open(lfile('python.bnf')), tokens)

# vim: et sw=4 sts=4
