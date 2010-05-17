#!/usr/bin/env python
from codetalker.bnf.parsers import jbnf,cbnf,msbnf,antlrbnf

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print 'usage: convert_bnf.py file from to'
    grammars = {'msbnf':msbnf, 'cbnf':cbnf, 'antlrbnf':antlrbnf}
    frm = grammars[sys.argv[2]]
    tog = grammars[sys.argv[3]]

    grammar = frm.Grammar(sys.argv[1])
    text = tog.output_grammar(grammar)
    print text

# vim: et sw=4 sts=4
