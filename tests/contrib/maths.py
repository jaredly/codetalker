#!/usr/bin/env python

from __future__ import division
from codetalker.contrib.math import evaluate

strings = (
    '1',
    '1+2',
    '2-3',
    '1.5e10-24',
    '15.0/45**2',
    '(1+2)/3-4*(2+3e-4)'
)

def make(exp):
    def meta():
        assert eval(exp) == evaluate(exp)
    return meta

for exp in strings:
    globals()['test_math "%s"' % exp] = make(exp)

# vim: et sw=4 sts=4
