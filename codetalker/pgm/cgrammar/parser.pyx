from codetalker.pgm.cgrammar.structs cimport *
from libc.stdlib cimport *

cdef ParseNode* _new_parsenode(unsigned int rule):
    cdef ParseNode* node = <ParseNode*>malloc(sizeof(ParseNode))
    node.rule = rule
    node.next = NULL
    node.prev = NULL
    node.child = NULL
    node.token.value = NULL
    return node

cdef ParseNode* parse_rule(unsigned int rule, State* state, object error):
    cdef ParseNode* node = _new_parsenode(rule)
    cdef ParseNode* tmp
    for i from 0<=i<state.rules.rules[rule].num:
        tmp = parse_children(rule, &state.rules.rules[rule].options[i], state, error)
        if tmp != NULL:
            node.child = tmp
            return node
    return NULL

cdef ParseNode* parse_children(unsigned int rule, RuleOption* option, State* state, object error):
    cdef:
        ParseNode* current = _new_parsenode(rule)
        unsigned int i = 0
        unsigned int at = 0
        ParseNode* tmp = NULL
        RuleItem* item = NULL
        bint ignore

    for i from 0<=i<option.num:
        item = &option.items[i]
        while state.tokens.at < state.tokens.num:
            ignore = False
            for m from 0<=m<state.ignore.num:
                if state.tokens.tokens[state.tokens.at].which == state.ignore.tokens[m]:
                    ignore = True
                    break
            if not ignore:
                break
            tmp = _new_parsenode(rule)
            tmp.token = &state.tokens.tokens[state.tokens.at]
            tmp.prev = current
            current.next = tmp
            current = tmp
            state.tokens.at += 1
        if state.tokens.at >= state.tokens.num:
            error[0] = state.tokens.at
            error[1] = ['Not enough tokens -- expecting', rule, i, item.value.which]
            return NULL
        if item.type == RULE:
            at = state.tokens.at
            tmp = parse_rule(item.value.which, state, error)
            if tmp == NULL:
                state.tokens.at = at
                if state.tokens.at >= error[0]:
                    error[0] = at
                    error[1] = [rule, i]
                return NULL
            current = append_nodes(current, tmp)
            continue
        elif item.type == TOKEN:
            if state.tokens.tokens[state.tokens.at].which == item.value.which:
                tmp = _new_parsenode(rule)
                tmp.prev = current
                current.next = tmp
                tmp.token = &state.tokens.tokens[state.tokens.at]
                current = tmp
                state.tokens.at += 1
            else:
                if state.tokens.at > error[0]:
                    error[0] = state.tokens.at
                    error[1] = [rule, i, option.items[i].value.which]
                return NULL
        elif item.type == LITERAL:
            if item.value.text == state.tokens.tokens[state.tokens.at].value:
                tmp = _new_parsenode(rule)
                tmp.prev = current
                tmp.token = &state.tokens.tokens[state.tokens.at]
                current.next = tmp
                current = tmp
                state.tokens.at += 1
            else:
                if state.tokens.at > error[0]:
                    error[0] = state.tokens.at
                    error[1] = [rule, i, option.items[i].value.which]
                return NULL
        elif item.type == SPECIAL:
            tmp = check_special(rule, item.value.special, current, state, error)
            if tmp == NULL:
                return NULL
            current = tmp
    return current

cdef ParseNode* check_special(unsigned int rule, RuleSpecial special, ParseNode* current, State* state, error):
    cdef ParseNode* tmp
    if special.type == STAR:
        while state.tokens.at < state.tokens.num:
            at = state.tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state.tokens.at = at
                break
            current = append_nodes(current, tmp)
        return current
    elif special.type == PLUS:
        at = state.tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            state.tokens.at = at
            return NULL
        current = append_nodes(current, tmp)
        while state.tokens.at < state.tokens.num:
            at = state.tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state.tokens.at = at
                break
            current = append_nodes(current, tmp)
        return current
    elif special.type == OR:
        at = state.tokens.at
        for i from 0<=i<special.option.num:
            tmp = parse_children(rule, special.option.items[i].value.special.option, state, error)
            if tmp != NULL:
                current = append_nodes(current, tmp)
                return current
        return NULL
    elif special.type == QUESTION:
        at = state.tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            return current
        current = append_nodes(current, tmp)
        return current
    else:
        print 'unknown special type:', special.type
        return NULL
    return NULL

cdef ParseNode* append_nodes(ParseNode* one, ParseNode* two):
    cdef ParseNode* tmp = two
    while tmp.prev != NULL:
        tmp = tmp.prev
    one.next = tmp
    tmp.prev = one
    return two





