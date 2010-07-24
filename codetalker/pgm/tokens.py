#!/usr/bin/env python

from token import Token, ReToken

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

from codetalker.cgrammar import TSTRING, SSTRING, STRING, ID, NUMBER, INT, HEX, CCOMMENT, CMCOMMENT, PYCOMMENT, WHITE, NEWLINE, ANY, CharToken, StringToken, IdToken, IIdToken

__all__ = ['Token', 'ReToken', 'CharToken', 'StringToken', 'IdToken', 'IIdToken',
           'TSTRING', 'SSTRING', 'STRING', 'ID', 'NUMBER', 'INT', 'HEX', 'ANY',
           'CCOMMENT', 'CMCOMMENT', 'PYCOMMENT', 'WHITE', 'NEWLINE', 'INDENT', 'DEDENT', 'EOF']

# vim: et sw=4 sts=4
