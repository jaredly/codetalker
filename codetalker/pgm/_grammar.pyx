'''
_grammar.pyx: helper cython file for doing the hard parsing
work for codetalker.
Author: Jared Forsyth <jared@jaredforsyth.com>
'''
from stdlib cimport *

cdef:
    struct Token
    struct TokenStream
    struct RuleSpecial
    struct RuleItem

    struct Token:
        unsigned int which
        unsigned int lineno
        unsigned int charno
        char* value

    struct TokenStream:
        Token* tokens
        unsigned int num
        unsigned int at

    struct IgnoreTokens:
        unsigned int* tokens
        unsigned int num

    enum RuleItemType:
        LITERAL, RULE, TOKEN, SPECIAL

    enum RuleSpecialType:
        STAR, PLUS, QUESTION, OR, STRAIGHT

    struct RuleSpecial:
        RuleSpecialType type
        RuleItem* children
        unsigned int num

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

    struct Rules:
        unsigned int num
        Rule* rules

    enum NodeType:
        NNODE, NTOKEN

    struct ParseNode:
        unsigned int rule
        NodeType type
        Token token # TODO make pointer
        ParseNode* next
        ParseNode* prev
        ParseNode* child

    struct State:
        Rules rules
        TokenStream tokens
        char** rule_names
        IgnoreTokens ignore

cdef RuleItem* RuleSpecial_children

def grammar_parse_rule(unsigned int rule, tokenstream, rules, tokens, ignore, rule_names, error):
    cdef State state
    state.rules = make_rules(rules)
    state.tokens = make_tokens(tokenstream, tokens)
    state.ignore = make_ignore(ignore, tokens)
    state.rule_names = <char**>malloc(sizeof(char*) * len(rule_names))
    for i in range(len(rule_names)):
        state.rule_names[i] = rule_names[i]
    cdef ParseNode* tree = parse_rule(0, &state, error)
    free(state.rule_names)
    if tree == NULL:
        print 'error occurred: ', error
    res = to_parsetree(tree)
    return res

cdef object to_parsetree(ParseNode* node):
    res = [node.rule]
    # print 'to_parsetree', node.rule, node.token.which, node.child == NULL
    if node.child == NULL:
        if node.token.value == NULL:
            return
        return node.token.which, node.token.value, node.token.lineno, node.token.charno
    cdef ParseNode* tmp
    cdef ParseNode* child = node.child
    while (child.prev != NULL):
        cres = to_parsetree(child)
        if cres:
            res.insert(1, cres)
        tmp = child
        child = child.prev
        free(tmp)
    cres = to_parsetree(child)
    if cres:
        res.insert(1, cres)
    free(child)
    return res

cdef Rules make_rules(object rules):
    '''convert pythonic rules to use optimized C structs'''
    cdef Rules crules
    crules.num = len(rules)
    crules.rules = <Rule*>malloc(sizeof(Rule) * crules.num)
    for i in range(crules.num):
        crules.rules[i] = make_rule(rules[i])
    return crules

cdef Rule make_rule(object rule):
    '''convert pythonic rules to use optimized C structs'''
    cdef Rule crule
    crule.num = len(rule)
    crule.options = <RuleOption*>malloc(sizeof(RuleOption) * crule.num)
    for i in range(crule.num):
        crule.options[i] = make_option(rule[i])
    return crule

cdef RuleOption make_option(object option):
    '''convert pythonic rule options to use optimized C structs'''
    cdef RuleOption coption
    coption.num = len(option)
    coption.items = <RuleItem*>malloc(sizeof(RuleItem) * coption.num)
    for i in range(coption.num):
        coption.items[i] = make_item(option[i])
    return coption

cdef RuleItem make_item(object item, bint from_or=False):
    '''convert pythonic rule items to use optimized C structs'''
    cdef RuleItem citem
    cdef RuleOption option
    cdef bint to_or = False
    if type(item) == int:
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
        if from_or:
            citem.value.special.type = STRAIGHT
            citem.value.special.children = <RuleItem*>malloc(sizeof(RuleItem) * (len(item)))
            citem.value.special.num = len(item)
            for i in range(len(item)):
                citem.value.special.children[i] = make_item(item[i])
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
        #else:
#            log('unknown special:', item[0])
        citem.value.special.num = len(item)-1
        citem.value.special.children = <RuleItem*>malloc(sizeof(RuleItem) * (len(item)-1))
        for i in range(len(item)-1):
            citem.value.special.children[i] = make_item(item[i+1], to_or)
    return citem

