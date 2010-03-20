#!/usr/bin/env python
import string

class BNFException(Exception):
    pass

def flatten(lst, seen = ()):
    """flatten a nested list"""
    seen += (lst,)
    res = []
    for item in lst:
        if item in seen:continue
        if type(item) in (tuple,list):
            res += list(flatten(item))
        else:
            res.append(item)
            seen += (item,)
    return res

class Grammar:
    def __init__(self, filename, tokens = string.printable, extends = None):
        self.filename = filename
        self.original = open(filename).read()
        self.extends = extends
        self.tokens = tokens
        self.parse()

    def loadrules(self):
        raise NotImplementedError,'need to override this'
    
    def rulesplit(self, name):
        raise NotImplementedError,'need to override this'

    def parse(self):
        self.rules = {}
        self.firsts = {}
        if self.extends:
            self.rules = self.extends.rules.copy()
        self.lines = {}
        self.loadrules()
        for name in self.rules:
            self.loadfirst(name, 'base')

    def loadfirst(self, name, parent):
        if name in self.firsts:return self.firsts[name]
        elif name == "''":return ["'"]
        elif name.startswith("'"):
            return [name.strip("'")[0]]
        elif name == 'e':
            return list(self.tokens)
        elif name in self.tokens:
            return [name]
        elif name not in self.rules:
            print self.tokens
            raise Exception, 'invalid rule found in "%s", line %d: %s' % (self.filename, 
                    self.lines[parent][0], name)

        chars = []
        self.firsts[name] = chars
        for child in self.rules[name]:
            if not child:
                continue
            chars.append(flatten(self.loadfirst(child[0], name)))
        return chars


# vim: et sw=4 sts=4
