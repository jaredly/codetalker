# cython: profile=True
from stdlib cimport malloc, free

from codetalker.pgm.tokens import INDENT, DEDENT, EOF, Token as PyToken, ReToken
from codetalker.pgm.errors import ParseError, TokenError, AstError

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
    check_idtoken(char** strings, int num, int at, char* text)

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
    int check_idtoken(char** strings, int num, int at, char* text, int ln)
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

cdef extern from "c/parser.h":
    struct Token
    struct TokenStream
    struct RuleSpecial
    struct RuleOption

    enum t_type:
        CTOKEN
        CHARTOKEN
        STRTOKEN
        RETOKEN
        IDTOKEN

    union PTokenValue:
        char** strings
        char* chars
        int tid

    struct PToken:
        unsigned int which
        t_type type
        PTokenValue value
        int num

    struct PTokens:
        unsigned int num
        PToken* tokens

    struct cTokenError:
        int lineno
        int charno
        char* text

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
        unsigned int pass_single

    struct Grammar:
        Rules rules
        IgnoreTokens ignore
        AstAttrs* ast_attrs
        PTokens tokens
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
    int matches(cParseNode* node, int which)
    void _kill_ptree(cParseNode* node)
    Token* c_get_tokens(Grammar* grammar, char* text, int indent, cTokenError* error)

ReToken._type = RETOKEN

class CToken(PyToken):
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

class CharToken(PyToken):
    _type = CHARTOKEN
    chars = ''

class StringToken(PyToken):
    _type = STRTOKEN
    strings = []

class IdToken(PyToken):
    _type = IDTOKEN
    strings = []

python_data = {}

def consume_grammar(rules, ignore, indent, rule_names, rule_funcs, tokens, ast_attrs):
    cdef Grammar grammar
    grammar.rules = convert_rules(rules)
    grammar.ignore = convert_ignore(ignore, tokens)
    grammar.ast_attrs = convert_ast_attrs(ast_attrs, rule_funcs, tokens)
    grammar.tokens = convert_ptokens(tokens)
    cdef int gid = store_grammar(grammar)
    python_data[gid] = rule_names, tokens, indent
    return gid

def get_tokens(gid, text):
    cdef cTokenError error
    error.text = ''

    cdef Token* tokens
    cdef Grammar* grammar = load_grammar(gid)
    if grammar.tokens.num != -1:
        tokens = c_get_tokens(grammar, text, python_data[gid][2], &error)
    else:
        tokens = _get_tokens(gid, text, &error)

    if tokens == NULL:
        if len(error.text):
            raise TokenError(error.text, error.lineno, error.charno)
    pytokens = convert_back_tokens(gid, tokens)
    kill_tokens(tokens)
    return pytokens

