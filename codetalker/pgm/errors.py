#!/usr/bin/env python

class CodeTalkerException(Exception):
    def __init__(self, text, lineno, charno):
        Exception.__init__(self, text + ' at (%d, %d)' % (lineno, charno))

class ParseError(CodeTalkerException):
    pass

class TokenError(CodeTalkerException):
    pass

class RuleError(CodeTalkerException):
    pass

# vim: et sw=4 sts=4
