#!/usr/bin/env python

class Special:
    '''a special sub-rule for doing more complicated regular expression-like stuff'''
    def __init__(self, *items):
        self.items = items

class star(Special):
    char = '*'
class plus(Special):
    char = '+'
class _or(Special):
    char = '|'
class qstart(Special):
    char = '*?'
class qplus(Special):
    char = '+?'

def commas(item):
    return (item, star(',', item), [','])

# vim: et sw=4 sts=4
