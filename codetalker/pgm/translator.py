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
            def beta(node, scope=None):
                if node is None:
                    return None
                if self.scope:
                    return func(node, scope)
                else:
                    return func(node)
            return beta
        return meta

    def translate(self, tree, scope=None):
        if tree is None:
            return None
        if tree.__class__ not in self.register:
            if isinstance(tree, Token):
                return tree.value
            raise TranslatorException('no rule to translate %s' % tree.__class__.__name__)

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
            if self.defaults.keys() == ['scope']:
                scope = self.defaults['scope']
                for k, v in args.items():
                    setattr(scope, k, v)
            else:
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
