#!/usr/bin/env python

from tokens import Token, EOF
from errors import TokenError

def tokenize(tokens, text):
    '''a generator to split some text into tokens'''
    while text.hasMore():
        if text.specials:
            for special in text.specials:
                yield special
            text.specials = []
        for i, token in enumerate(tokens):
            one = token.check(text)
            if one is not None:
                one.which = i
                yield one
                break
        else:
            raise TokenError('no token matches the text at (%d, %d): "%s"' % (text.lineno,
                text.charno, text.text[text.at:text.at+10].encode('string_escape')))
        text.advance(len(one.value))

# vim: et sw=4 sts=4
