
import grammar

class Node:
    def __init__(self, rule, index):
        self.name = rule
        self.index = index
        self.children = []
    def __str__(self):
        return ''.join(str(x) for x in self.children)
    def __repr__(self):
        return ('<%s>\n%s\n</%s>'%(self.name,'\n'.join(x.__repr__() for x in self.children),self.name)).replace('\n','\n  ')

def parse_rule(rule, text, i, bnf, stack):
    stack += (rule,)
    if i>=len(text):
        if i>bnf['error'][0]:
            bnf['error'] = i,stack + ('EOF',)
        return False, 0
    node, ni = match_literal(rule, text, i)
    if node:
        return node, ni
    elif not rule in bnf['rules']:
        if i > bnf['error'][0]:
            bnf['error'] = i, stack + (text[i],)
        return False, 0

    return parse_children(bnf['rules'][rule], rule, text, i, bnf, stack)

def parse_children(children, parent, text, i, bnf, stack):
    assert children[0] in 'U?'
    for sequence in children[1:]:
        if sequence[0] == 'U': #union
            n,ni = parse_children(sequence, parent, text, i, bnf, stack)
            if n:
                return n, ni
        elif sequence[0] == '?':
            # ... doesn't make sense
            raise Exception,"why have an optional inside of a switch?? bad BNF for rule %s"%parent
        elif sequence[0] == '.': # sequence!
            n,ni = parse_sequence(sequence[1:], parent, text, i, bnf, stack)
            if n:
                return n, ni
        else:
            raise Exception,"invalid BNF"
    if i>bnf['error'][0]:
        bnf['error'] = i, stack + ('IDK',)
    return False,0

def parse_sequence(sequence, parent, text, i, bnf, stack):
    node = Node(parent, i)
    a = 0
    while a<len(sequence):
        if a+1<len(sequence) and type(sequence[a+1])==str:
            if sequence[a+1] in '+*:' and type(sequence[a]) == list and sequence[a][0] == '?':
                raise Exception,'it makes no sence to *+: on an optional'
            if sequence[a+1] == '+':
                n,ni = parse_item(sequence[a], parent, text, i, bnf, stack)
                if not n:return False, 0
                node.children.append(n)
                i = ni
            if sequence[a+1] in '+*':
                while True:
                    if a+2<len(sequence) and sequence[a+2] == '?':
                        n,ni = parse_sequence(sequence[a+3:], parent, text, i, bnf, stack)
                        if n:
                            node.children += n.children
                            return node, ni
                    n,ni = parse_item(sequence[a], parent, text, i, bnf, stack)
                    if not n:break
                    node.children.append(n)
                    i = ni
                a += 2
                continue
            elif sequence[a+1] == ':':
                n,ni = parse_item(sequence[a], parent, text, i, bnf, stack)
                if not n:
                    return False, 0
                a += 2
                continue

        n,ni = parse_item(sequence[a], parent, text, i, bnf, stack)
        if not n:
            if not (type(sequence[a])==list and sequence[a][0]=='?'):
                return False, 0
        else:
            node.children.append(n)
            i = ni
        a += 1
    return node, i


def parse_item(item, parent, text, i, bnf, stack):
    if type(item) == list:
        return parse_children(item, parent, text, i, bnf, stack)
    elif type(item) == str:
        return parse_rule(item, text, i, bnf, stack)
    else:
        raise Exception,'Unknown item: %s'%item

def match_literal(rule, text, i):
    if rule[0] == "'":
        chars = rule.strip("'") or "'"
        if isinstance(text[i],Node):
            txt = str(text[i])
            while len(txt)<len(chars) and i<len(text)-1:
                i+=1
                txt+=str(text[i])
            if txt == chars:
                return chars, i+1
        elif text[i:i+len(chars)] == chars:
            i += len(chars)
            return chars, i
    elif isinstance(text[i],Node) and text[i].name == rule:
        return text[i], i+1
    return False, 0

def parse(text, bnf):
    bnf = grammar.parse_grammar(open(bnf).read())
    bnf['error'] = 0, None
    node = parse_rule('start',text,0,bnf,())
    if not node[1]:
        print 'error',bnf['error']
    return node

if __name__ == '__main__':
    def t():
        res = parse(open('parse.py').read(), 'tokenize.bnf')
    import cProfile
    cProfile.run('t()','slowparser.prof')
