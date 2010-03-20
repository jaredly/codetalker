### tokenizer

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def __repr__(self):
        txt = self.name+'\n'
        for child in self.children:
            txt += str(child).replace('\n','\n  ')
        txt += self.name.replace('<','</')+'\n'
        return txt

    def __str__(self):
        res = ''
        for c in self.children:
            res += str(c)
        return res

stack = []
predicates = {}
bookends = {}
items = {}

class BNFException(Exception):
    pass

id = 0
def next_id():
    global id
    id+=1
    return id

def splitchildren(text):
    """WORKS"""
    ors = [[]]
    i = 0
    ins = False
    while i<len(text):
        current = ''
        if text[i] == '<':
            current+=text[i]
            i+=1
            if i>=len(text):raise BNFException,'invalif bnf'
            while text[i]!='>':
                current+=text[i]
                i+=1
                if i>=len(text):raise BNFException,'invalif bnf'
            current+=text[i]
            i+=1
        elif text[i] == "'":
            current+=text[i]
            i+=1
            if i>=len(text):raise BNFException,'invalif bnf'
            while text[i]!="'":
                current+=text[i]
                i+=1
                if i>=len(text):raise BNFException,'invalif bnf'
            current+=text[i]
            if current == "'\\t'":
                current = "'\t'"
            elif current == "'\\n'":
                current = "'\n'"
            i+=1
        elif text[i] in '*+':
            current+=text[i]
            i+=1
        elif text[i] == '|':
            ors.append([])
            i+=1
            continue
        else:
            raise Exception,'fail: %s:'%text[i]
        ors[-1].append(current)
    return ors

def parserule(text, i, rule):
    if rule.startswith("'"):
        char = rule.strip("'") or "'"
        if text[i] != char:
            return False,0
        i += 1
        return char, i
    if i>=len(text):
        return False, 0
    for n,one in enumerate(rules[rule]):
        if text[i] in firsts[rule][n]:
            res, di = parsechildren(text, i, rule, one)
            if not res:
                continue
            return res, di
    return False, 0

def parsechildren(text, i, rule, children):
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

def flatten(x):
    """WORKS"""
    res = []
    for r in x:
        if type(r) in (tuple,list):
            res += list(flatten(r))
        else:
            res.append(r)
    return res

firsts = {}
def first(rule,rules):
    """WORKS"""
    if rule in firsts:return firsts[rule]
    elif rule.startswith("'"):
        return rule.strip("'") or "'"
    ret = []
    for one in rules[rule]:
        ret.append(flatten(first(one[0],rules)))
    firsts[rule] = ret
    return ret

rules = {}
def genrules(text):
    given = {}
    for x in text.split('\n'):
        if not x.strip():continue
        k,v = x.split(':',1)
        given[k.strip()] = splitchildren(v.strip())
#    given = dict(x.split(':',1) for x in text.split('\n') if x)
#    print given
#    given = dict((k.strip(), splitchildren(v.strip())) for k,v in given.items())
    ## cache all the 'first's
    first('<start>',given)
    for k in given:
        first(k,given)
    global rules
    rules = given



def parse(text):
    genrules(open('tokenize.bnf').read())
    print 'done genning'
    #for rule in firsts:
    #    print rule,firsts[rule]
    nodes = parserule(text, 0, '<start>')
    return nodes

