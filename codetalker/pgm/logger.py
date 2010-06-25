#!/usr/bin/env python

import sys

DEBUG = False

class Logger:
    def __init__(self, output=True):
        self.indent = 0
        self.output = output
        self.lines = []

    def quite(self):
        self.output = False

    def loud(self):
        self.output = True

    def write(self, text):
        text = ' '*self.indent + text
        if self.output:
            sys.stdout.write(text)
        self.lines.append(text)

logger = Logger(DEBUG)

# vim: et sw=4 sts=4
