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

import grammar

class Grammar(grammar.Grammar):
    '''A tool for parsing and storing a grammar.

    >>> g = Grammar('')
    >>> g = Grammar('<start>:\\'hi\\'')
    >>> g = Grammar("<a>:<b>|'4'\\n<b>:'yo'")
    '''
    def loadrules(self):
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

    def rulesplit(self, name):
        """just made much smaller w/ regex =)"""
        pieces = "('[^']*'|<[^>]+>|\||\+|\*|\?|\s|:|~|e)"
        lno, body = self.lines[name]
        parts = re.findall(pieces, body)
        if ''.join(parts) != body:
            print ''.join(parts),body
            raise grammar.BNFException,'Invalid BNF provided in "%s", line %d: %s' % (self.filename, lno, body)
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

if __name__=='__main__':
    import doctest
    doctest.testmod()

# vim: et sw=4 sts=4
