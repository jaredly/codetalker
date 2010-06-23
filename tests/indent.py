#!/usr/bin/env python

from magictest import MagicTest as TestCase, suite

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, SYMBOL, CCOMMENT, NEWLINE, EOF, INDENT, DEDENT
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError
from codetalker.pgm.text import IndentText
from codetalker.pgm.tokenize import tokenize

class IndentTest(TestCase):
    def tokens(self):
        text = IndentText("hi\n and\n\n more\nstuff")
        tokens = tuple(tokenize([ID, WHITE, NEWLINE], text))
        self.assertEqual(len(tokens), 13)
        self.assertEqual(tokens[2].__class__, INDENT)
        self.assertEqual(tokens[-3].__class__, DEDENT)

all_tests = suite(__name__)

# vim: et sw=4 sts=4
