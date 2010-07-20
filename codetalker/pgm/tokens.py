#!/usr/bin/env python

from token import Token, ReToken

from codetalker.pgm.cgrammar import TSTRING, SSTRING, STRING, ID, NUMBER, INT, CCOMMENT, PYCOMMENT, WHITE, NEWLINE

import re

class SpecialToken(Token):
    '''a special token which is automatically provided by the parser'''
    @classmethod
    def check(cls, text):
        return 0

class EOF(SpecialToken):
    '''singleton -- special token for signifying the end of file'''

class INDENT(SpecialToken):
    '''used by the preprocessor to indicate the start of an indented block'''

class DEDENT(SpecialToken):
    '''used by the preprocessor to indicate the end of an indented block'''

# vim: et sw=4 sts=4
