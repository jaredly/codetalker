#!/usr/bin/env python
from codetalker.parser import Node
from codetalker.bnf import c as grammar
import codetalker

def prettyfy(full):
    space = Node(' ',-1,True)
    lbreak = Node('\n',-1,True)
    tab = Node('    ',-1,True)
    [n.appendChild(space) for n in full.getElementsByTagName('type')]
    [n.appendChild(space) for n in full.getElementsByTagName(',')]

    [n.appendChild(lbreak) for n in full.getElementsByTagName('embedded-statement') if not n.children[0].name=='block']
    [n.appendChild(lbreak) for n in full.getElementsByTagName('declaration-statement')]
    for block in full.getElementsByTagName('block'):
        block.children.insert(1,lbreak)
        block.children.insert(0,space)
        for exp in block.getElementsByTagName('declaration-statement'):
            exp.children.insert(0,tab)
        for exp in block.getElementsByTagName('embedded-statement'):
            if exp.children[0].name == 'block':continue
            exp.children.insert(0,tab)
        for exp in block.getElementsByTagName('block'):
            if exp is block:continue
            if len(exp.children)>2:
                exp.children.insert(-1,tab)
    for node in full.gETN('assignment-operator'):
        node.appendChild(space)
        node.children.insert(0,space)
    for list_type in ('parameter-modifier',
            'fixed-parameter-tail',
            'argument-list-tail',
            'named-argument-tail',
            'expression-list-tail',
            'argument-tail',
            'positional-argument-tail',
            'formal-p-right',
            'local-variable-declarator-list',
            'constant-declarator-tail'):
        for node in full.getElementsByTagName(list_type):
            node.children.insert(1,space)
    print full

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: parse.py [code file]'
        sys.exit(1)
    code, = sys.argv[1:]

    full = codetalker.parse(open(code).read(), grammar)
    print prettyfy(full)



# vim: et sw=4 sts=4