cdef TokenStream make_tokens(tstream, tokens):
    cdef TokenStream ctokens
    ctokens.num = len(tstream)
    ctokens.tokens = <Token*>malloc(sizeof(Token) * ctokens.num)
    for i in range(ctokens.num):
        ctokens.tokens[i].which = tokens.index(tstream[i].__class__)
        ctokens.tokens[i].lineno = tstream[i].lineno
        ctokens.tokens[i].charno = tstream[i].charno
        ctokens.tokens[i].value = tstream[i].value
        # print 'token w/ value "%s" at (%d, %d)' % (tstream[i].value, tstream[i].lineno, tstream[i].charno)
    return ctokens

cdef IgnoreTokens make_ignore(ignore, tokens):
    cdef IgnoreTokens cignore
    cignore.num = len(ignore)
    cignore.tokens = <unsigned int*>malloc(sizeof(unsigned int)*cignore.num)
    for i in range(cignore.num):
        cignore.tokens[i] = tokens.index(ignore[i])
    return cignore

indent = [0]
def log(*what):
    st = [str(x) for x in what]
    print '  ' * len(indent), ' '.join(st)

cdef ParseNode* parse_rule(unsigned int rule, State* state, object error):
    cdef ParseNode* node = <ParseNode*>malloc(sizeof(ParseNode))
    node.rule = rule
#    log('parsing rule ', state.rule_names[rule])
#    indent.append(0)
    node.next = NULL
    node.prev = NULL
    node.child = NULL
    node.token.value = NULL
    cdef ParseNode* res

    for i in range(state.rules.rules[rule].num):
        res = parse_children(rule, &state.rules.rules[rule].options[i], state, error)
        if res != NULL:
            node.child = res
#            indent.pop(0)
#            log('sucess')
            return node
#    indent.pop(0)
#    log('failed', state.rule_names[rule])
    return NULL

cdef ParseNode* parse_children(unsigned int rule, RuleOption* option, State* state, object error):
    cdef ParseNode* current = <ParseNode*>malloc(sizeof(ParseNode))
    current.rule = rule
    current.next = NULL
    current.prev = NULL
    current.child = NULL
    current.token.value = NULL
    cdef unsigned int i = 0
    cdef unsigned int at
    cdef ParseNode* res
    cdef RuleOption *new_option
    cdef bint ignore
    for i in range(option.num):
        ## include "ignore" stuff here
        while True:
            ignore = False
            for m in range(state.ignore.num):
                if state.tokens.tokens[state.tokens.at].which == state.ignore.tokens[m]:
                    ignore = True
                    break
            if not ignore:
                break
            res = <ParseNode*>malloc(sizeof(ParseNode))
            res.prev = current
            res.next = NULL
            res.child = NULL
            res.token.value = NULL
            current.next = res
            res.token = state.tokens.tokens[state.tokens.at]
            current = res
            state.tokens.at += 1
        if option.items[i].type == RULE:
            at = state.tokens.at
            res = parse_rule(option.items[i].value.which, state, error)
            if res == NULL:
                state.tokens.at = at
                if state.tokens.at >= error[0]:
                    error[0] = state.tokens.at
                    error[1] = [rule, i]
                return NULL
            current = append_nodes(current, res)
            continue
        elif option.items[i].type == TOKEN:
#            log('token?', option.items[i].value.which, state.tokens.tokens[state.tokens.at].which, state.tokens.tokens[state.tokens.at].value)
            if state.tokens.at >= state.tokens.num:
                error[0] = state.tokens.at
                error[1] = 'Not enough tokens -- expecting', option.items[i].value.which
                return NULL
            if state.tokens.tokens[state.tokens.at].which == option.items[i].value.which:
                res = <ParseNode*>malloc(sizeof(ParseNode))
                res.prev = current
                res.next = NULL
                res.child = NULL
                res.token.value = NULL
                current.next = res
                res.token = state.tokens.tokens[state.tokens.at]
                current = res
                state.tokens.at += 1
#                log('good token')
                continue
            elif state.tokens.at >= error[0]:
                error[0] = state.tokens.at
                error[1] = [rule, i, option.items[i].value.which]
#            log('bad token...')
            return NULL
        elif option.items[i].type == LITERAL:
#            log('literal?', option.items[i].value.text, state.tokens.tokens[state.tokens.at].value)
            if state.tokens.at >= state.tokens.num:
                error[0] = state.tokens.at
                error[1] = 'Not enough tokens -- expecting', option.items[i].value.text
#                log('nope')
                return NULL
            if option.items[i].value.text == state.tokens.tokens[state.tokens.at].value:
