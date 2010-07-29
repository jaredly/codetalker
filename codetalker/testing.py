#!/usr/bin/env python

from codetalker.pgm.errors import ParseError, TokenError

def parse_rule(name, grammar):
    parts = name.split('.')
    mod = __import__(name, fromlist=['__dict__'])
    def meta(rule, passing=(), failing=()):
        def _pass(string):
            def meta():
                grammar.get_parse_tree(string, start=rule)
            return meta
        def _fail(string):
            def meta():
                try:
                    res = grammar.get_parse_tree(string, start=rule)
                except (ParseError, TokenError), e:
                    pass
                else:
                    raise AssertionError('parsing was supposed to fail for', string, res)
            return meta
        for i, string in enumerate(passing):
            fn = _pass(string)
            mod.__dict__['test_pass_rule_%s #%d' % (rule.__name__, i)] = fn
        for i, string in enumerate(failing):
            fn = _fail(string)
            mod.__dict__['test_fail_rule_%s #%d' % (rule.__name__, i)] = fn
    return meta


# vim: et sw=4 sts=4
