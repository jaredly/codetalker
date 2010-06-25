#!/usr/bin/env python

from tokens import Token
import types
import inspect

from errors import CodeTalkerException

class TranslatorException(CodeTalkerException):
    pass

class Scope:
    pass

class Translator:
    def __init__(self, grammar):
        self.grammar = grammar
        self.register = {}

    def translates(self, what):
        if inspect.isclass(what) and issubclass(what, Token) and what in self.grammar.tokens:
            what = -(self.grammar.tokens.index(what) + 1)
        elif what in self.grammar.real_rules:
            what = self.grammar.real_rules[what]
        else:
            raise TranslatorException('Unexpected translation target: %s' % what)
        def meta(func):
            self.registers[what] = func
        return meta

    def translate(self, tree, scope):
        if tree._type not in self.register:
            if tree._type >= 0:
                raise TranslatorException('unknown rule to translate (%s)' % self.grammar.rule_names[tree._type])
            else:
                raise TranslatorException('unknown token to translate (%s)' % self.grammar.tokens[-(tree._type + 1)])
        return self.register[tree._type](tree, scope)

    def from_source(self, text, **args):
        tree = self.grammar.process(text)
        return self.from_ast(tree, **args)

    def from_ast(self, tree, **args):
        Scope = type('Scope', (), {'__slots__': tuple(args.keys())})
        scope = Scope()
        for k,v in args.iteritems():
            setattr(scope, k, v)
        return self.translate(tree, scope)

# vim: et sw=4 sts=4
