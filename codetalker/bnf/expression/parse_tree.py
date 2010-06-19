#!/usr/bin/env python

class ParseNode:
    def __init__(self, rule, rules):
        self.parent = None
        self.rule = rule
        self.rules = rules
        # self.child = rule.first_child()
        # self.child_state = self.child.new_state()
        self.children = []

    def addChild(self, node):
        node.parent = self
        self.children.append(node)

    def addChildren(self, nodes):
        [self.addChild(node) for node in nodes]

    def advance(self, char):
        if self.child.advance():
            pass

    def done(self):
        return not self.child.hasNext()

    def dive(self):
        if isinstance(self.child, ):
            pass

class TextStream:
    def __init__(self, text):
        self.pos = 0
        self.lineno = 0
        self.charno = 0

    def get(self):
        return self.text[self.pos]
    
    def advance(self):
        c = self.text[self.pos]
        if c == '\n':
            self.lineno += 1
            self.charno = 0
        else:
            self.charno += 1
        self.pos += 1
        if self.pos >= len(self.text):
            raise Exception('Npoe. too long')

    def save_state(self):
        return [self.pos, self.lineno, self.charno]
    
    def restore_state(self, state):
        self.pos, self.lineno, self.charno = state

def parse_rule(rule, rules, text):
    c = text.get()
    node = ParseNode(rule.name)
    state = text.save_state()
    for i, first in rule.firsts:
        text.restore_state(state)
        if c in first:
            cnodes = parse_children(rule, rules, rule.options[i])
            node.addChildren(cnodes)
            break
    return node

def parse_children(rule, rules, children):
    '''pase some children'''



def parse(text, func, grammar):
    base = ParseNode(None, parent, rule, rules)
    node = base.dive()
        


# vim: et sw=4 sts=4
