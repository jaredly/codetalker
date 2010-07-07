#!/usr/bin/env python
from tokens import INDENT, DEDENT
from errors import *

class Text:
    '''a small utility class in charge of serving up
    a body of text and keeping track of the line + char
    number.'''
    def __init__(self, text):
        self.charno = 1
        self.lineno = 1
        self.at = 0
        self.text = text
        self.current = self.text
        self.ln = len(text)
        self.specials = []

    def advance(self, num):
        lines = self.text[self.at:self.at+num].count('\n')
        if lines:
            self.charno = len(self.text[self.at:self.at+num].split('\n')[-1]) + 1
            self.lineno += lines
        else:
            self.charno += num
        self.at += num
        self.current = self.text[self.at:]

    def hasMore(self):
        return self.at < self.ln

import re

class IndentText(Text):
    '''a specialized Text class, which also keeps track
    of indentation -- outputs INDENT and DEDENT tokens'''
    def __init__(self, text):
        Text.__init__(self, text)
        self.indents = [0]

    def advance(self, num):
        if num == 1 and self.text[self.at:self.at+num] == '\n':
            next = self.text.find('\n', self.at+1)
            if self.text[self.at+1:next].strip():
                indent = white(self.text, self.at+1)
                if indent > self.indents[-1]:
                    self.specials = [INDENT('', self.lineno + 1, 0)]
                    self.indents.append(indent)
                elif indent < self.indents[-1]:
                    self.specials = []
                    while indent < self.indents[-1]:
                        self.specials.append(DEDENT('', self.lineno + 1, 0))
                        self.indents.pop(-1)
                    if indent != self.indents[-1]:
                        raise IndentError('invalid indent at line %d' % self.lineno)
        Text.advance(self, num)

def white(text, at=0):
    i = at
    l = len(text)
    while i < l and text[i] in ' \t':
        i += 1
    return i - at

# vim: et sw=4 sts=4
