#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import jbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = jbnf.Grammar(lfile('json.tokens.bnf'), extends = generic.tokens)
tknames = tuple(x for x, in tokens.rules['token'])
main = msbnf.Grammar(lfile('json.bnf'), tokens = tknames)

# vim: et sw=4 sts=4
