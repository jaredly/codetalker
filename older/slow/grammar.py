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

def parse_grammar(text):
    _lines = list((i,line) for i,line in enumerate(text.split('\n')) if not line.strip().startswith('#') and line.strip())
    lines = []
    for i,line in _lines:
        #if '#' in line:
        #    line = line.split('#')[0]
        if line.startswith(' '):
            lines[-1][1] += ' ' + line.strip()
        else:
            lines.append([i,line.strip()])
            if not ':' in line:
                raise BNFException,"invalid BNF on line %d"%i
    rules = {}
    for i,line in lines:
        k,v = line.split(':',1)
        try:
            rules[k.strip()] = parse_bnf_line(v)
        except Exception,e:
            raise Exception,"Error on line %d: %s"%(i,e)

    first = {}
    cache_first(rules, first)

    grammar = {'rules':rules,'first':first}
    return grammar

def collapse(lst):
    for i in range(len(lst)):
        if type(lst) == list and type(lst[i]) == type(lst[i][0]) \
            and type(lst[i]) in (tuple,list) and len(lst[i])==1:
            lst[i] = lst[i][0]
        if type(lst[i]) in (list,tuple):
            collapse(lst[i])

def parse_bnf_line(text):
    parts_rx = "('[^']*'|\w+|\||\+|\*|\?|\s|:|~|e|\[|\]|\(|\))"
    parts = re.findall(parts_rx, text)
    if ''.join(parts) != text:
        raise BNFException,'Invalid BNF provided: %s :: %s'%(text,''.join(parts))
    for i,p in enumerate(parts):
        if p == "'\\n'":parts[i] = "'\n'"
        elif p == "'\\t'":parts[i] = "'\t'"
    parts = list(p for p in parts if p.strip())
    bnf = parse_bnf(parts)[0]
    #print bnf
    return bnf

def parse_bnf(parts, i=0):
    """
    at the start:
        '.' means concat
        'U' means union
        '?' means maybe union
    """
    #pdb.set_trace()
    i = 0
    bnf = [['.']]
    while i<len(parts):
        if parts[i] in ')]':
            return bnf, i+1
        elif parts[i] == '|':
            bnf.append(['.'])
            i += 1
        elif parts[i] == '(':
            nf, di = parse_bnf(parts[i+1:])
            bnf[-1].append(['U']+nf)
            i += di + 1
        elif parts[i] == '[':
            nf, di = parse_bnf(parts[i+1:])
            bnf[-1].append(['?']+nf)
            i += di + 1
        elif parts[i] not in ' \t':
            bnf[-1].append(parts[i])
            i += 1
    for i,part in enumerate(bnf):
        if len(part)==1 and type(part[0]) in (tuple,list):
            bnf[i] = type(bnf[i])(part[0])
    return ['U'] + bnf,i

def cache_first(rules, first):
    for rule in rules:
        cache_one_first(rule, rules, first)

def cache_one_first(rule, rules, first):
    if first.has_key(rule):return
    first[rule] = options = []
    bnf = rules[rule]

    for option in bnf[1:]:
        options += get_first(option, rules, first)

def get_first(option, rules, first):
    if type(option) == str:
        if option[0] == "'":
            return [option[1:-1]]
        elif not rules.has_key(option):
            return [option]
        cache_one_first(option, rules, first)
        return first[option]
    if option[0] == '.':
        res = get_first(option[1], rules, first)
        option = option[1:]
        while len(option):
            if option[0] == ':':
                option = option[1:]
            elif len(option)>2 and option[1] == '*':
                res += get_first(option[2], rules, first)
                option = option[2:]
            elif type(option[0]) is list and option[0][0] == '?' and len(option)>1:
                if option[1] == ':':
                    option = option[1:]
                    if len(option)<=1:
                        break
                res += get_first(option[1], rules, first)
                option = option[1:]
            else:
                break
        return res
    res = []
    for sub in option[1:]:
        res += get_first(sub, rules, first)
    return res

if __name__=='__main__':
     print parse_grammar(open('python.real.bnf').read())['first']['stmt']

'''
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
    """parse the rules from a BNF string of *text*"""
    for line in text.split('\n'):
        if not line.strip():continue
        name,rule = line.split(':',1)
        rules[name.strip()] = split_rule(rule.strip())
    #first('<start>',given)
    for name in rules:
        first(name,rules)
'''
