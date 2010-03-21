#!/usr/bin/env python
from codetalker.bnf import generic
from codetalker.bnf.parsers import jbnf, cbnf, msbnf
import os

lfile = lambda name:os.path.join(os.path.dirname(__file__),name)

tokens = msbnf.Grammar(lfile('msdn_tokens.txt'))#, extends = generic.tokens)
tknames = tuple(x for x, in tokens.rules['token'])
# print tknames
"""tknames = tuple(a.strip() for a in ''' identifier
    keyword
    comment
    pp-directive
    boolean-literal
    integer-literal
    real-literal
    character-literal
    string-literal
    null-literal
    operator-or-punctuator'''.split('\n') if a.strip())"""
main = msbnf.Grammar(lfile('msdn_c.smaller.txt'), tokens = tknames)

# vim: et sw=4 sts=4
