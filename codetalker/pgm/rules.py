#!/usr/bin/env python

from errors import *
import tokens
import types
from special import Special
import inspect

class RuleLoader(object):
    __slots__ = ('grammar', 'options', 'dont_ignore', 'astAttrs', 'pass_single')
    def __init__(self, grammar):
        self.grammar = grammar
        self.options = []
        self.dont_ignore = False
        self.astAttrs = {}
        self.pass_single = False # single or multi

    def __or__(self, other):
        self.options.append(self.process(other))
        return self

    def add_option(self, other):
        self | other

    def process(self, what):
        if type(what) == str:
            return [what]
        elif inspect.isclass(what) and issubclass(what, tokens.Token):
            if what in self.grammar.tokens:
                return [-(self.grammar.tokens.index(what) + 1)]
            else:
                raise RuleError('invalid token found: %s' % what)
        elif type(what) == tuple:
            options = []
            for item in what:
                options += self.process(item)
            return options # flatten nested tuples
        elif type(what) == list:
            options = []
            for item in what:
                options += self.process(item)
            return [('?',) + tuple(options)]
        elif isinstance(what, Special):
            options = []
            for item in what.items:
                if what.char == '|':
                    options.append(tuple(self.process(item)))
                else:
                    options += self.process(item)
            return [(what.char,) + tuple(options)]
        elif type(what) == types.FunctionType:
            return [self.grammar.load_rule(what)]
        else:
            raise RuleError('invalid rule item found: %s' % what)

# vim: et sw=4 sts=4
