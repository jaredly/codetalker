#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import msbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('json.tokens.bnf'), extends = generic.tokens)
tknames = tuple(x[1:] for x, in tokens.rules['token'])
main = msbnf.Grammar(lfile('json.bnf'), tokens = tknames)

# vim: et sw=4 sts=4
