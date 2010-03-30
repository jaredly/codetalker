'''check.py -- a sample python file to test python parsing'''
import parse_lib
# a comment
print str(parse_lib.parse(open('parse.py').read())[1]) # another comment
"""hello
my fred"""
if 1:
    print "yes"

for a in range(20):
    if a % 2 == 0:
        print a
    else:
        for i in range(1):
            print i,
        print

def x(self):
    if name==main:
        print yeah

class Some:
    def other(self):
        print 34
    f = property(4,5,6)

