#!/usr/bin/env python

from util import *

tokenize = just_tokenize(STRING, ID, NUMBER, WHITE, NEWLINE)

test_one = make_test(tokenize, '"a string" an_id 12 14.3\n"and\\" 4" .5',
                    expected = [STRING, WHITE, ID, WHITE, NUMBER, WHITE, NUMBER, NEWLINE, STRING, WHITE, NUMBER])

# vim: et sw=4 sts=4
