#!/usr/bin/env python
from urllib import urlopen as upen
import re

def get_code(num):
    print 'get page...'
    url = 'http://www.c.happycodings.com/code_snippets/code%d.html' % num
    text = upen(url).read()
    print 'got'
    code = re.findall('<TEXTAREA[^>]*>(.+?)</TEXTAREA>', text, re.S)
    return code[0]

for i in range(50):
    code = get_code(i+1)
    open('c/more/code%d.c' % (i+1), 'w').write(code)

# vim: et sw=4 sts=4
