#!/usr/bin/env python

import sys
from codetalker.contrib.json import loads
from codetalker.pgm.errors import ParseError, TokenError

def parse(text):
    try:
        print loads(text)
    except (TokenError, ParseError), e:
        if text:
            print>>sys.stderr, text.splitlines()[e.lineno-1]
        else:
            print>>sys.stderr
        print>>sys.stderr, ' '*(e.charno-1)+'^'
        print>>sys.stderr, "Invalid Syntax:", e
    

if len(sys.argv) > 1:
    parse(sys.argv[1])
else:
    print 'reading from stdin...'
    parse(sys.stdin.read())

# vim: et sw=4 sts=4
