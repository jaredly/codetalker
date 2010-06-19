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
            self.charno = len(self.text[self.at:self.at+num].split('\n')[-1])
            self.lineno += lines
        else:
            self.charno += num
        self.at += num

    def hasMore(self):
        return self.at < self.ln

class Grammar:
    def __init__(self, start, tokens, ignore=[]):
        self.start = start
        self.tokens = tokens
        self.ignore = ignore
        self.load_grammar()

    def load_grammar(self):
        self.rules = []
        self.rule_dict = {}
        self.load_func(self.start)

    def load_func(self, func):
        if func in self.rule_dict:
            return self.rule_dict[func]
        num = len(self.rules)
        self.rule_dict[func] = num
        self.rules.append(RuleLoader(self))
        func(self.rules[-1])
        return num

    def get_tokens(self, text):
        return tokenize(self.tokens, text)

    def process(self, text):
        text = Text(text)
        tokens = self.get_tokens(text)
        print list(tokens)

# vim: et sw=4 sts=4
