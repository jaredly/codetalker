#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import *
from codetalker.pgm.errors import *

def noop(rule):
    rule | EOF

def just_tokenize(*tokens):
    g = pgm.Grammar(noop, tokens)
    def meta(text):
        _tokens = g.get_tokens(text)
        assert ''.join(tok.value for tok in _tokens) == text
        return _tokens
    return meta

def make_fail(fn, text):
    def meta():
        try:
            res = fn(text)
        except TokenError:
            pass
        else:
            raise AssertionError('was supposed to fail while tokenizing \'%s\' (got %s)' % (text.encode('string_escape'), res))
    return meta

def make_test(fn, text, expected=None):
    if type(expected) == int:
        num = expected
        expected = None
    else:
        num = len(expected)
    def meta():
        tokens = fn(text)
        if num:
            assert len(tokens) == num
        if expected is not None:
            for tok, cls in zip(tokens, expected):
                assert isinstance(tok, cls)
    return meta

def make_tests(globs, name, tokenize, tests):
    print 'hi'
    for i, (string, expected) in enumerate(tests):
        globs['test %s #%d' % (name, i)] = make_test(tokenize, string, expected)

def make_fails(globs, name, tokenize, tests):
    for i, string in enumerate(tests):
        globs['test %s (fail) #%d' % (name, i)] = make_fail(tokenize, string)


# vim: et sw=4 sts=4
