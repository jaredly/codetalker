#!/usr/bin/env python

from tokenize import tokenize

class Grammar:
    def __init__(self, start, tokens, ignore=[]):
        self.start = start
        self.tokens = tokens
        self.ignore = ignore

    def process(self, text):
        tokens = tokenize(self.tokens, text)
        print tokens

# vim: et sw=4 sts=4
