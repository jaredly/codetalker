#!/usr/bin/env python
import parser
from node import Node

def parse(text, lang, junk = ('whites','comment','pp-line')):
    root, i, const = parser.parse(text, lang.tokens)
    tokens = list(node.children[0] for node in root.find('token'))
    #parser.debug = 1
    root, i, const = parser.parse(tokens, lang.main, ignore=junk)
    root.reparent()
    root.finalize()
    return root

# vim: et sw=4 sts=4
