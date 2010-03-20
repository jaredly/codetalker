#!/usr/bin/env python
import codetalker
from codetalker.bnf import json

def collapsenode(node):
    if node.name == '<value>':
        return collapsenode(node.children[0])
    elif node.name == '<number>':
        if '.' in node:
            return float(str(node))
        return int(str(node))
    elif node.name == '<string>':
        return str(node)[1:-1]
    elif node.name in ('<list>', '<object>'):
        return collapsenode(node.children[1])
    elif node.name == '<list contents>':
        if len(node.children)==1:return []
        return [collapsenode(node.children[0])] + list(collapsenode(x.children[1]) for x in node.children[1:] if len(x.children)==2)
    elif node.name == '<object contents>':
        obj = {}
        if len(node.children)==1:return {}
        return dict(((collapsenode(node.children[0]),collapsenode(node.children[2])),) +
                tuple((collapsenode(x.children[1]),collapsenode(x.children[3])) for x in node.children[3:] if len(x.children)==4))
    elif node.name == '<tfn>':
        return {'true':True,'false':False,'null':None}[str(node)]
    raise Exception,"don't know how to deal w/ this: %s" % node.name


def loads(text):
    node = codetalker.parse(text, json)
    return collapsenode(node.children[0])
    
if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print 'usage: json.py somefile.json'
        sys.exit(1)
    print loads(open(sys.argv[1]).read())
# vim: et sw=4 sts=4
