#!/usr/bin/env python

import magictest
from magictest import MagicTest as TestCase

from codetalker.pgm.ccss import grammar
from codetalker.pgm.grammar import Text

class CCSSTest(TestCase):
    def tokens(self):
        text = Text('hello = world')
        tokens = list(grammar.get_tokens(text))
        self.assertEqual(len(tokens), 6)
        self.assertEqual(tokens[2].charno, 7)
        self.assertEqual(tokens[-2].val, 'world')
    def token_lines(self):
        text = Text('hello\nworld = 6')
        tokens = list(grammar.get_tokens(text))
        self.assertEqual(len(tokens), 8)
        self.assertEqual(tokens[-2].lineno, 2)


all_tests = magictest.suite(__name__)

# vim: et sw=4 sts=4
