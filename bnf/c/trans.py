#!/usr/bin/env python


if __name__ == '__main__':
    import sys, os
    if len(sys.argv)<3:
        print 'usage: tans.py cin.bnf out.tokens.bnf'
        sys.exit(1)
    inf, outf = sys.argv[1:]
    if os.path.exists(outf):
        print 'file exists: %s' %outf
        sys.exit(1)
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


# vim: et sw=4 sts=4
