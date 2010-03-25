#!/usr/bin/env python
'''
    one of the examples for codetalker (http://github.com/jabapyth/codetalker)
    really basic, and is mostly for testing;
    parses the input file, dies on invalid syntax, and outputs (if it works)
    the same code back.
'''
import codetalker
from codetalker.bnf import c

import os,sys

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'usage: parse_c.py file.c'
        sys.exit(1)
    text = open(sys.argv[1]).read()
    root = codetalker.parse(text, c)
    print root

# vim: et sw=4 sts=4
