#!/usr/bin/env python
from codetalker.bnf.parsers import msbnf

def tokenize(inf, outf):
    names = []
    txt = open(inf)
    for line in txt:
        if line.startswith('%token '):
            names += line.split()[1:]
    out = open(outf,'w')
    for name in names:
        print>>out, '<%s> : \'%s\'' % (name, name.lower())
    print>>out, '<token> : <%s>' % '>|<'.join(names)
    out.close()

def compress(cin, cout):
    text = open(cin).read()
    sections = msbnf.splitsections(text)
    print [s[0] for s in sections]
    autosection = ['### C.4 auto-created optimizations',[-1]]
    mult = {}
    rules = []
    ruled = {}
    errors = 0
    dups = 0
    for section in sections:
        for decl in section[1][1:]:
            if decl[0]=='comment':continue
            decl[2] = decl[2].strip()
            fs = tuple(a.strip() for a in decl[3:])
            if decl[2] in rules:
                if ruled[decl[2]] != fs:
                    print '!! same name, different def. please fix: at %d' % decl[1]
                    errors += 1
                print 'dub rule found at %d: %s' % (decl[1],decl[2])
                dups += 1
            rules.append(decl[2])
            ruled[decl[2]] = fs
            if len(fs)==1:continue
            if decl[2] not in mult.get(fs,[]):
                mult[fs] = mult.get(fs, []) + [decl[2]]
    replaced = {}
    if errors > 0:
        print 'Please fix the errors found.'
        sys.exit(1)
    i = 0
    for k,v in mult.items():
        if len(v) > 1:
            i += 1
            nname = 'auto-rule-%d' % i
            while nname in rules:
                i += 1
                nname = 'auto-rule-%d' % i
            rules.append(nname)
            for rname in v:
                replaced[rname] = nname
            decl = ('rule', -1, nname+':') + tuple('    '+l for l in k)
            autosection[1].append(decl)
            cdecl = ('comment', -1, '# used by ' + ', '.join(v))
            autosection[1].append(cdecl)
            print 'added %s for'%nname, v

    sections.append(autosection)
    outf = open(cout,'w')
    for section in sections:
        print>>outf, section[0]
        print>>outf
        for decl in section[1][1:]:
            if decl[0]=='comment':
                print>>outf, '\n'.join(decl[2:])
            else:
                print>>outf, decl[2]
                if decl[2] in replaced:
                    print>>outf, '    '+replaced[decl[2]]
                else:
                    print>>outf, '    '+'\n    '.join(x.strip() for x in decl[3:])
            print>>outf
    outf.close()

    print 'yeah!'







if __name__ == '__main__':
    import sys, os
    if len(sys.argv)<3:
        print 'usage: tans.py cin.bnf out.tokens.bnf'
        sys.exit(1)
    inf, outf = sys.argv[1:]
    if not os.path.exists(inf):
        print 'infile doesn\'t exist: %s' % inf
        sys.exit(1)
    if os.path.exists(outf):
        print 'out file exists: %s' %outf
        sys.exit(1)
    compress(inf, outf)


# vim: et sw=4 sts=4
