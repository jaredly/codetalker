#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import jbnf, cbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = jbnf.Grammar(lfile('c.tokens.2.bnf'), extends = generic.tokens)
tknames = tuple(x for x, in tokens.rules['<token>'])
main = cbnf.Grammar(lfile('c.bnf'), tokens = tknames)

# vim: et sw=4 sts=4
