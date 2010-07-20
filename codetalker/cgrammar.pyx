from stdlib cimport malloc, free

from codetalker.pgm.tokens import INDENT, DEDENT, EOF
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

cdef extern from "stdlib.h" nogil:
    char* strncpy(char* dest, char* src, int num)
    int strncmp(char* dest, char* src, int num)

cdef extern from "c/_speed_tokens.h":
    int check_ctoken(int tid, int at, char* text, int ln)
    int check_chartoken(char* chars, int num, int at, char* text, int ln)
    int check_stringtoken(char** strings, int num, int at, char* text, int ln)
    int t_white(int at, char* text, int ln)
    enum ttype:
        tTSTRING  # triple string
        tSSTRING  # single-quoted string
        tSTRING   # normal (double-quoted) string
        tID       # [a-zA-Z_][a-zA-Z_0-9]*
        tNUMBER   # ([1-9]+(\.\d*))|(\.\d+)
        tINT      # [1-9][0-9]*
        tCCOMMENT # // blah\n or /** blah **/
        tPYCOMMENT# # blah\n
        tWHITE    # space | \t
        tNEWLINE  # \n

cdef enum t_type:
    CTOKEN
    CHARTOKEN
    STRTOKEN
    RETOKEN
'''

from codetalker.pgm.token import Token, ReToken

ReToken._type = RETOKEN

class CToken(Token):
    _type = CTOKEN

class TSTRING(CToken):
    tid = tTSTRING
class SSTRING(CToken):
    tid = tSSTRING
class STRING(CToken):
    tid = tSTRING
class ID(CToken):
    tid = tID
class NUMBER(CToken):
    tid = tNUMBER
class INT(CToken):
    tid = tINT
class CCOMMENT(CToken):
    tid = tCCOMMENT
class PYCOMMENT(CToken):
    tid = tPYCOMMENT
class WHITE(CToken):
    tid = tWHITE
class NEWLINE(CToken):
    tid = tNEWLINE

class CharToken(Token):
    _type = CHARTOKEN
    chars = ''

class StringToken(Token):
    _type = STRTOKEN
    strings = []
    '''

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
        AstAttrs* ast_attrs
        char** rule_names

    struct Error:
        int at
        int reason
        Token* token
        char* text
        int wanted

    int store_grammar(Grammar gram)
    Grammar* load_grammar(int gid)
    void free_grammars()

    cParseNode* _get_parse_tree(int start, Grammar* gram, TokenStream* tokens, Error* error)

python_data = {}

def consume_grammar(rules, ignore, indent, rule_names, tokens, ast_attrs):
    cdef Grammar grammar
    grammar.rules = convert_rules(rules)
    grammar.ignore = convert_ignore(ignore)
    grammar.ast_attrs = convert_ast_attrs(ast_attrs)
    cdef int gid = store_grammar(grammar)
    python_data[gid] = rule_names, tokens, indent
    return gid

def get_tokens(gid, text):
    cdef Token* tokens = _get_tokens(gid, text)
    pytokens = convert_back_tokens(gid, tokens)
    kill_tokens(tokens)
    return pytokens

