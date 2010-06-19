#!/usr/bin/env python

from something import plus, star, expand, all_chars, token

'''something special for tokens?'''

@token
def NUMBER(rule):
    rule | (plus(expand('0-9')), ['.', star(expand('0-9'))])
    rule | ('.', plus(expand('0-9')))

@token
def NAME(rule):
    rule | (expand('a-zA-Z_'), star(expand(r'\w_')))

@token
def STRING(rule):
    rule | s_trip_string
    rule | ("'", star(_or(('\\', all_chars), expand("^'\n"))), "'")
    rule | ('"', star(_or(('\\', all_chars), expand('^"\n'))), '"')

def s_trip_string(rule):
    rule | ("'''", star(s_trip_contents), "'''")

def s_trip_contents(rule):
    rule | ('\\', all_chars)
    rule | expand("^'")
    rule | ("'", expand("^'"))
    rule | ("''", expand("^'"))

def d_trip_string(rule):
    rule | ('"""', star(d_trip_contents), '"""')

def d_trip_contents(rule):
    rule | ('\\', all_chars)
    rule | expand('^"')
    rule | ('"', expand('^"'))
    rule | ('""', expand('^"'))

# vim: et sw=4 sts=4
