from libc.stdlib cimport malloc
from codetalker.pgm.cgrammar.structs cimport *

cdef TokenStream tokens(tstream):
    cdef TokenStream ctokens
    ctokens.num = len(tstream)
    ctokens.tokens = <Token*>malloc(sizeof(Token) * ctokens.num)
    for i in range(ctokens.num):
        ctokens.tokens[i].which = tstream[i].which
        ctokens.tokens[i].lineno = tstream[i].lineno
        ctokens.tokens[i].charno = tstream[i].charno
        ctokens.tokens[i].value = tstream[i].value
    return ctokens

cdef Rules rules(object rules):
    cdef Rules crules
    crules.num = len(rules)
    crules.rules = <Rule*>malloc(sizeof(Rule)*crules.num)
    for i from 0<=i<crules.num:
        crules.rules[i] = convert_rule(rules[i], i)
    return crules

cdef Rule convert_rule(object rule, unsigned int i):
    cdef Rule crule
    crule.which = i
    crule.dont_ignore = rule.dont_ignore
    crule.num = len(rule.options)
    crule.options = <RuleOption*>malloc(sizeof(RuleOption)*crule.num)
    for i from 0<=i<crule.num:
        crule.options[i] = convert_option(rule.options[i])
    return crule

cdef RuleOption convert_option(object option, to_or=False):
    cdef RuleOption coption
    coption.num = len(option)
    coption.items = <RuleItem*>malloc(sizeof(RuleItem) * coption.num)
    for i from 0<=i<coption.num:
        coption.items[i] = convert_item(option[i], to_or)
    return coption

cdef RuleItem convert_item(object item, bint from_or=False):
    cdef RuleItem citem
    cdef RuleOption* option
    cdef bint to_or = False
    if type(item) == int:
        # rule or token
        if item >= 0:
            citem.type = RULE
            citem.value.which = item
        else:
            citem.type = TOKEN
            citem.value.which = -(item + 1)
    elif type(item) == str:
        citem.type = LITERAL
        citem.value.text = item
    else:
        citem.type = SPECIAL
        citem.value.special.option = <RuleOption*>malloc(sizeof(RuleOption))
        if from_or:
            citem.value.special.type = STRAIGHT
            citem.value.special.option[0] = convert_option(item)
            return citem
        if item[0] == '*':
            citem.value.special.type = STAR
        elif item[0] == '+':
            citem.value.special.type = PLUS
        elif item[0] == '|':
            citem.value.special.type = OR
            to_or = True
        elif item[0] == '?':
            citem.value.special.type = QUESTION

        citem.value.special.option[0] = convert_option(item[1:], to_or)
    return citem

cdef IgnoreTokens ignore(object ignore):
    cdef IgnoreTokens itokens
    itokens.num = len(ignore)
    itokens.tokens = <unsigned int*>malloc(sizeof(unsigned int)*itokens.num)
    for i from 0<=i<itokens.num:
        itokens.tokens[i] = ignore[i]
    return itokens

cdef object tokens_back(Token* start):
    res = []
    while start != NULL:
        res.append((start.which, start.lineno, start.charno, start.value))
        start = start.next
    return res

class pyParseNode(object):
    def __init__(self, rule):
        self.rule = rule
        self.children = []
        self.parent = None
    
    def append(self, child):
        self.children.append(child)
        child.parent = self

    def prepend(self, child):
        self.children.insert(0, child)
        child.parent = self

    def __str__(self):
        strs = []
        for child in self.children:
            strs.append(str(child))
        return ''.join(strs)

class pyToken(object):
    def __init__(self, type, value, lineno=-1, charno=-1):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.charno = charno
        self.parent = None

    def __str__(self):
        return self.value

ind = []
cdef object nodes_back(ParseNode* node):
    '''convert a ParseNode struct back to a python object (a tuple)'''
    if node.type == NTOKEN:
        if node.token.value == NULL:
            return None
        return pyToken(node.token.which, node.token.value, node.token.lineno, node.token.charno)
    current = pyParseNode(node.rule)
    cdef ParseNode* child = node.child
    ind.append(0)
    while child != NULL:
        res = nodes_back(child)
        if res is not None:
            current.prepend(res)
        child = child.prev
    ind.pop(0)
    return current

