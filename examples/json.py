#!/usr/bin/env python
import codetalker
from codetalker.bnf import json

def collapse(node):
    if node.name == 'value':
        return collapse(node.children[0])

    elif node.name == 'number':
        lit = str(node)
        if '.' in lit:
            return float(lit)
        return int(lit)

    elif node.name == 'string':
        return str(node)[1:-1].decode('string_escape')

    elif node.name in ('list', 'object'):
        return collapse(node.children[1])

    elif node.name == 'list-contents':
        if not node.children:
            return []
        return [collapse(node.children[0])] + \
                list(collapse(x.children[1]) for x in node.children[1:]\
                                                    if len(x.children)==2)

    elif node.name == 'object-contents':
        obj = {}
        if len(node.children)==0:return {}
        return dict(((collapse(node.children[0]),collapse(node.children[2])),) +
                tuple((collapse(x.children[1]),collapse(x.children[3])) \
                        for x in node.children[3:] if len(x.children)==4))

    elif node.name == 'tfn':
        return {'true':True,'false':False,'null':None}[str(node)]

    raise Exception,"don't know how to deal w/ this: %s" % node.name


def loads(text):
    node = codetalker.parse(text, json)
    return collapse(node.children[0])
    
if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print 'usage: json.py somefile.json'
        sys.exit(1)
    print loads(open(sys.argv[1]).read())
# vim: et sw=4 sts=4
