#!/usr/bin/env python
import parser

def parse(text, lang, junk = ('whites',)):
    node = parser.parse(text, lang.tokens)
    tokens = tuple(t for t in node.tokens() if t.name not in junk)
    full = parser.parse(tokens, lang.main)
    return full

# vim: et sw=4 sts=4
