#!/usr/bin/env python
import os
from codetalker.bnf.parsers import jbnf

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = jbnf.Grammar(lfile('tokenize.bnf'))
# vim: et sw=4 sts=4
