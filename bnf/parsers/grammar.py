#!/usr/bin/env python
import string
import sys
import re

debug = False

class BNFException(Exception):
    pass

class RuleFirst:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if hasattr(other, 'name') and other.name == self.name:
            return True
        if type(other) == tuple and len(other)==1 and other[0]==self.name:
            return True
        return NotImplemented

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
        self.start = 'start'
        self.parse()

    def loadrules(self):
        raise NotImplementedError,'need to override this'

    def parse(self):
        self.rules = {}
        self.firsts = {}
        if self.extends:
            self.rules = self.extends.rules.copy()
        self.lines = {}
        #if self.filename.endswith('er.txt'):
        #    self.debug = True
        self.loadrules()

        errors = self.test_reachability()
        errors += self.test_ordering()
        errors += self.test_almost_dup()
        reach = self.check_circular(self.start)
        if reach:
            print 'front-end recursion found:',reach
            sys.exit(0)
        if errors>0:
            print>>sys.stderr, 'please correct the above errors'
            sys.exit(1)
        for name in self.rules:
            try:
                self.loadfirst('@'+name, 'base')
            except BNFException, e:
                print>>sys.stderr, "Error in %s" % self.filename
                print>>sys.stderr, '    %s' % e
                sys.exit(1)
    
    def test_almost_dup(self):
        errors = 0
        for rule in self.rules:
            for i,line in enumerate(self.rules[rule]):
                for other in self.rules[rule]:
                    if line is other:continue
                    for a in range(len(line)):
                        if a >= len(other):break
                        if line[a]!=other[a]:
                            break
                    if a>0:
                        pass#print 'you could optimize %d %s' % (self.lines[rule][0]+1, rule)
                        #errors += 1
        return errors

    def test_ordering(self):
        errors = 0
        for rule in self.rules:
            for i,line in enumerate(self.rules[rule]):
                for other in self.rules[rule][i+1:]:
                    for a in range(len(line)):
                        if a >= len(other):break
                        if line[a]!=other[a]:
                            break
                    else:
                        print 'there is a rule hidden behind a greedy other on line %s. rule %s' % (self.lines[rule][0]+1, rule)
                        errors += 1
        return errors

    def test_reachability(self):
        at = self.start
        found = set([at])
#        for rule in self.rules:
#            if rule in found:continue
#            self.crawl_reach(rule, found)
        errors = self.crawl_reach(at,found)

        for rule in self.rules:
            errors += self.check_exists(rule)
            if rule not in found and rule in self.lines:
                if debug:print 'unreachable rule "%s" at line %d' % (rule, self.lines[rule][0]+1)
        return errors

    def check_exists(self, rule):
        errors = 0
        for line in self.rules[rule]:
            for child in line:
                if child[0]=='@':
                    if child[1:] not in self.rules and child[1:] not in self.tokens:
                        print 'undefined rule:',child[1:],child,'in',rule
                        print line
                        errors += 1
                elif child[0] not in '!*?:+':
                    print 'invalid child: "%s" in %s' % (child, rule)
                    errors += 1
        return errors
    
    def crawl_reach(self, at, found):
        errors = 0
        if at in self.tokens:return errors
        elif at not in self.rules:
            print>>sys.stderr,'undefined rule:',at
            return 1
        for line in self.rules[at]:
            for child in line:
                if child[0]=='@':
                    if child[1:] in found:continue
                    found.add(child[1:])
                    errors += self.crawl_reach(child[1:], found)
        return errors

    def check_circular(self, rule=None, stack = ()):
        if rule is None:
            rule = self.start
        if rule in stack:
            raise Exception,'recursion! %s '%(stack+(rule,),)
            return stack+(rule,)
        elif rule in self.tokens:
            return False
        ret = []
        kids = set()
        for line in self.rules[rule]:
            if line[0][0]=='@':
                kids.add(line[0][1:])
                break

        for child in kids:
            res = self.check_circular(child, stack+(rule,))
            if res:
                ret.append(res)

        if len(ret) == 1:
            return ret[0]
        return ret

    def loadfirst(self, name, parent):
        if name == '!':
            ## means there was a '' in the rule; treat as epsilon
            return list(self.tokens)
        elif name[0] == '!':
            return [name[1]]
        elif name[0] == '@' and name[1:] in self.tokens:
            return [RuleFirst(name[1:])]
        elif name[0] != '@':
            print self.tokens
            raise BNFException, 'invalid rule found in "%s", line %d for rule %s: %s' % (self.filename, 
                    self.lines[parent][0]+1, parent, name)
        elif name[1:] not in self.rules:
            raise BNFException, 'rule not found on line %d (parent=%s): %s' % (
                    self.lines[parent][0]+1, parent, name[1:])

        name = name[1:]
        if self.firsts.has_key(name):return self.firsts[name]
        self.firsts[name] = []
        #print>>open('first.log','aw'), 'firsting',name
        for child in self.rules[name]:
            if not child:
                continue
            f = self.loadfirst(child[0], name)
            i = 0
            while len(child)>i+2 and child[i+1] in '*?':
                if child[i+2] == '?':
                    i += 1
                f += self.loadfirst(child[i+2], name)
                i+=2
            f = flatten(f)
            self.firsts[name].append(f)
        #print>>open('first.log','aw'), 'from ',name, self.firsts[name]
        return self.firsts[name]

# vim: et sw=4 sts=4
