#!/usr/bin/env python
import os
from codetalker.bnf.parsers import jbnf,msbnf

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('tokens.mbnf'))
tknames = tuple(x[1:] for x, in tokens.rules['token'])
expressions = msbnf.Grammar(lfile('basic-expression.bnf'), tokens=tknames)
# vim: et sw=4 sts=4
