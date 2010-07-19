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
    int check_ctoken(int tid, int at, char* text)
    int check_chartoken(char* chars, int at, char* text)
    int check_stringtoken(char** strings, int num, int at, char* text)

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

    struct ParseNode:
        unsigned int rule
        NodeType type
        Token* token
        ParseNode* next
        ParseNode* prev
        ParseNode* child

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

    ParseNode _get_parse_tree(Grammar* gram, TokenStream tokens, Error error)

def consume_grammar(rules, ignore, tokens_list, ast_attrs):
    cdef Grammar grammar
    grammar.rules = convert_rules(rules)
    grammar.ignore = convert_ignore(ignore)
    grammar.tokens = convert_tokenslist(tokens_list)
    grammar.ast_attrs = convert_ast_attrs(ast_attrs)
    cdef int gid = store_grammar(grammar)
    return gid

def get_tokens(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    pytokens = convert_back_tokens(tokens)
    kill_tokens(tokens)
    return pytokens

def get_parse_tree(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    cdef ParseTree ptree = _get_parse_tree(grammar, tokens)
    pyptree = convert_back_ptree(ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return pyptree

def get_ast(gid, text):
    cdef Grammar* grammar = load_grammar(gid)
    cdef TokenStream tokens = _get_tokens(grammar, text)
    cdef ParseTree ptree = _get_parse_tree(grammar, tokens)
    ast = _get_ast(grammar, ptree)
    kill_ptree(ptree)
    kill_tokens(tokens)
    return ast

### CONVERT STUFF ###

cdef Rules convert_rules(object rules):
    cdef Rules



