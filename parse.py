### tokenizer

class Node:
    def __init__(self, name, literal = False):
        self.name = name
        self.children = []
        self.isliteral = False
        if literal:
            self.children = [name]
            self.isliteral = True

    def __repr__(self):
        txt = self.name+'\n'
        for child in self.children:
            txt += child.__repr__().replace('\n','\n  ')
        txt += self.name.replace('<','</')+'\n'
        return txt

    def __str__(self):
        res = ''
        for c in self.children:
            res += str(c)
        return res

    def getElementsByTagName(self, name):
        res = []
        if self.name == name:
            res.append(self)
        for child in self.children:
            if type(child)!=str:
                res += child.getElementsByTagName(name)
        return res

    def toliteral(self):
        self.children = [str(self)]
        self.isliteral = True

    def __getitem__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0][x]

    def __len__(self):
        if not self.isliteral:return 1#raise Exception,'not a literal'
        return len(self.children[0])

    def __eq__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0] == x


stack = []
predicates = {}
bookends = {}
items = {}

class BNFException(Exception):
    pass

def splitchildren(text):
    """WORKS"""
    ors = [[]]
    i = 0
    ins = False
    while i<len(text):
        current = ''
        if text[i] in ' \t':
            i += 1
            continue
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
        elif text[i] in '*+?':
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
        if text[i:i+len(char)] != char:
            return False,0
        i += len(char)
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

                    if a < len(children)-2 and children[a+2] == '?':
                        # non-greedy
                        res, di = parsechildren(text, i, rule, children[a+3:])
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
    elif rule == "''":
        return ["'"]
    elif rule.startswith("'"):
        return [rule.strip("'")[0]]

    ret = []
    firsts[rule] = ret
    for one in rules[rule]:
        ret.append(flatten(first(one[0],rules)))
    return ret

rules = {}
def genrules(text):
    given = {}
    for x in text.split('\n'):
        if not x.strip():continue
        k,v = x.split(':',1)
        given[k.strip()] = splitchildren(v.strip())
    #first('<start>',given)
    for k in given:
        first(k,given)
    global rules
    rules = given

def totokens(node):
    assert node.name == 'start'
    for tokenw in node.children:
        yield tokenw.children[0].toliteral()

def parse(text):
    genrules(open('tokenize.bnf').read())
    print 'done genning'
    #for rule in firsts:
    #    print rule,firsts[rule]
    text = [Node(c,True) for c in text]
    nodes = parserule(text, 0, '<start>')
    return nodes

if __name__=='__main__':
    print [parse(open('check.py').read())[0]]
