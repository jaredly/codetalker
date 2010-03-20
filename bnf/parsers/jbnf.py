"""
jbnf.py -> parse my special falvor of bnf.

defines:
    Grammar(text)

examples
<name> : 'L' | <something> | <other><man>+

-- to do the string "'", use ''
-- suffixes:
* `+` one or more of the preceeding
* `*` zero or more of the preceeding
* `:` check for, but do not consume the preceeding
* `+?` non-greedy version
* `*?` non-greedy version
* `~` no big deal if it's not there

comments start with #

"""

import re
import string

class Grammar:
    '''A tool for parsing and storing a grammar.

    >>> g = Grammar('')
    >>> g = Grammar('<start>:\\'hi\\'')
    >>> g = Grammar("<a>:<b>|'4'\\n<b>:'yo'")
    '''
    def __init__(self, filename, tokens = string.printable, extends = None):
        self.filename = filename
        self.original = open(filename).read()
        self.extends = extends
        self.tokens = tokens
        self.parse()

    def parse(self):
        self.rules = {}
        self.firsts = {}
        if self.extends:
            self.rules = self.extends.rules.copy()
            #self.firsts = self.extends.firsts.copy()
        self.lines = {}
        for i,line in enumerate(self.original.split('\n')):
            if not line.startswith('#') and line.strip():
                try:
                    if not ':' in line:
                        raise Exception
                    name, sep, body = re.findall(r'\s*(<[^>]+>)\s*([+]?:)\s*(.*)\s*', line)[0]
                except:
                    raise Exception, 'invalid bnf in file %s, line %d: %s' % (self.filename, i, line)
                
                name = name.strip()
                body = body.strip()
                self.lines[name] = i,body
                if sep == '+:':
                    if self.extends:
                        self.rules[name] += self.rulesplit(name)
                    else:
                        raise Exception, 'no previous declaration for %s found in "%s", line %d.' % (name, self.filename, i)
                else:
                    self.rules[name] = self.rulesplit(name)
        for name in self.rules:
            self.loadfirst(name, 'base')

    def loadfirst(self, name, parent):
        if name in self.firsts:return self.firsts[name]
        elif name == "''":return ["'"]
        elif name.startswith("'"):
            return [name.strip("'")[0]]
        elif name == 'e':
            return list(self.tokens)
        elif name in self.tokens:
            return [name]
        elif name not in self.rules:
            print self.tokens
            raise Exception, 'invalid rule found in "%s", line %d: %s' % (self.filename, self.lines[parent][0], name)

        chars = []
        self.firsts[name] = chars
        for child in self.rules[name]:
            if not child:
                continue
            chars.append(flatten(self.loadfirst(child[0], name)))
        return chars

    def rulesplit(self, name):
        """just made much smaller w/ regex =)"""
        pieces = "('[^']*'|<[^>]+>|\||\+|\*|\?|\s|:|~|e)"
        lno, body = self.lines[name]
        parts = re.findall(pieces, body)
        if ''.join(parts) != body:
            raise BNFException,'Invalid BNF provided in "%s", line %d: %s' % (self.filename, lno, body)
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
                options[-1].append(part)
        return options

def flatten(lst):
    """flatten a nested list"""
    res = []
    for item in lst:
        if type(item) in (tuple,list):
            res += list(flatten(item))
        else:
            res.append(item)
    return res

if __name__=='__main__':
    import doctest
    doctest.testmod()

# vim: et sw=4 sts=4
