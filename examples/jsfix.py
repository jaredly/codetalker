#!/usr/bin/env python
'''
    fixes a javascript file according to JSLint's specs
'''
import codetalker
from codetalker.bnf import js
from codetalker.node import TextNode, Node

import os,sys

space = TextNode(' ', -1)
br = TextNode('\n', -1)
tab = TextNode('    ', -1)

def pad(node, what=space):
    lpad(node, what)
    rpad(node, what)

def lpad(node, what=space):
    p = node.prevNode()
    if p and not str(p)[-1].isspace():
        node.insertBefore(what.clone())

def rpad(node, what=space):
    n = node.nextNode()
    if n and not str(n)[0].isspace():
        node.appendAfter(what.clone())

def fix(root):
    fix_braces(root)
    strip_white(root)
    fix_indent(root)
    fix_switch(root)
    fix_else(root)
    fix_nitspace(root)

def compoundize(old):
    st = Node('statement', old.index, old.final, (old,), old.pos)
    c = Node('compound-st', old.index, old.final, (TextNode('{', -1), st, TextNode('}', -1)), old.pos)
    return c


def fix_braces(root):
    sts = list(root.find('if-statement,iteration-st, if-tail'))
    for node in sts:
        while len(node.children) == 1:
            node = node.children[0]
        for child in node.children:
            if isinstance(child, Node) and child.name == 'statement' and child.children[0].name != 'compound-st':
                old = child.children[0]
                child.children = [compoundize(old)]
                child.dirty()

def strip_white(root):
    whites = list(root.find('whites'))
    for node in whites:
        p = node.prevNode()
        n = node.nextNode()
        if p and n:
            if str(p)[-1].isalnum() and str(n)[0].isalnum():
                node.children = [TextNode(' ', node.index)]
                node.dirty()
                continue
        node.remove()

def fix_indent(root):
    for node in root.find('compound-st'):
        if len(node.children) > 2:
            node.insert(1, br.clone())
    for node in root.find('statement'):
        if str(node.nextNode())[0]!='\n':
            node.appendChild(br.clone())
    for comp in root.find('compound-st'):
        for node in comp.find('statement'):
            if node.children[0].name == 'compound-st':
                node.children[0].insert(-1, tab.clone())
            else:
                node.insert(0, tab.clone())

def fix_switch(root):
    for node in root.find('switch-body'):
        node.insert(1, br.clone())
    for node in root.find('case-sub,default-sub'):
        node.insert(0, tab.clone())

    for node in root.find('switch-sub-body'):
        node.insert(0, br.clone())
        for child in node.find('statement'):
            if child.children[0].name == 'compound-st':
                pass
            else:
                child.insert(0, tab.clone())
                child.insert(0, tab.clone())
        for child in node.find('compound-st'):
            child.insert(-1, tab.clone())
            child.insert(-1, tab.clone())

def fix_else(root):
    for node in root.find('if-tail'):
        p = node.prevNode()
        while p and not str(p).strip(' \t'):
            o = p
            p = p.prevNode()
            o.remove()
        if str(p)[-1] == '\n':
            br = p.children[-1]
            if str(br).strip(' \t') != '\n':
                continue
            p.children[-1].remove()
        pad(node.children[0])

def fix_nitspace(root):
    for node in root.find(
            'and-op,or-op,bit-or-op,bit-and-op,'
            'compare-op,compare2-op,shift-op,'
            'add-op,mul-op,assignment-op,declare-op'):
        pad(node)
    for node in root.sfind(','):
        rpad(node.parent)
    for node in root.sfind(';'):
        rpad(node.parent)

    for node in root.find('function-args,paren-expression'):
        pad(node)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'usage: parse_js.py file.js -q'
        sys.exit(1)
    if len(sys.argv) == 3:
        filen, op = sys.argv[1:]
    else:
        filen, = sys.argv[1:]
        op = None
    text = open(filen).read()
    root = codetalker.parse(text, js)
    fix(root)
    print codetalker.node.str_node(root)
    #print codetalker.node.xml_node(root, 30)

# vim: et sw=4 sts=4
