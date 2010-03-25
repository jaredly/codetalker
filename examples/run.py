#!/usr/bin/env python
from code import InteractiveConsole as IC

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: run.py other.py'
        sys.exit(0)
    execfile(sys.argv[1])

    ic = IC(globals())
    ic.interact()

# vim: et sw=4 sts=4
