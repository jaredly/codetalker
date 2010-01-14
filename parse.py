### tokenizer

from node import Node
import grammar

def isliteral(rule):
    return rule.startswith("'")

def matchliteral(text, i, rule):
    if rule.startswith("'"):
        char = rule.strip("'") or "'"
        if text[i:i+len(char)] != char:
            return False,0
        i += len(char)
        return char, i
    elif isinstance(text[i],Node) and text[i].name == rule:
        return text[i], i+1
    return False,0

def parserule(text, i, rule):
    if i>=len(text):
        return False, 0
    res, di = matchliteral(text, i, rule)
    if res:
        return res, di
    if not rule in grammar.rules:
        return False,0

    '''if rule.startswith("'"):
        # rule is literal
        char = rule.strip("'") or "'"
        if text[i:i+len(char)] != char:
            return False,0
        i += len(char)
        return char, i'''
    for n,one in enumerate(grammar.rules[rule]):
        if text[i] in grammar.firsts[rule][n]:
            res, di = parse_children(text, i, rule, one)
            if not res:
                continue
            return res, di
    return False, 0

def parse_children(text, i, rule, children):
    node = Node(rule)
    a = 0
    while a < len(children):
        if a < len(children)-1:
            if children[a+1] == '+':
                res, di = parserule(text, i, children[a])
                if not res:
                    return False, 0
                node.children.append(res)
                i = di
            if children[a+1] in '+*':
                while 1:

                    if a < len(children)-2 and children[a+2] == '?':
                        # non-greedy
                        res, di = parse_children(text, i, rule, children[a+3:])
                        if res:
                            node.children += res.children
                            return node, di

                    res, di = parserule(text, i, children[a])
                    if not res:break
                    node.children.append(res)
                    i = di
                a += 2
                continue
        res, di = parserule(text, i, children[a])
        if not res:
            return False, 0
        node.children.append(res)
        i = di
        a += 1
    #print 'yes!!',node,rule
    return node, i

def totokens(node):
    assert node.name == '<start>'
    for tokenw in node.children:
        yield tokenw.children[0].toliteral()

def parse(text):
    grammar.make_rules(open('tokenize.bnf').read())
    print 'done genning'
    #for rule in grammar.firsts:
    #    print rule,grammar.firsts[rule]
    #text = [Node(c,True) for c in text]
    nodes = parserule(text, 0, '<start>')
    return nodes

if __name__=='__main__':
    print [parse(open('check.py').read())[0]]
