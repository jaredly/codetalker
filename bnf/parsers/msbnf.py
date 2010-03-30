#!/usr/bin/env python
'''
Grammar looks like:

    rule : [ items ]
    items are one of:
        rule-name
        'string literal'
        (U+ABCD) // unicode literal -- not yet supported
        * // zero or more of the previous
        + // one or more of the previous
        ? // zero or one of the previous
        : // non-capturing match
        [rx range]
        [^rx notrange]

'''
import grammar
import re
import sys
import string

def output_grammar(gmr):
    txt = ''
    for rule,options in sorted(gmr.rules.iteritems()):
        txt += '%s:\n'
        for option in options:
            txt += '    '
            for child in option:
                if child[0] == '@':
                    txt += child[1:]+' '
                elif child[0] == '!':
                    txt += "'%s'" % escape(child[0][1:])

def splitsections(text):
    '''Sections look like:
        ["### header", [startline, decl...]]
    
    Decls look like:
        [type, startline, line...]
    
    type: one of
        comment, rule'''

    sections = [["### Global", [0]]]
    special = {}
    decl = None
    for i,line in enumerate(text.split('\n')):
        if not line.strip():continue
        if line.startswith('###'):
            if decl:
                if sections:
                    sections[-1][1].append(decl)
                decl = None
            sections.append([line, [i]])
        elif line.startswith('#'):
            if decl and decl[0] == 'comment':
                decl.append(line)
            else:
                if decl:
                    sections[-1][1].append(decl)
                decl = ['comment',i,line]
        elif line.startswith(' '):
            if decl and decl[0] == 'rule':
                decl.append(line)
            else:
                raise Exception,'orphaned rule-item at line %d: %s' % (i, line)
        elif line.startswith('@'):
            name, val = line[1:].split(':')
            special[name.strip()] = val.strip()
        else:
            if decl:
                sections[-1][1].append(decl)
            decl = ['rule',i,line]
    if decl:
        sections[-1][1].append(decl)
    return sections, special

class BNFError(Exception):
    pass

class Grammar(grammar.Grammar):
    def loadrules(self):
        sections, special = splitsections(self.original)
        if special.has_key('start'):
            self.start = special['start']
        for section in sections:
            for decl in section[1][1:]:
                if decl[0] == 'comment':
                    continue
                name,opts = decl[2].split(':')
                name = name.strip()
                if self.lines.has_key(name):
                    print 'prev line: ',decl[1:]
                self.lines[name] = decl[1:]
                options = tuple(x.strip() for x in opts.split(',') if x.strip())
                try:
                    self.loadrule(name, options, decl[3:])
                except BNFError, e:
                    print>>sys.stderr, 'Error in "%s"' % self.filename
                    print>>sys.stderr, '\tError parsing BNF for rule at line %d: %s' % (
                            decl[1]+1, e)
                    sys.exit()

    def loadrule(self, name, options, body):
        valid_opts = 'one of', 'add', 'sub', 'replace'
        for opt in options:
            if opt not in valid_opts:
                raise BNFError,'invalid option: %s' % opt

        mods = sum(['add' in options,'sub' in options,'replace' in options])
        if mods > 1:
            raise BNFError,'invalid options. only one of "add","sub","replace" is allowed'
        if mods == 0 and self.rules.has_key(name):
            raise BNFError,'duplicate declaration of %s. use add, sub, or replace' % name

        choices = []
        if 'add' in options or 'sub' in options:
            if not self.rules.has_key(name):
                raise BNFError,'can\'t add: not previous definition of %s' % name
            choices = self.rules[name]
        elif 'replace' in options:
            if name+'-old' in self.rules:
                raise BNFError,'rule has already been replaced (%s-old exists): %s' % (name, name)
            self.rules[name+'-old'] = self.rules[name]
            del self.rules[name]

        if 'one of' in options:
            if len(body) == 1:
                items = body[0].split(' ')
            else:
                items = body
            items = list(("!%s" % x.strip(),) for x in items if x.strip())
            if 'sub' in options:
                for it in items:
                    if it not in choices:
                        raise BNFError,'item not there to remove: %s' % it
                    choices.remove(it)
                self.rules[name] = choices
            else:
                self.rules[name] = choices + items
        else:
            for line in body:
                parts = rulesplit(line)
                if 'sub' in options:
                    for it in parts:
                        if it not in choices:
                            raise BNFError,'item not there to remove: %s' % it
                        choices.remove(it)
                else:
                    choices += parts
            self.rules[name] = choices
        for choice in self.rules[name]:
            if choice[0] == '@'+name:
                print 'recursive rule; consider changing.', name, self.lines[name][0]+1
        if self.debug:
            pass#fail

def rulesplit(line):
    '''split a rule end
    allowed:
        'string lit'
        rule-name
        *
        +
        :
        ?
        [char-range]

    >>> rulesplit
    '''
    rx = r"([\w\-]+|\s|'(?:\\'|[^']|)*'|\*|\+|:|\?|\[(?:[^\]]|\\\]])+\])"
    parts = re.findall(rx, line)
    if ''.join(parts) != line:
        raise BNFError, 'invalid bnf:\nparsed  : %s\noriginal: %s' % (''.join(parts), line)

    parts = list(p for p in parts if p.strip())

    if len(parts)==1 and parts[0][0] == '[':
        try:
            return expand(parts[0])
        except BNFError, e:
            raise BNFError,'invalid character range: %s; %s' % (parts[0], e)

    ret = []
    for part in parts:
        if part.startswith('['):
            raise BNFError,'a character range must be the only item'
        if not part.strip():continue
        if part[0] == "'":
            part = part[1:-1]
            ret.append('!'+part.decode('string_escape'))
        elif part in '*+:?':
            ret.append(part)
        else:
            ret.append('@'+part)
    return [tuple(ret)]

def expand(crange):
    '''expand a regex-like character crange. supported escapes:
    \w a-zA-Z_0-9
    \s whitespace
    \. all printable'''
    if crange[0]!='[' or crange[-1]!=']':
        raise BNFError
    items = []
    i = 1
    exclude = False
    if crange[1] == '^':
        i += 1
        exclude = True
    while i<len(crange)-1:
        char = crange[i]
        if char == '\\':
            next = crange[i+1]
            if next == 'w':
                items += list(string.ascii_letters + string.digits + '_')
            elif next == '.':
                items += list(string.printable)
            elif next == 's':
                items += list(' \t\n\r\x0b\x0c')
            elif next in '-][':
                items.append(next)
            elif next == 'n':
                items.append('\n')
            elif next == 't':
                items.append('\t')
            else:
                raise BNFError, 'invalid escape "%s"; the only valid escapes are \\n \\t \\w \\. \\s \\- \\[ \\]' % next
            i += 2
            continue
        elif char == '-':
            if i < 2 or i >= len(crange)-2: raise BNFError
            cs = ord(items[-1])
            ce = ord(crange[i+1])
            if ce<cs:raise BNFError
            for a in range(cs,ce):
                items.append(chr(a+1))
            i += 2
            continue
        items.append(char)
        i += 1
    if exclude:
        return list(('!'+a,) for a in string.printable if a not in items)
    return list(('!'+a,) for a in items)

# vim: et sw=4 sts=4
