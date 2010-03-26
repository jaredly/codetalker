#!/usr/bin/env python

import grammar

regex = '''
    (?<rule>[\w_]+)|
    (?<literal>'([^']|\\')*')|
    (?<notchars>~\([^\)]+\))|
    (?<repeat>\*\+\?)
    '''

def linehandle(line, rule, nsubs=0):
    items = [[]]
    subs = {}
    inside = False
    i = 0
    while i<len(line):
        char = line[i]
        if char in ' \t':
            i += 1
        elif char in '~*?':
            items[-1].append(char)
            i += 1
        elif char == '.':
            if line[i+1]=='.':
                items[-1].append('..')
                i += 2
            else:
                items[-1].append(char)
                i += 1
        elif char == "'":
            literal = '!'
            i += 1
            while line[i] != "'":
                if line[i] == '\\':
                    literal += line[i:i+2]
                    i += 2
                else:
                    literal += line[i]
                    i += 1
            items[-1].append(literal)
            i += 1
        elif char == '(':
            depth = 1
            start = i
            i += 1
            instring = False
            while depth > 0:
                if instring:
                    if line[i] == "'":
                        instring = False
                    elif line[i] == "\\":
                        i += 1
                elif line[i] == "'":
                    instring = True
                elif line[i] == '(':
                    depth += 1
                elif line[i] == ')':
                    depth -= 1
                i += 1
            sitems, ssubs, nsubs = linehandle(line[start+1:i-1], rule, nsubs)
            subs += ssubs
            subs[rule + '-%d' % nsubs] = sitems
            items[-1].append(rule + '-%d' % nsubs)
            nsubs += 1

        elif char == '|':
            items.append([])
            i += 1
        elif char in string.ascii_letters:
            rulename = '@'
            while line[i] in string.ascii_litters+string.digits+'-':
                rulename += line[i]
                i += 1
            items[-1].append(rulename)
        else:
            print 'weird char found: %s; %d; %s' % (line[i],i,line)
            fail

def split(text):
    rules = {}
    order = []
    name = None
    inrule = False
    for line in text.split('\n'):
        if line.strip().startswith('//') or not line.strip():
            continue
        if inrule == 2 and line.strip() == ';':
            inrule = 0
        elif not inrule:
            inrule = 1
            name = line.split(' ')[0]
        elif inrule == 1 and line.strip().startswith(':'):
            inrule = 2
            rules[-1].append(line.strip()[1:].strip())
        elif inrule == 2 and line.strip().startswith('|'):
            rules[-1].append(line.strip()[1:].strip())
    return rules

class Grammar(grammar.Grammar):
    def loadrules(self):
        sections = split(self.original)
        print sections[0]
        print sections[-1]
        print len(sections)

# vim: et sw=4 sts=4
