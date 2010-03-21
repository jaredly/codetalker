#!/usr/bin/env python
import string
import sys
import re

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

class RxFirst:
    def __init__(self, rx):
        self.rx = re.compile(rx[2:-1])
    def __eq__(self, other):
        if isinstance(other, RxFirst):
            return other.rx == self.rx
        if type(other) != str:
            return NotImplemented
        return self.rx.match(other) is not None
    def __ne__(self, other):
        if isinstance(other, RxFirst):
            return other.rx == self.rx
        if type(other) != str:
            return NotImplemented
        return self.rx.match(other) is None

class Grammar:
    def __init__(self, filename, tokens = string.printable, extends = None):
        self.filename = filename
        self.original = open(filename).read()
        self.extends = extends
        self.tokens = tokens
        self.debug = False
        self.parse()

    def loadrules(self):
        raise NotImplementedError,'need to override this'

    def parse(self):
        self.rules = {}
        self.firsts = {}
        if self.extends:
            self.rules = self.extends.rules.copy()
        self.lines = {}
        if self.filename.endswith('er.txt'):
            self.debug = True
        self.loadrules()
        if self.debug:
            self.test_reachability()
        if self.debug:
            fail
        for name in self.rules:
            try:
                self.loadfirst('@'+name, 'base')
            except BNFException, e:
                print>>sys.stderr, "Error in %s" % self.filename
                print>>sys.stderr, '    %s' % e
                sys.exit(1)

    def test_reachability(self):
        at = 'start'
        found = set()
        for rule in self.rules:
            if rule in found:continue
            self.crawl_reach(rule, found)

        for rule in self.rules:
            if rule not in found:
                print 'unreachable rule "%s" at line %d' % (rule, self.lines[rule][0]+1)

    def crawl_reach(self, at, found):
        if at in self.tokens:return
        elif at not in self.rules:
            print>>sys.stderr,'undefined rule:',at
            return
        for line in self.rules[at]:
            for child in line:
                if child[0]=='@':
                    if child[1:] in found:continue
                    found.add(child[1:])
                    self.crawl_reach(child[1:], found)

    def loadfirst(self, name, parent):
        if name in self.firsts:return self.firsts[name]
        elif name == '!':
            ## means there was a '' in the rule; treat as epsilon
            return list(self.tokens)
        elif name[0] == '!':
            return [name[1]]
        elif name[0] == '@' and name[1:] in self.tokens:
            return [name[1:]]
        elif name[0] != '@':
            print self.tokens
            raise BNFException, 'invalid rule found in "%s", line %d for rule %s: %s' % (self.filename, 
                    self.lines[parent][0]+1, parent, name)
        elif name[1:] not in self.rules:
            raise BNFException, 'rule not found on line %d (parent=%s): %s' % (
                    self.lines[parent][0]+1, parent, name[1:])


        name = name[1:]
        chars = []
        self.firsts[name] = chars
        for child in self.rules[name]:
            if not child:
                continue
            chars.append(flatten(self.loadfirst(child[0], name)))
        return chars

# vim: et sw=4 sts=4
