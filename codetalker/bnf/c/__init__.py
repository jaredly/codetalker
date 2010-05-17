#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import jbnf, cbnf, antlrbnf, msbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('c.tokens.bnf'), extends = generic.tokens)
tknames = tuple(x[1:] for x, in tokens.rules['token'])

main = msbnf.Grammar(lfile('c.main.bnf'), tokens = tknames, 
        extends = generic.expressions)

# vim: et sw=4 sts=4
