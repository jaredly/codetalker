#!/usr/bin/env python
from codetalker import parser
from codetalker.bnf import c

def main():
    text = open(os.path.join(os.path.dirname(__file__),'hanoi.c')).read()
    small = '1 2 manhatten; ()'
    nodes, i, const = parser.parse(small, c.tokens)
    if len(nodes)!=1:
        print 'bad node length',nodes
        sys.exit(1)
    if i!=len(small):
        print 'not everything was parsed'
        print str(nodes[0])
        print const['error'],const['pos']
        sys.exit(1)
    if str(nodes[0]) != small:
        print 'parsed badly:\ninput:\t"%s"\nparsed:\t"%s"' % (small, nodes[o])
        sys.exit(1)

    nodes, i, const = parser.parse(text, c.tokens)
    if len(nodes) != 1:
        print 'bad node length',nodes
        sys.exit(1)
    if i != len(text):
        print 'not everything was parsed'
        print str(nodes[0])
        print const['error'],const['pos']
        sys.exit(1)
    print 'all test were successful'


if __name__=='__main__':
    import sys,os
    main()

# vim: et sw=4 sts=4
