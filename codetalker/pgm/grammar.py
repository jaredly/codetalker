#!/usr/bin/env python

from tokenize import tokenize

class Text:
    def __init__(self, text):
        self.charno = 1
        self.lineno = 1
        self.at = 0
        self.text = text
        self.ln = len(text)

    def advance(self, num):
        lines = self.text[self.at:self.at+num].count('\n')
        if lines:
            self.charno = len(self.text[at:at+num].split('\n')[-1])
            self.lineno += lines
        else:
            self.charno += num
        self.at += num

    def hasMore(self):
        return self.at < self.ln - 1

class Grammar:
    def __init__(self, start, tokens, ignore=[]):
        self.start = start
        self.tokens = tokens
        self.ignore = ignore

    def get_tokens(self, text):
        return tokenize(self.tokens, text)

    def process(self, text):
        text = Text(text)
        tokens = self.get_tokens(text)
        print list(tokens)

# vim: et sw=4 sts=4
