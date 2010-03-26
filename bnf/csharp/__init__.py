#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import jbnf, cbnf, msbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('c.tokens.txt'), extends = generic.mtokens)
tknames = tuple(x[1:] for x, in tokens.rules['token'])
main = msbnf.Grammar(lfile('msdn_c.smaller.txt'), tokens = tknames)

# vim: et sw=4 sts=4
