#!/usr/bin/env python
'''Prettyfy JSON

An example included with codetalker. Outputs prettyfied (with whitespace) 
json that is logically equivalent to the input json. Dies on invalid input.

usage::
    python examples/prettyjson.py some/file.json

While trying to unserstand this, it is helpful to have bnf/json/json.bnf open
to look at the grammar structure.
'''

import codetalker
from codetalker.bnf import json
from codetalker.node import TextNode

def prettyfy(node):
    while node.name in ('start','value'):
        node = node.children[0]
    if node.name != 'object':
        print 'Need an object at the start'
        sys.exit(1)

    # remove whitespace
    for w in node.find('whites'):
        w.remove()

    lbreak = TextNode('\n', -1)

    # put a line break after the commas in objects and lists
    for n in node.find('object-tail,list-tail'):
        n.insert(1, lbreak.clone())

    # put a line-break at the beginning and end of the
    # list and object contents
    for body in node.find('object-contents,list-contents'):
        body.insert(0,lbreak.clone())
        body.appendChild(lbreak.clone())

    # indent the contents of objects and lists
    for body in node.find('object-contents,list-contents'):
        for nline in body.sfind('\n'):
            nline.children[0] += '    '

    # dedent the final } and ] of objects and lists
    # (I know that the last child will be a line-break followed
    #  by indenting spaces, because I put it there on line 39)
    for body in node.find('object-contents,list-contents'):
        last = body.children[-1]
        last.children[0] = last.children[0][:-4]

    return node

if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        print 'usage: json.py somefile.json'
        sys.exit(1)
    text = open(sys.argv[1]).read()
    root = codetalker.parse(text, json)
    ## print the prettified json
    print prettyfy(root)

# vim: et sw=4 sts=4
