#!/usr/bin/env python
from codetalker.parser import Node
from codetalker.bnf import c as grammar
import codetalker

'''
to prettyfy c:


'''


def prettyfy(full):
    space = Node(' ',-1,True)
    lbreak = Node('\n',-1,True)
    tab = Node('    ',-1,True)
    [n.appendChild(space) for n in full.find('type')]
    [n.appendChild(space) for n in full.find('return-type') if n.children[0].name!='type']
    [n.appendChild(space) for n in full.find(',')]

    [n.appendChild(lbreak) for n in full.find('embedded-statement') if not n.children[0].name=='block']
    [n.appendChild(lbreak) for n in full.find('declaration-statement')]
    [n.appendChild(lbreak) for n in full.find('interface-member-declaration')]
    for block in full.find('block'):
        block.children.insert(1,lbreak)
        block.children.insert(0,space)
        for exp in block.find('comment'):
            exp.children.insert(0,tab)
        for exp in block.find('declaration-statement'):
            exp.children.insert(0,tab)
        for exp in block.find('embedded-statement'):
            if exp.children[0].name == 'block':continue
            exp.children.insert(0,tab)
        for exp in block.find('block'):
            if exp is block:continue
            if len(exp.children)>2:
                exp.children.insert(-1,tab)

    for node in full.find('assignment-operator'):
        node.appendChild(space)
        node.children.insert(0,space)
    for node in full.find('local-variable-declarator'):
        if len(node.children) == 3:
            node.children.insert(2,space)
            node.children.insert(1,space)
    for node in full.find('comment'):
        node.children.insert(0,lbreak)
        node.appendChild(lbreak)
    

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
        for node in full.find(list_type):
            node.children.insert(1,space)
    print full

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: parse.py [code file]'
        sys.exit(1)
    code, = sys.argv[1:]

    import codetalker.parser
    codetalker.parser.debug = False
    full = codetalker.parse(open(code).read(), grammar)
    print prettyfy(full)



# vim: et sw=4 sts=4