#                log('yeah!')
                res = <ParseNode*>malloc(sizeof(ParseNode))
                res.prev = current
                res.next = NULL
                res.child = NULL
                res.token.value = NULL
                current.next = res
                res.token = state.tokens.tokens[state.tokens.at]
                current = res
                state.tokens.at += 1
                continue
            elif state.tokens.at >= error[0]:
                error[0] = state.tokens.at
                error[1] = [rule, i, option.items[i].value.text]
#            log('nope')
            return NULL
        elif option.items[i].type == SPECIAL:
#            log('special', option.items[i].value.special.type)
#            indent.append(0)
            if option.items[i].value.special.type == STAR:
                while 1:
                    at = state.tokens.at
                    new_option = <RuleOption*>malloc(sizeof(RuleOption))
                    new_option.num = option.items[i].value.special.num
                    new_option.items = option.items[i].value.special.children
                    res = parse_children(rule, new_option, state, error)
                    free(new_option)
                    if res == NULL:
                        state.tokens.at = at
                        break
                    current = append_nodes(current, res)
#                indent.pop(0)
#                log('done starring')
                continue
            elif option.items[i].value.special.type == PLUS:
                at = state.tokens.at
                new_option = <RuleOption*>malloc(sizeof(RuleOption))
                new_option.num = option.items[i].value.special.num
                new_option.items = option.items[i].value.special.children
                res = parse_children(rule, new_option, state, error)
                free(new_option)
                if res == NULL:
                    state.tokens.at = at
#                    indent.pop(0)
#                    log('plus fail')
                    return NULL
                current = append_nodes(current, res)
                while 1:
                    at = state.tokens.at
                    new_option = <RuleOption*>malloc(sizeof(RuleOption))
                    new_option.num = option.items[i].value.special.num
                    new_option.items = option.items[i].value.special.children
                    res = parse_children(rule, new_option, state, error)
                    free(new_option)
                    if res == NULL:
                        state.tokens.at = at
                        break
                    current = append_nodes(current, res)
#                indent.pop(0)
#                log('+done')
                continue
            elif option.items[i].value.special.type == OR:
                at = state.tokens.at
                for e in range(option.items[i].value.special.num):
                    new_option = <RuleOption*>malloc(sizeof(RuleOption))
                    new_option.num = 1
                    new_option.items = &option.items[i].value.special.children[e]
                    res = parse_children(rule, new_option, state, error)
                    free(new_option)
                    if res != NULL:
                        current = append_nodes(current, res)
                        break
                    else:
                        state.tokens.at = at
                else:
#                    indent.pop(0)
#                    log('failed or')
                    return NULL
#                indent.pop(0)
#                log('OR success')
                continue
            elif option.items[i].value.special.type == QUESTION:
                at = state.tokens.at
                new_option = <RuleOption*>malloc(sizeof(RuleOption))
                new_option.num = option.items[i].value.special.num
                new_option.items = option.items[i].value.special.children
                res = parse_children(rule, new_option, state, error)
                free(new_option)
#                indent.pop(0)
                if res == NULL:
                    state.tokens.at = at
#                    log('failed, but i dont care')
                else:
                    current = append_nodes(current, res)
                continue
            elif option.items[i].value.special.type == STRAIGHT:
#                log('straight')
                at = state.tokens.at
                new_option = <RuleOption*>malloc(sizeof(RuleOption))
                new_option.num = option.items[i].value.special.num
                new_option.items = option.items[i].value.special.children
                res = parse_children(rule, new_option, state, error)
                free(new_option)
                if res == NULL:
                    state.tokens.at = at
#                    indent.pop(0)
#                    log('failed...')
                    return NULL
                current = append_nodes(current, res)
#                indent.pop(0)
            else:
#                log('unknown special', option.items[i].value.special.type, STAR, PLUS, OR, QUESTION)
                error[1] = 'unknown special'
#                indent.pop(0)
                return NULL
        else:
            error[1] = 'unknown rule type'
#            log('unknown rule type!!!', option.items[i].type, RULE, TOKEN, SPECIAL, LITERAL)
            continue
            return NULL
    return current

cdef ParseNode* append_nodes(ParseNode* one, ParseNode* two):
    cdef ParseNode* tmp = two
    while tmp.prev != NULL:
        tmp = tmp.prev
    one.next = tmp
    tmp.prev = one
    return two


# cdef parse_rule(unsigned int rule, tokens, error, rules, tokens):
    # pass


# vim: et sw=4 sts=4


