#!/usr/bin/env python
import parser

def parse(text, lang):
    node = parser.parse(text, lang.tokens)
    tokens = node.tokens()
    full = parser.parse(tokens, lang.main)
    return full

# vim: et sw=4 sts=4
