from stdlib cimport malloc, free

from codetalker.pgm.errors import ParseError

'''Stuff in here:

available to python:

    consume_grammar
    get_tokens
    get_parse_tree
    get_ast

from c:

    struct Grammar
    struct TokenStream
    struct Error

    # grammar handle
    load_grammar
    store_grammar

    # tokenize stuff
    check_ctoken(int tid, int at, char* text)
    check_chartoken(char* chars, int at, char* text)
    check_stringtoken(char** strings, int num, int at, char* text)

    # parse stuff
    _get_parse_tree(Grammar grammar, TokenStream tokens, Error error)

everythin else is in here.
'''

cdef extern from "c/speed_tokens.h":
    int check_ctoken(int tid, int at, char* text, int ln)
    int check_chartoken(char* chars, int at, char* text, int ln)
    int check_stringtoken(char** strings, int num, int at, char* text, int ln)
    int white(int at, char* text, int ln);

cdef extern from "c/parser.h":
    struct Token
    struct TokenStream
    struct RuleSpecial
    struct RuleOption

    struct Token:
        unsigned int which
        unsigned int lineno
        unsigned int charno
        char* value
        Token* next

    struct TokenStream:
        Token* tokens
        unsigned int num
        unsigned int at
        unsigned int eof

    struct IgnoreTokens:
        unsigned int* tokens
        unsigned int num

    enum RuleItemType:
        LITERAL, RULE, TOKEN, SPECIAL

    enum RuleSpecialType:
        STAR, PLUS, QUESTION, OR, STRAIGHT

    struct RuleSpecial:
        RuleSpecialType type
        RuleOption* option

    union ItemValue:
        unsigned int which
        RuleSpecial special
        char* text

    struct RuleItem:
        RuleItemType type
        ItemValue value

    struct RuleOption:
        RuleItem* items
        unsigned int num

    struct Rule:
        RuleOption* options
        unsigned int num
        bint dont_ignore
        unsigned int which

    struct Rules:
        unsigned int num
        Rule* rules

    enum NodeType:
        NNODE, NTOKEN

    struct cParseNode:
        unsigned int rule
        NodeType type
        Token* token
        cParseNode* next
        cParseNode* prev
        cParseNode* child

    struct AstAttr:
        char* name
        unsigned int single
        unsigned int numtypes
        int* types
        int start
        int end
        int step

    struct AstAttrs:
        unsigned int num
        AstAttr* attrs

    struct Grammar:
        Rules rules
        IgnoreTokens ignore
        TokenStream tokens
        AstAttrs ast_attrs
        char** rule_names

    int store_grammar(Grammar gram)
    Grammar* load_grammar(int gid)
    void free_grammars

    cParseNode _get_parse_tree(Grammar* gram, TokenStream tokens, Error error)

python_data = {}

def consume_grammar(rules, ignore, rule_names, tokens, ast_attrs):
    cdef Grammar grammar
    grammar.rules = convert_rules(rules)
    grammar.ignore = convert_ignore(ignore)
    grammar.ast_attrs = convert_ast_attrs(ast_attrs)
    cdef int gid = store_grammar(grammar)
    python_data[gid] = rule_names, tokens
    return gid

def get_tokens(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    pytokens = convert_back_tokens(gid, tokens)
    kill_tokens(tokens)
    return pytokens

def get_parse_tree(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    cdef ParseTree ptree = _get_parse_tree(grammar, tokens)
    pyptree = convert_back_ptree(gid, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return pyptree

def get_ast(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    cdef ParseTree ptree = _get_parse_tree(grammar, tokens)
    ast = _get_ast(grammar, gid, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return ast

### CONVERT STUFF ###

cdef Rules convert_rules(object rules):
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

cdef IgnoreTokens convert_ignore(object ignore):
    cdef IgnoreTokens itokens
    itokens.num = len(ignore)
    itokens.tokens = <unsigned int*>malloc(sizeof(unsigned int)*itokens.num)
    for i from 0<=i<itokens.num:
        itokens.tokens[i] = ignore[i]
    return itokens

cdef AstAttrs* convert_ast_attrs(object ast_attrs):
    cdef AstAttrs* result = <AstAttrs*>malloc(sizeof(AstAttrs)*len(ast_attrs))
    for i from 0<=i<len(ast_attrs):
        keys = ast_attrs[i].keys()
        result[i].num = len(keys)
        result[i].attrs = <AstAttr*>malloc(sizeof(AstAttr)*result[i].num);
        for m from 0<=m<result[i].num:
            result[i].attrs[m] = convert_ast_attr(keys[m], ast_attrs[i][keys[m]])
    return result

cdef AstAttr convert_ast_attr(char* name, object ast_attr):
    cdef AstAttr attr
    attr.name = name
    if type(ast_attr) != dict:
        ast_attr = {'type':ast_attr}
    attr.single = type(ast_attr.get('type')) != list
    if attr.single:
        attr.numtypes = 1
        attr.types = <int*>malloc(sizeof(int))
        attr.types[0] = ast_attr['type']
    else:
        attr.numtypes = len(ast_attr['type'])
        attr.types = <int*>malloc(sizeof(int)*attr.numtypes)
        for i from 0<=i<attr.numtypes:
            attr.types[i] = ast_attr['type'][i]

    attr.start = ast_attr.get('start', 0)
    attr.end = ast_attr.get('end', 0)
    attr.step = ast_attr.get('step', 1)

    return attr

### CONVERT IT BACK ###

cdef object convert_back_tokens(int gid, Token* start):
    res = []
    while start != NULL:
        res.append(python_data[gid][1][start.which](start.value, start.lineno, start.charno))
        start = start.next
    return res

class ParseNode(object):
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

cdef object convert_back_ptree(int gid, cParseNode* start):
    '''convert a cParseNode struct back to a python object'''
    if node.type == NTOKEN:
        if node.token.value == NULL:
            return None
        return python_data[gid][1][node.token.which](node.token.value, node.token.lineno, node.token.charno)
    current = ParseNode(node.rule, python_data[gid][0][node.rule])
    cdef cParseNode* child = node.child
    while child != NULL:
        res = convert_back_ptree(child)
        if res is not None:
            current.prepend(res)
        child = child.prev
    return current

### KILL STUFF ###


### TOKENIZE ###


### ASTTIZE ###
