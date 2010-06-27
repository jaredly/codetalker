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
        Token token
        ParseNode* next
        ParseNode* prev
        ParseNode* child

    struct State:
        Rules rules
        TokenStream tokens
        char** rule_names

cdef RuleItem* RuleSpecial_children

def grammar_parse_rule(unsigned int rule, tokenstream, rules, tokens, rule_names, error):
    cdef State state
    state.rules = make_rules(rules)
    state.tokens = make_tokens(tokenstream, tokens)
    state.rule_names = <char**>malloc(sizeof(char*) * len(rule_names))
    for i in range(len(rule_names)):
        state.rule_names[i] = <char*>malloc(sizeof(char) * (len(rule_names[i]) + 1))
        state.rule_names[i] = rule_names[i]
    cdef ParseNode* tree = parse_rule(0, &state, error)
    if tree == NULL:
        print 'error occurred: ', error
    res = to_parsetree(tree)
    return res

cdef object to_parsetree(ParseNode* node):
    # while (node.prev != NULL):
    #     node = node.prev
    res = [node.rule]
    # print 'to_parsetree', node.rule, node.token.which, node.child == NULL
    if node.child == NULL:
        if node.token.value == NULL:
            return 'nope'
        return node.token.which, node.token.value, node.token.lineno, node.token.charno
    cdef ParseNode* child = node.child
    while (child.prev != NULL):
        res.insert(1, to_parsetree(child))
        child = child.prev
    res.insert(1, to_parsetree(child))
    return res


cdef Rules make_rules(object rules):
    cdef Rules crules
    crules.num = len(rules)
    crules.rules = <Rule*>malloc(sizeof(Rule) * crules.num)
    for i in range(crules.num):
        crules.rules[i] = make_rule(rules[i])
    return crules

cdef Rule make_rule(object rule):
    cdef Rule crule
    crule.num = len(rule)
    crule.options = <RuleOption*>malloc(sizeof(RuleOption) * crule.num)
    for i in range(crule.num):
        crule.options[i] = make_option(rule[i])
    return crule

cdef RuleOption make_option(object option):
    cdef RuleOption coption
    coption.num = len(option)
    coption.items = <RuleItem*>malloc(sizeof(RuleItem) * coption.num)
    for i in range(coption.num):
        coption.items[i] = make_item(option[i])
    return coption

cdef RuleItem make_item(object item, bint from_or=False):
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
        else:
            print 'unknown special:', item[0]
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
        print 'token w/ value "%s" at (%d, %d)' % (tstream[i].value, tstream[i].lineno, tstream[i].charno)
    return ctokens

cdef ParseNode* parse_rule(unsigned int rule, State* state, object error):
    cdef ParseNode* node = <ParseNode*>malloc(sizeof(ParseNode))
    node.rule = rule
    print 'parsing rule ', state.rule_names[rule]
    node.next = NULL
    node.prev = NULL
    node.child = NULL
    node.token.value = NULL
    cdef ParseNode* res

    for i in range(state.rules.rules[rule].num):
        res = parse_children(rule, &state.rules.rules[rule].options[i], state, error)
        if res != NULL:
            node.child = res
            return node
    print 'failed', state.rule_names[rule]
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
    for i in range(option.num):
        ## include "ignore" stuff here
        if option.items[i].type == RULE:
            print 'child rule>'
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
            print 'token?', option.items[i].value.which, state.tokens.tokens[state.tokens.at].which, state.tokens.tokens[state.tokens.at].value
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
                continue
            elif state.tokens.at >= error[0]:
                error[0] = state.tokens.at
                error[1] = [rule, i, option.items[i].value.which]
            return NULL
        elif option.items[i].type == LITERAL:
            print 'literal?', option.items[i].value.text, state.tokens.tokens[state.tokens.at].value
            if state.tokens.at >= state.tokens.num:
                error[0] = state.tokens.at
                error[1] = 'Not enough tokens -- expecting', option.items[i].value.text
                print 'nope'
                return NULL
            if option.items[i].value.text == state.tokens.tokens[state.tokens.at].value:
                print 'yeah!'
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
            print 'nope'
            return NULL
        elif option.items[i].type == SPECIAL:
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
                    return NULL
                continue
            elif option.items[i].value.special.type == QUESTION:
                at = state.tokens.at
                new_option = <RuleOption*>malloc(sizeof(RuleOption))
                new_option.num = option.items[i].value.special.num
                new_option.items = option.items[i].value.special.children
                res = parse_children(rule, new_option, state, error)
                free(new_option)
                if res == NULL:
                    state.tokens.at = at
                else:
                    current = append_nodes(current, res)
                continue
            elif option.items[i].value.special.type == STRAIGHT:
                print 'straight'
                at = state.tokens.at
                new_option = <RuleOption*>malloc(sizeof(RuleOption))
                new_option.num = option.items[i].value.special.num
                new_option.items = option.items[i].value.special.children
                res = parse_children(rule, new_option, state, error)
                free(new_option)
                if res == NULL:
                    state.tokens.at = at
                    return NULL
                current = append_nodes(current, res)
            else:
                print 'unknown special', option.items[i].value.special.type, STAR, PLUS, OR, QUESTION
                error[1] = 'unknown special'
                return NULL
        else:
            error[1] = 'unknown rule type'
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


