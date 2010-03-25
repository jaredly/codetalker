#!/usr/bin/env python

import codetalker
from codetalker.bnf import c

if __name__=='__main__':
    text = open('test/hanoi.c').read()
    r = codetalker.parse(text, c)
    [w.remove() for w in r.gETN('comment')]
    for w in r.gETN('whites'):
        if '\n' not in str(w):
            w.remove()
        else:
            w.children = ['\n']
    words = r.gETN('keyword,identifier')
    for word in words:
        next = word.nextNode()
        if str(next)[0].isalnum():
            codetalker.Node('whites',-1,False,[' ']).appendAfter(word)
    print r



# vim: et sw=4 sts=4
