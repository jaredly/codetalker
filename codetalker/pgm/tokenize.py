#!/usr/bin/env python

from tokens import Token, EOF
from errors import CodeTalkerException

class TokenError(CodeTalkerException):
    pass

def tokenize(tokens, text):
    while text.hasMore():
        for token in tokens:
            one = token.check(text)
            if one is not None:
                yield one
                break
        else:
            raise TokenError('no token matches the text at (%d, %d): "%s"' % (text.lineno,
                text.charno, text.text[text.at:text.at+10].encode('string_escape')))
        text.advance(len(one.value))

    yield EOF('')

# vim: et sw=4 sts=4
