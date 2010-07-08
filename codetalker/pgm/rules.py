#!/usr/bin/env python

from errors import *
import tokens
import types
from special import Special
import inspect

class RuleLoader(object):
    __slots__ = ('grammar', 'options', 'token', 'dont_ignore', 'astAttrs', 'pass_single', 'builder')
    def __init__(self, grammar, token=False):
        self.grammar = grammar
        self.options = []
        self.token = token
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
        elif not self.token and what in self.grammar.tokens:
            return [-(self.grammar.tokens.index(what) + 1)]
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
            if self.token:
                return [self.grammar.load_token(what)]
            else:
                return [self.grammar.load_rule(what)]
        else:
            raise RuleError('invalid rule item found: %s' % what)

    def rule(self):
        return Rule(options=self.options, dont_ignore=self.dont_ignore)

class Rule(object):
    __slots__ = ('options', 'dont_ignore')
    def __init__(self, **args):
        for arg in args:
            setattr(self, arg, args[arg])

# vim: et sw=4 sts=4
