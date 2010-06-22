#!/usr/bin/env python

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

# vim: et sw=4 sts=4
