#!/usr/bin/env python

from magictest import MagicTest as TestCase, suite

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, CCOMMENT, NEWLINE, EOF, StringToken
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

class SYMBOL(StringToken):
    items = list('[]=-+/{}')

def start_one(rule):
    rule | star(ID)

def start_two(rule):
    rule | plus(ID)

def start_three(rule):
    rule | ("single", start_one)

def start_four(rule):
    rule | star(four_sub)

def four_sub(rule):
    rule | (ID, _or('+','=','-'), ID, _or(NEWLINE, EOF))


def make_grammar(start):
    return pgm.Grammar(start=start, tokens=[STRING, ID, NUMBER, CCOMMENT, SYMBOL, NEWLINE, EOF, WHITE], ignore=[WHITE, CCOMMENT])

def parse_test(start):
    grammar = make_grammar(start)
    def decor(func):
        def meta(self):
            return func(self, grammar)

tests = {
    start_one: [(
        '',
        'one',
        'one two',
        'many different ids and stuff',
    ), (
        'one 10',
    )],
    start_two: [(
        'one',
        'one two three four',
    ), (
        '',
        '10 23',
    )],
    start_three: [(
        'single',
        'single one',
        'single a b c d  d',
    ), (
        'one',
        'single 10',
    )],
    start_four: [(
        '',
        'a=b',
        'a+b',
        'a-b',
        'a=b\nb=c',
        'd+f\ng-e\na=e',
    ), (
        'a'
    )],
}

def check_parse(text, grammar):
    try:
        return grammar.process(text)
    except ParseError:
        return grammar.process(text, debug=True)

class SmallTest(TestCase):
    pass

def make_pass(grammar, text):
    def meta(self):
        try:
            return grammar.process(text)
        except ParseError:
            return grammar.process(text, debug=True)
    return meta

def make_fail(grammar, text):
    def meta(self):
        try:
            tree = grammar.process(text)
            self.fail('Expected "%s" to fail' % text.encode('string_escape'))
        except ParseError:
            pass
    return meta

for func, strings in tests.iteritems():
    grammar = make_grammar(func)
    name = func.__name__
    for i, good in enumerate(strings[0]):
        setattr(SmallTest, name + '_good_%d' % i, make_pass(grammar, good))
    for i, bad in enumerate(strings[1]):
        setattr(SmallTest, name + '_bad_%d' % i, make_fail(grammar, bad))

all_tests = suite(__name__)

# vim: et sw=4 sts=4