def get_parse_tree(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef cTokenError terror
    terror.text = ''

    cdef Token* tokens
    if grammar.tokens.num != -1:
        tokens = c_get_tokens(grammar, text, python_data[gid][2], &terror)
    else:
        tokens = _get_tokens(gid, text, &terror)

    if tokens == NULL:
        if len(terror.text):
            raise TokenError(terror.text, terror.lineno, terror.charno)
    cdef TokenStream tstream = tokens_to_stream(tokens)
    tstream.eof = python_data[gid][1].index(EOF)
    cdef Error error
    error.text = '(no error)'
    cdef cParseNode* ptree = _get_parse_tree(0, grammar, &tstream, &error)
    if tstream.at < tstream.num-1:
        print "Didn't use all the tokens (%d out of %d)" % (error.at+1, tstream.num)
        raise ParseError('Didn\'t use all the tokens: %s' % error.text, error.token.lineno, error.token.charno)
    pyptree = convert_back_ptree(gid, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return pyptree

def get_ast(gid, text, ast_classes, ast_tokens):
    cdef Grammar* grammar = load_grammar(gid)
    cdef cTokenError terror
    terror.text = ''

    cdef Token* tokens
    if grammar.tokens.num != -1:
        tokens = c_get_tokens(grammar, text, python_data[gid][2], &terror)
    else:
        tokens = _get_tokens(gid, text, &terror)

    if tokens == NULL:
        if len(terror.text):
            raise TokenError(terror.text, terror.lineno, terror.charno)
    cdef TokenStream tstream = tokens_to_stream(tokens)
    tstream.eof = python_data[gid][1].index(EOF)
    cdef Error error
    error.text = '(no error reported)'
    error.at = 0
    error.wanted = 0
    cdef cParseNode* ptree = _get_parse_tree(0, grammar, &tstream, &error)
    if tstream.at < tstream.num-1:
        print "Didn't use all the tokens (%d out of %d)" % (error.at+1, tstream.num)
        raise ParseError('Didn\'t use all the tokens: %s (failed on #%d "%s")' % (error.text, error.at, tstream.tokens[error.at].value), error.token.lineno, error.token.charno)
    ast = _get_ast(grammar, gid, ptree, ast_classes, ast_tokens)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return ast

### CONVERT STUFF ###

cdef TokenStream tokens_to_stream(Token* tokens):
    cdef TokenStream ts
    ts.num = 0
    cdef Token* tmp = tokens
    while tmp != NULL:
        ts.num += 1
        tmp = tmp.next
    ts.tokens = <Token*>malloc(sizeof(Token)*ts.num)
    ts.at = 0
    for i from 0<=i<ts.num:
        ts.tokens[i] = tokens[0]
        tokens = tokens.next
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

cdef IgnoreTokens convert_ignore(object ignore, object tokens):
    cdef IgnoreTokens itokens
    itokens.num = len(ignore)
    itokens.tokens = <unsigned int*>malloc(sizeof(unsigned int)*itokens.num)
    for i from 0<=i<itokens.num:
        itokens.tokens[i] = tokens.index(ignore[i])
    return itokens

cdef AstAttrs* convert_ast_attrs(object ast_attrs, object rules, object tokens):
    cdef AstAttrs* result = <AstAttrs*>malloc(sizeof(AstAttrs)*len(ast_attrs))
    for i from 0<=i<len(ast_attrs):
        # print ast_attrs[i],i
        if ast_attrs[i]['pass_single']:
            result[i].pass_single = 1
            continue
        else:
            result[i].pass_single = 0
        keys = ast_attrs[i]['attrs'].keys()
        result[i].num = len(keys)
        if len(keys):
            result[i].attrs = <AstAttr*>malloc(sizeof(AstAttr)*result[i].num);
        else:
            result[i].attrs = NULL

        for m from 0<=m<result[i].num:
            result[i].attrs[m] = convert_ast_attr(keys[m], ast_attrs[i]['attrs'][keys[m]], rules, tokens)
    return result

cdef object which_rt(object it, object rules, object tokens):
    if it in rules:
        return rules[it]
    elif it in tokens:
        return -(1 + tokens.index(it))
    raise Exception('invalid AST type: %s' % it)

cdef AstAttr convert_ast_attr(char* name, object ast_attr, object rules, object tokens):
    cdef AstAttr attr
    attr.name = name
    if type(ast_attr) != dict:
        ast_attr = {'type':ast_attr}
    attr.single = type(ast_attr.get('type')) != list
    if attr.single:
        attr.numtypes = 1
        attr.types = <int*>malloc(sizeof(int))
        attr.types[0] = which_rt(ast_attr['type'], rules, tokens)
    else:
        attr.numtypes = len(ast_attr['type'])
        attr.types = <int*>malloc(sizeof(int)*attr.numtypes)
        for i from 0<=i<attr.numtypes:
            attr.types[i] = which_rt(ast_attr['type'][i], rules, tokens)

    attr.start = ast_attr.get('start', 0)
    attr.end = ast_attr.get('end', 0)
    attr.step = ast_attr.get('step', 1)

    return attr

cdef PTokens convert_ptokens(object tokens):
    cdef PTokens ptokens
    ptokens.num = len(tokens) - 3 # don't include INDENT, DEDENT, and EOF
    ptokens.tokens = <PToken*>malloc(sizeof(PToken)*ptokens.num)
    for i from 0<=i<ptokens.num:
        if isinstance(tokens[i], ReToken):
            ptokens.num = -1
            return ptokens
        ptokens.tokens[i].which = i
        if issubclass(tokens[i], CToken):
            ptokens.tokens[i].type = CTOKEN
            ptokens.tokens[i].value.tid = tokens[i].tid
        elif issubclass(tokens[i], StringToken):
            ptokens.tokens[i].type = STRTOKEN
            ptokens.tokens[i].num = len(tokens[i].strings)
            ptokens.tokens[i].value.strings = <char**>malloc(sizeof(char*)*ptokens.tokens[i].num)
            for m from 0<=m<ptokens.tokens[i].num:
                ptokens.tokens[i].value.strings[m] = tokens[i].strings[m]
        elif issubclass(tokens[i], CharToken):
            ptokens.tokens[i].type = CHARTOKEN
            ptokens.tokens[i].num = len(tokens[i].chars)
            ptokens.tokens[i].value.chars = tokens[i].chars
        elif issubclass(tokens[i], IdToken):
            ptokens.tokens[i].type = IDTOKEN
            ptokens.tokens[i].num = len(tokens[i].strings)
            ptokens.tokens[i].value.strings = <char**>malloc(sizeof(char*)*ptokens.tokens[i].num)
            for m from 0<=m<ptokens.tokens[i].num:
                ptokens.tokens[i].value.strings[m] = tokens[i].strings[m]
        else:
            ptokens.num = -1
            print 'failed'
            return ptokens
    return ptokens

### CONVERT IT BACK ###

cdef object convert_back_tokens(int gid, Token* start):
    res = []
    while start != NULL:
        res.append(python_data[gid][1][start.which](start.value, start.lineno, start.charno))
        start = start.next
    return res

class ParseNode(object):
    def __init__(self, rule, name):
        self.rule = rule
        self.name = name
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
    
    def __repr__(self):
        return u'<ParseNode type="%s" itype="%d" children="%d" str="%s">' % (self.name, self.rule, len(self.children), str(self))

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
    _kill_ptree(node)

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

cdef Token* _get_tokens(int gid, char* text, cTokenError* error):
    tokens = python_data[gid][1]
    cdef:
        Token* start = NULL
        Token* current = NULL
        Token* tmp = NULL

        TokenState state

        int res = 0
        int num = 0
        int ntokens = len(tokens) - 3 # ignore INDENT, DEDENT, EOF
        char** strings = NULL
        bint indent = python_data[gid][2]

    state.at = 0
    state.text = text
    state.ln = len(text)
    # print "tokenizing '%s' (length %d)'" % (str(text).encode('string_escape'), state.ln)
    state.lineno = 1
    state.charno = 1

    state.num_indents = 1
    state.indents = <int*>malloc(sizeof(int)*100)
    state.indents[0] = 0
    state.max_indents = 100

    ID_t = tokens.index(INDENT)
    DD_t = tokens.index(DEDENT)

    while state.at < state.ln:
        # print 'at',state.at
        for i from 0<=i<ntokens:
            # print 'for token', tokens[i]
            if tokens[i]._type == CTOKEN:
                res = check_ctoken(tokens[i].tid, state.at, state.text, state.ln)
            elif tokens[i]._type == CHARTOKEN:
                # print 'chartoken', tokens[i].chars, tokens[i].num
                res = check_chartoken(tokens[i].chars, len(tokens[i].chars), state.at, state.text, state.ln)
            elif tokens[i]._type == STRTOKEN:
                # print 'stringtoken', tokens[i].strings
                num = len(tokens[i].strings)
                strings = <char**>malloc(sizeof(char*)*num)
                for m from 0<=m<num:
                    strings[m] = tokens[i].strings[m]
                res = check_stringtoken(strings, num, state.at, state.text, state.ln)
            elif tokens[i]._type == IDTOKEN:
                num = len(tokens[i].strings)
                strings = <char**>malloc(sizeof(char*)*num)
                for m from 0<=m<num:
                    strings[m] = tokens[i].strings[m]
                res = check_idtoken(strings, num, state.at, state.text, state.ln)
            elif tokens[i]._type == RETOKEN:
                res = tokens[i].check(state.text[state.at:])
            else:
                print 'Unknown token type', tokens[i]._type, tokens[i]

            if res:
                tmp = <Token*>malloc(sizeof(Token))
                tmp.value = <char*>malloc(sizeof(char)*(res+1))
                strncpy(tmp.value, state.text + state.at, res)
                tmp.value[res] = '\0'
                # print 'got token!', res, state.at, [tmp.value], state.lineno, state.charno
                tmp.which = i
                tmp.next = NULL
                tmp.lineno = state.lineno
                tmp.charno = state.charno
                if start == NULL:
                    start = tmp
                else:
                    current.next = tmp
                current = tmp

                current = advance(res, current, indent, &state, ID_t, DD_t, error)
                if current == NULL:
                    return NULL
                state.at += res
                break
        else:
            error.text = 'no valid token found'
            error.lineno = state.lineno
            error.charno = state.charno
            return NULL
    # print 'done tokenizing'
    return start

cdef Token* advance(int res, Token* current, bint indent, TokenState* state, int ID_t, int DD_t, cTokenError* error):
    cdef:
        int numlines = 0
        int cindent
        int last = state.at
        int ind = 0
        Token* tmp
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
    if indent and res == 1 and state.text[state.at] == <char>'\n':
        ind = t_white(state.at + 1, state.text, state.ln)
        if ind < 0:
            return current
        cindent = state.indents[state.num_indents - 1]
        if ind > cindent:
            add_indent(state, ind)
            tmp = <Token*>malloc(sizeof(Token))
            tmp.value = ''
            tmp.which = ID_t
            tmp.next = NULL
            tmp.lineno = state.lineno
            tmp.charno = state.charno
            current.next = tmp
            current = tmp
        elif ind < cindent:
            while ind < cindent:
                state.num_indents -= 1
                tmp = <Token*>malloc(sizeof(Token))
                tmp.value = ''
                tmp.which = DD_t
                tmp.next = NULL
                tmp.lineno = state.lineno
                tmp.charno = state.charno
                current.next = tmp
                current = tmp
                cindent = state.indents[state.num_indents - 1]
            if ind != cindent:
                etxt = 'invalid indentation -- %d (expected %d)' % (ind, cindent)
                error.text = etxt
                error.lineno = state.lineno
                error.charno = state.charno
                return NULL
    return current

cdef void add_indent(TokenState* state, int ind):
    cdef int* indents
    if state.num_indents == state.max_indents:
        indents = <int*>malloc(sizeof(int)*state.max_indents*2)
        for i from 0<=i<state.max_indents:
            indents[i] = state.indents[i]
        free(state.indents)
        state.indents = indents
        state.max_indents *= 2
    state.indents[state.num_indents] = ind
    state.num_indents += 1

### ASTTIZE ###

cdef object _get_ast(Grammar* grammar, int gid, cParseNode* node, object ast_classes, object ast_tokens):
    # print 'getting ast'
    if node == NULL:
        return None
    if node.type == NTOKEN:
        if node.token.value == NULL:
            return None
        return python_data[gid][1][node.token.which](node.token.value, node.token.lineno, node.token.charno)
    cdef AstAttrs attrs = grammar.ast_attrs[node.rule]
    cdef cParseNode* child
    cdef cParseNode* start
    cdef int cnum
    cdef int stepnum
    start = node.child
    while start.prev != NULL:
        start.prev.next = start
        start = start.prev

    name = python_data[gid][0][node.rule]
    if attrs.pass_single:
        # print 'pass single'
        child = start
        while child != NULL:
            if child.type != NTOKEN or child.token.which in ast_tokens:
                return _get_ast(grammar, gid, child, ast_classes, ast_tokens)
            child = child.next
    elif not attrs.num:
        # print 'pass multi'
        res = []
        child = start
        while child != NULL:
            if child.type != NTOKEN or child.token.which in ast_tokens:
                res.append(_get_ast(grammar, gid, child, ast_classes, ast_tokens))
            child = child.next
        return res

    obj = getattr(ast_classes, name)()

    for i from 0<=i<attrs.num:
        # print 'attr num', i, 'of', attrs.num
        child = start
        if attrs.attrs[i].single:
            cnum = 0
            stepnum = 0
            # print 'stype'
            while child != NULL:
                # print 'looking', attrs.attrs[i].numtypes
                # print attrs.attrs[i].types[0]
                if matches(child, attrs.attrs[i].types[0]):
                    # print 'match!'
                    if stepnum == 0 and cnum >= attrs.attrs[i].start:
                        setattr(obj, attrs.attrs[i].name, _get_ast(grammar, gid, child, ast_classes, ast_tokens))
                        break
                    # print '(but not gotten)'
                    cnum += 1
                    stepnum += 1
                    if stepnum == attrs.attrs[i].step:
                        stepnum = 0
                child = child.next
            else:
                raise AstError('No child nodes match astAttr %s' % attrs.attrs[i].name)
        else:
            kids = []
            setattr(obj, attrs.attrs[i].name, kids)
            cnum = 0
            # print 'mtype'
            while child != NULL:
                for m from 0<=m<attrs.attrs[i].numtypes:
                    if matches(child, attrs.attrs[i].types[m]):
                        # print 'match!'
                        if cnum >= attrs.attrs[i].start and (attrs.attrs[i].end == 0 or cnum < attrs.attrs[i].end):
                            kids.append(_get_ast(grammar, gid, child, ast_classes, ast_tokens))
                        # else:
                            # print '(but not gotten)'
                        cnum += 1
                        stepnum += 1
                        if stepnum == attrs.attrs[i].step:
                            stepnum = 0
                        break
                child = child.next
    # print 'got ast'
    return obj

