#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.tokens import *
from codetalker.pgm.special import *

def start(rule):
    rule | plus


# vim: et sw=4 sts=4
