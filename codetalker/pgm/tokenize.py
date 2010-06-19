#!/usr/bin/env python

from tokens import Token, EOF

def tokenize(tokens, text):
    while text.hasMore():
        for token in tokens:
            one = token.check(text)
            if one is not None:
                yield Token(token.name, one, text.lineno, text.charno)
                text.advance(len(one))
    yield EOF

# vim: et sw=4 sts=4
