#!/usr/bin/env python
import parser
from node import Node

def parse(text, lang, junk = ()):
    node = parser.parse(text, lang.tokens)
    tokens = tuple(t for t in node.tokens() if t.name not in junk)
    full = parser.parse(tokens, lang.main)
    full.childrenize()
    return tokens,full

# vim: et sw=4 sts=4
