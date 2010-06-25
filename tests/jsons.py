#!/usr/bin/env python
import os
local = lambda *a: os.path.join(os.path.dirname(__file__), *a)
text = open(local('grammar.json')).read()
from codetalker.contrib.json import JSON
good = [[[['*', ['|', [1], [-8]]]]], [[2], [12], [13]], [[-3, '=', 3, ['|', [-8], [-12]]]], [[['+', 4]]], [[5, ['*', ['|', ['-'], ['+']], 5]]], [[6, ['*', ['|', ['*'], ['/']], 6]]], [[7, ['*', ['|', [9], [10], [11]]]]], [[8], [-2], [-3], [-4], [-5]], [['(', 4, ')']], [['.', -3]], [['[', 4, ']']], [['(', ['?', 4, ['*', ',', 4], ['?', ',']], ')']], [['@', -3, '(', ['?', 4, ['*', ',', 4], ['?', ',']], ')', ['|', [-8], [-12]]]], [[-1, ['+', -8], -10, ['+', ['|', [1], [14], [-8]]], ['|', [-11], [-12]]]], [[-3, ':', 3, ['|', [-8], [-12]]]]]
import time
def timeit(a, *b, **c):
    t = time.time()
    r = a(*b, **c)
    print '%s took %s' % (a, time.time() - t)
    return r

if not good == timeit(JSON.from_string, text):
    print 'failurez'



# vim: et sw=4 sts=4
