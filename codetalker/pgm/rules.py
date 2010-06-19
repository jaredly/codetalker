#!/usr/bin/env python

from errors import *

class RuleLoader:
    def __init__(self, grammar):
        self.grammar = grammar
        self.options = []

    def __or__(self, other):
        self.options.append(self.process(other))

    def process(self, what):
        if type(what) == str:
            self.options.append(other)

# vim: et sw=4 sts=4
