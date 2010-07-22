#!/usr/bin/env python

class CodeTalkerException(Exception):
    pass

class LineError(CodeTalkerException):
    def __init__(self, text, lineno, charno):
        Exception.__init__(self, text + ' at (%d, %d)' % (lineno, charno))
        self.lineno = lineno
        self.charno = charno

class ParseError(LineError):
    pass

class TokenError(LineError):
    pass

class AstError(CodeTalkerException):
    pass

class RuleError(CodeTalkerException):
    pass

# vim: et sw=4 sts=4
