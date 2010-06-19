#!/usr/bin/env python

from tokens import EOF

def tokenize(tokens, text):
    while len(text):
        for token in tokens:
            one = token.check(text)
            if one is not None:
                yield one
                text = text[len(one):]
    yield EOF

# vim: et sw=4 sts=4
