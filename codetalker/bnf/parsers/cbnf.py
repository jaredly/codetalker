#!/usr/bin/env python
"""A grammar parser for the bnf style the the c_grammar.bnf file is in"""

import re
import string
import grammar

class Grammar(grammar.Grammar):
    '''A tool for parsing and storing a grammar.
    '''
    def loadrules(self):
        buff = ''
        for i, line in enumerate(self.original.split('\n')):
            if line.startswith('%'):continue
            if line.strip() == ';':
                name, body = re.findall(r'\s*([\w_]+)\s*:\s*(.*)\s*$', buff)[0]
                name = '<%s>' % name
                self.lines[name] = i,body
                self.rules[name] = self.rulesplit(name)
                buff = ''
            else:
                buff += line.strip()

    def rulesplit(self, name):
        pieces = "('[^']*'|[\w_]+|\||\s)"
        lno, body = self.lines[name]
        parts = re.findall(pieces, body)
        if ''.join(parts) != body:
            raise grammar.BNFException, "Invalid BNF provided for rule %s, line %s: %s" % (name, lno, body)
        options = [[]]
        for part in parts:
            if part == '|':
                options.append([])
            elif part == "'\\t'":
                options[-1].append("'\t'")
            elif part == "'\\n'":
                options[-1].append("'\n'")
            elif part in ' \t':
                continue
            else:
                if not part.startswith("'"):
                    part = '<%s>' % part
                options[-1].append(part)
        return options




# vim: et sw=4 sts=4
