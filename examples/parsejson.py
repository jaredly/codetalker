#!/usr/bin/env python

import os
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
    if not os.path.isfile(sys.argv[1]):
        print 'Error: arg must be a file path'
        sys.exit(1)
    print 'parsing file: %s' % (sys.argv[1],)
    parse(open(sys.argv[1]).read())
else:
    print 'reading from stdin...'
    parse(sys.stdin.read())

# vim: et sw=4 sts=4
