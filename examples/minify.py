#!/usr/bin/env python

import codetalker
from codetalker.bnf import c

from codetalker.nnode import TextNode

import os,sys
BASE = os.path.dirname(__file__)

def remove_whitespace(filename):
    text = open(filename).read()
    root = codetalker.parse(text, c)
    ## remove comments
    [w.remove() for w in root.find('comment')]
    ## remove all whitespace that doesnt come between two words
    ## (we don't want to change 'int foo' to 'intfoo')
    whites = list(root.find('whites'))
    for node in whites:
        p = node.prevNode()
        n = node.nextNode()
        if p and n:
            pc = str(p)[-1] # last char of the previous
            nc = str(n)[0]  # first char of the next
            if pc.isalnum() and nc.isalnum():
                # if it is between two words, make it contain only a
                # single space
                node.children = [TextNode(' ',node.index)]
                # mark the node as 'dirty'; we changed the children
                # -- nodes cache their string exapnsion
                node.dirty()
                continue
        # otherwise remove!
        node.remove()
    ## print the root, outputting our code!
    print root

if __name__=='__main__':
    if len(sys.argv) != 2:
        print 'usage: white.py somefile.c'
        sys.exit(1)
    remove_whitespace(sys.argv[1])


# vim: et sw=4 sts=4
