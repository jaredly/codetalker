#!/usr/bin/env python

from tokens import Token
import types
import inspect
import copy
from nodes import AstNode

from errors import CodeTalkerException

class TranslatorException(CodeTalkerException):
    pass

class Translator:
    def __init__(self, grammar, **defaults):
        self.grammar = grammar
        self.register = {}
        self.scope = True
        if not defaults:
            self.scope = False
        self.defaults = defaults

    def translates(self, what):
        def meta(func):
            self.register[what] = func
        return meta

    def translate(self, tree, scope=None):
        if self.scope:
            return self.register[tree.__class__](tree, scope)
        else:
            return self.register[tree.__class__](tree)

    def from_string(self, text, **args):
        # assert text == str(self.grammar.process(text))
        tree = self.grammar.get_ast(text)
        '''
        ptree = self.grammar.process(text)
        if ptree is None:
            return None
        tree = self.grammar.to_ast(ptree)
        '''
        return self.from_ast(tree, **args)

    def from_ast(self, tree, **args):
        if self.scope:
            stuff = copy.deepcopy(self.defaults)
            stuff.update(args)
            Scope = type('Scope', (), {})
            scope = Scope()
            for k,v in stuff.iteritems():
                setattr(scope, k, v)
            return self.translate(tree, scope)
        elif args:
            raise Exception('no scope -- cannot define variables: %s' % (args,))
        else:
            return self.translate(tree)

# vim: et sw=4 sts=4
