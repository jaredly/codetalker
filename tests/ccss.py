#!/usr/bin/env python

import magictest
from magictest import MagicTest as TestCase

class CCSSTest(TestCase):
    def importTest(self):
        from codetalker.pgm.ccss import grammar

    def smallparsing(self):
        from codetalker.pgm.ccss import grammar
        tree = grammar.process('''hello = world''')


all_tests = magictest.suite(__name__)

# vim: et sw=4 sts=4
