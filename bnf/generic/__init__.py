#!/usr/bin/env python
import os
from codetalker.bnf.parsers import jbnf,msbnf

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('tokens.mbnf'))
expressions = msbnf.Grammar(lfile('basic-expressions.bnf'))
# vim: et sw=4 sts=4