def get_parse_tree(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef Token* tokens = _get_tokens(gid, text)
    cdef TokenStream tsream = tokens_to_stream(tokens)
    tsream.eof = python_data[gid][1].index(EOF)
    cdef Error error
    cdef cParseNode* ptree = _get_parse_tree(0, grammar, &tsream, &error)
    pyptree = convert_back_ptree(gid, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return pyptree

def get_ast(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef Token* tokens = _get_tokens(gid, text)
    cdef TokenStream tsream = tokens_to_stream(tokens)
    tsream.eof = python_data[gid][1].index(EOF)
    cdef Error error
    cdef cParseNode* ptree = _get_parse_tree(0, grammar, &tsream, &error)
    # ast = _get_ast(grammar, gid, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return False

### CONVERT STUFF ###

cdef TokenStream tokens_to_stream(Token* tokens):
    cdef TokenStream ts
    ts.num = 1
    cdef Token* tmp = tokens
    while tmp.next != NULL:
        ts.num += 1
        tmp = tmp.next
    ts.tokens = <Token*>malloc(sizeof(Token)*ts.num)
    ts.at = 0
    return ts

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

cdef object convert_back_ptree(int gid, cParseNode* node):
    '''convert a cParseNode struct back to a python object'''
    if node.type == NTOKEN:
        if node.token.value == NULL:
            return None
        return python_data[gid][1][node.token.which](node.token.value, node.token.lineno, node.token.charno)
    current = ParseNode(node.rule, python_data[gid][0][node.rule])
    cdef cParseNode* child = node.child
    while child != NULL:
        res = convert_back_ptree(gid, child)
        if res is not None:
            current.prepend(res)
        child = child.prev
    return current

### KILL STUFF ###

cdef void kill_tokens(Token* start):
    cdef Token* tmp
    while start != NULL:
        tmp = start
        start = start.next
        free(tmp)

cdef void kill_ptree(cParseNode* node):
    if node.type == NTOKEN:
        free(node)
        return
    cdef cParseNode* child = node.child
    free(node)
    while child != NULL:
        node = child
        child = child.prev
        kill_ptree(node)

### TOKENIZE ###

cdef struct TokenState:
    int at
    int ln
    char* text
    int lineno
    int charno
    int* indents
    int num_indents
    int max_indents

cdef Token* _get_tokens(int gid, char* text):
    cdef:
        Token* start = NULL
        Token* current = NULL
        Token* tmp = NULL

        TokenState state

        int res = 0
        int num = 0
        int ntokens = len(tokens)
        char** strings = NULL
        bint indent = python_data[gid][2]

    state.at = 0
    state.text = text
    state.ln = len(text)
    state.lineno = 1
    state.charno = 1
    state.indents = <int*>malloc(sizeof(int)*100)
    state.num_indents = 0
    state.max_indents = 100

    tokens = python_data[gid][1]
    ID_t = tokens.index(INDENT)
    DD_t = tokens.index(DEDENT)

    while state.at < state.ln:
        for i from 0<=i<ntokens:
            if tokens[i]._type == CTOKEN:
                res = check_ctoken(tokens[i].tid, state.at, state.text, state.ln)
            elif tokens[i]._type == CHARTOKEN:
                res = check_chartoken(tokens[i].chars, tokens[i].num, state.at, state.text, state.ln)
            elif tokens[i]._type == STRTOKEN:
                num = len(tokens[i].strings)
                strings = <char**>malloc(sizeof(char*)*num)
                for m from 0<=m<num:
                    strings[m] = tokens[i][m]
                res = check_stringtoken(strings, num, state.at, state.text, state.ln)
            elif tokens[i]._type == RETOKEN:
                res = tokens[i].check(state.text[state.at:])

            if res:
                tmp = <Token*>malloc(sizeof(Token))
                tmp.value = <char*>malloc(sizeof(char)*(res+1))
                strncpy(tmp.value, state.text+state.at, res)
                tmp.which = i
                tmp.lineno = state.lineno
                tmp.charno = state.charno
                if start == NULL:
                    start = tmp
                else:
                    current.next = tmp
                current = tmp

                current = advance(res, current, indent, &state, ID_t, DD_t)
                state.at += res
                break

cdef Token* advance(int res, Token* current, bint indent, TokenState* state, int ID_t, int DD_t):
    cdef:
        int numlines = 0
        last = state.at
        ind = 0
    for i from state.at <= i < state.at + res:
        if state.text[i] == '\n':
            numlines+=1
            last = i
    state.lineno += numlines
    if numlines:
        state.charno = state.at + res - last
    else:
        state.charno += res
    if not indent:
        return current
    ## TODO: check indent
    return current




### ASTTIZE ###
