"""
grammar.py -> parses BNF grammars

SWEET!!

examples

<name> : 'L' | <something> | <other><man>+

-- to do the string "'", use ''
-- suffixes:
* `+` one or more of the preceeding
* `*` zero or more of the preceeding
* `:` check for, but do not consume the preceeding
* `+?` non-greedy version
* `*?` non-greedy version
* `~` no big deal if it's not there

............. um changing to fit the Python BNF






"""

import re
import string

class BNFException(Exception):
    pass

def split_rule(text):
    """just made much smaller w/ regex =)"""
    pieces = "('[^']*'|<[^>]+>|\||\+|\*|\?|\s|:|~|e)"
    parts = re.findall(pieces, text)
    if ''.join(parts) != text:
        raise BNFException,'Invalid BNF provided'
    options = [[]]
    for part in parts:
        if part == '|':
            options.append([])
        elif part == "'\\t'":
            options[-1].append("'\t'")
        elif part == "'\\n'":
            options[-1].append("'\n'")
        elif part in ' \t':
            continue
        else:
            options[-1].append(part)
    return options

def flatten(lst):
    """flatten a nested list"""
    res = []
    for item in lst:
        if type(item) in (tuple,list):
            res += list(flatten(item))
        else:
            res.append(item)
    return res

firsts = {}

def first(rule,rules):
    """cache the first character/token of a given *rule*"""
    if rule in firsts:return firsts[rule]
    elif rule == "''":
        return ["'"]
    elif rule.startswith("'"):
        return [rule.strip("'")[0]]
    elif rule == 'e':
        return list(string.printable)

    ret = []
    firsts[rule] = ret
    for one in rules[rule]:
        ret.append(flatten(first(one[0],rules)))
    return ret

rules = {}
def make_rules(text):
    '''parse the rules from a BNF string of *text*'''
    for line in text.split('\n'):
        if not line.strip():continue
        name,rule = line.split(':',1)
        rules[name.strip()] = split_rule(rule.strip())
    #first('<start>',given)
    for name in rules:
        first(name,rules)
