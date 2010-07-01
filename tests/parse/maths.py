#!/usr/bin/env python

from codetalker.contrib.math import m, grammar
from codetalker.pgm.grammar import TokenError

import py.test

def test_1():
    assert 5 == m.from_string('2+3')



# vim: et sw=4 sts=4
