#!/usr/bin/env python

from util import just_tokenize, make_tests, make_fails, TSTRING, STRING, SSTRING, ID, WHITE, NUMBER, INT, HEX, CCOMMENT, CMCOMMENT, PYCOMMENT, NEWLINE, ANY

def make_single(tok, *tests):
    fn = just_tokenize(tok, WHITE)
    return make_tests(globals(), tok.__name__, fn, tests)

def fail_single(tok, *tests):
    fn = just_tokenize(tok)
    return make_fails(globals(), tok.__name__, fn, tests)

# string

make_single(STRING,
        ('', 0),
        ('"one"', 1),
        ('"lo' + 'o'*1000 + 'ng"', 1),
        ('"many"'*20, 20))

fail_single(STRING,
        '"',
        '"hello',
        '"one""and',
        '"lo' + 'o'*1000)

# sstring

make_single(SSTRING,
        ('', 0),
        ("'one'", 1),
        ('\'lo' + 'o'*1000 + 'ng\'', 1),
        ('\'many\''*20, 20))

fail_single(SSTRING,
        "'",
        "'one",
        "'lo"+'o'*1000,
        "'many'"*20+"'")

# tstring

make_single(TSTRING,
        ('', 0),
        ('""""""', 1),
        ('"""one line"""', 1),
        ('"""two\nlines"""', 1),
        ('"""lots'+'\n'*100+'of lines"""', 1),
        ('"""many"""'*20, 20),
        ("''''''", 1),
        ("'''one line'''", 1),
        ("'''two\nlines'''", 1),
        ("'''lots"+'\n'*100+"of lines'''", 1),
        ("'''many'''"*20, 20))

fail_single(TSTRING,
        '"',
        '"""""',
        '"""',
        '"""start',
        '"""not full"',
        '"""partial""')

# ID

make_single(ID,
        ('', 0),
        ('o', 1),
        ('one', 1),
        ('lo'+'o'*1000+'ng', 1),
        ('numb3rs', 1),
        ('ev3ry_thing', 1))

fail_single(ID,
        '3',
        '3tostart',
        '$other',
        'in-the-middle')

# NUMBER

make_single(NUMBER,
        ('', 0),
        ('24', 1),
        ('1 2', 3),
        ('1.2', 1),
        ('.3', 1),
        ('1.23'+'4'*100, 1),
        ('123'+'4'*100 + '1.20', 1),
        ('1.23e10', 1),
        ('1.23E10', 1),
        ('1.23e+10', 1),
        ('1.23E+10', 1),
        ('.1e-10', 1),
        ('.1E-10', 1))

fail_single(NUMBER,
        '.1e',
        '.2e.10')

# INT

make_single(INT,
        ('123', 1),
        ('', 0),
        ('100'+'0'*1000+'6543', 1))

# HEX

make_single(HEX,
        ('0xdead', 1),
        ('0x1234', 1),
        ('0xDEad0142', 1),
        ('0XDe23', 1))

fail_single(HEX,
        '1x23',
        '0xread')

# CCOMMENT

make_single(CCOMMENT,
        ('', 0),
        ('// hello!', 1),
        ('// one\n', 1),
        ('// one\n// two', 2))

# CMCOMMENT

make_single(CMCOMMENT,
        ('', 0),
        ('/**/', 1),
        ('/** //*/', 1),
        ('/*/*/', 1),
        ('/* // *//**/', 2),
        ('/** multi\n// line**/', 1))

fail_single(CMCOMMENT,
        '/*/',
        '/',
        '/*',
        '/** stuff\n')

# PYCOMMENT

make_single(PYCOMMENT,
        ('', 0),
        ('# stuff', 1),
        ('# nline\n', 1),
        ('# more\n# stuff', 2))

# ANY

make_single(ANY,
        ('', 0),
        ('ask@#$\n', 7))

# vim: et sw=4 sts=4
