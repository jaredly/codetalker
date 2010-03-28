#!/usr/bin/env python
import parser
from node import Node

def parse(text, lang, junk = (), debug_tokens=False, debug_main=False):
    root, i, const = parser.parse(text, lang.tokens)
    if debug_tokens:
        parser.debug = 1
    tokens = list(node.children[0] for node in root.find('token'))
    if debug_main:
        parser.debug = 1
    root, i, const = parser.parse(tokens, lang.main)
    return root

# vim: et sw=4 sts=4
