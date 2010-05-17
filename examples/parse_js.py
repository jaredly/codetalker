#!/usr/bin/env python
'''
    one of the examples for codetalker (http://github.com/jabapyth/codetalker)
    really basic, and is mostly for testing;
    parses the input file, dies on invalid syntax, and outputs (if it works)
    the same code back.
'''
import codetalker
from codetalker.bnf import js

import os,sys

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'usage: parse_js.py file.js -q'
        sys.exit(1)
    if len(sys.argv) == 3:
        filen, op = sys.argv[1:]
    else:
        filen, = sys.argv[1:]
        op = None
    text = open(filen).read()
    root = codetalker.parse(text, js)
    if op != '-q':
        print root

# vim: et sw=4 sts=4
