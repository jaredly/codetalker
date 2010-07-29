#!/usr/bin/env python

from codetalker import testing
import codetalker.contrib.configparser as configparser

parse_rule = testing.parse_rule(__name__, configparser.grammar)

parse_rule(configparser.name, (
    'hi',
    'eggs and spam',
    'mult1ple 23',
    'spam-eggs',
    ), (
    '',
    '.',
    'sandom ch@rs',
    ))

parse_rule(configparser.value, (
    'basically anything',
    'with\n  and indent',
    'and\n  some more\n  lines',
    ), (
    'no\nindent',
    'multiple\n  indent\n    levels',
    'invalid\n    dedents\n  are bad',
    ))

parse_rule(configparser.define, (
    'a=b',
    'party=23 54',
    'but:we already\n  know this',
    'white :space',
    ), (
    '{}',
    ))

parse_rule(configparser.head, (
    '[section name]',
    '[no kidding ]',
    ), (
    '[no ending',
    ))

bigold_thing = '''
[eggs]
spam=1
eggs and rice= never again

[beef-steak 23]
lets=%(spam)s pig
spam: spamspamspam
knights=%(eggs)s
eggs: recursive %(knights)s
'''

def test_bigold():
    c = configparser.parse(bigold_thing)
    assert set(c.sections.keys()) == set(('eggs', 'beef-steak 23'))
    assert c.get_item('eggs', 'spam') == '1'
    assert c.get_item('beef-steak 23', 'lets') == 'spamspamspam pig'
    try:
        one = c.get_item('beef-steak 23', 'knights')
    except configparser.RecursionError:
        pass
    else:
        raise Exception('this was supposed to be recursive: %s' % one)


# vim: et sw=4 sts=4
