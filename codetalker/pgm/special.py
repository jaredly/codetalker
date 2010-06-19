#!/usr/bin/env python

class Special:
    '''a special sub-rule for doing more complicated regular expression-like stuff'''
    def __init__(self, type, *items):
        self.type = type
        self.items = items

    @classmethod
    def factory(cls, name):
        def meta(*items):
            return cls(name, *items)
        return meta

star = Special.factory('star')
plus = Special.factory('plus')
_os = Special.factory('or')

# vim: et sw=4 sts=4
