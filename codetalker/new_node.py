#!/usr/bin/env python

class Stream:
    def __init__(self):
        self.lineno = 0
        self.charno = 0

class CharStream:
    def __init__(self, text):
        self.lineno = 0
        self.charno = 0
        self.i = -1
        self.text = text
    def next(self):
        self.i += 1
        if self.i >= len(self.text):
            raise StopIteration
        if self.text[i] == '\n':
            self.lineno += 1
            self.charno = 0
        else:
            self.charno += 1
        return self.text[i]

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = -1
        self.lineno = 0
        self.charno = 0
    def next(self):
        self.i += 1
        if self.i >= len(self.tokens):
            raise StopIteration
        self.lineno = self.tokens[self.i].lineno
        self.charno = self.tokens[self.i].charno
        return self.tokens[self.i]
    def __iter__(self):
        return TokenStream(self.tokens)



# vim: et sw=4 sts=4
