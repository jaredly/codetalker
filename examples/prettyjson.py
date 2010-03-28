#!/usr/bin/env python
import codetalker
from codetalker.bnf import json
from codetalker.node import TextNode

def prettyfy(node):
    while node.name in ('start','value'):
        node = node.children[0]
    if node.name != 'object':
        print 'Need an object at the start'
        sys.exit(1)
    for w in node.find('whites'):
        w.remove()
    for n in node.find('object-tail,list-tail'):
        n.insert(1, TextNode('\n', n.index))
    for body in node.find('object-contents,list-contents'):
        body.insert(0,TextNode('\n', body.index))
        body.appendChild(TextNode('\n', body.index))
    for body in node.find('object-contents,list-contents'):
        for nline in body.sfind('\n'):
            nline.children[0] += '    '
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
    print prettyfy(root)

# vim: et sw=4 sts=4
