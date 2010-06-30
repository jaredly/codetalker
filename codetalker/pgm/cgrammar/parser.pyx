from codetalker.pgm.cgrammar.structs cimport *
from libc.stdlib cimport *

cdef ParseNode* _new_parsenode(unsigned int rule):
    cdef ParseNode* node = <ParseNode*>malloc(sizeof(ParseNode))
    node.rule = rule
    node.next = NULL
    node.prev = NULL
    node.child = NULL
    node.token = NULL
    node.type = NNODE
    return node

indent = []

def log(*a):
    strs = []
    for e in a:strs.append(str(e))
    print '  |'*len(indent), ' '.join(strs)

cdef ParseNode* parse_rule(unsigned int rule, State* state, object error):
    cdef ParseNode* node = _new_parsenode(rule)
    cdef ParseNode* tmp
    log('parsing rule', rule)
    indent.append(0)
    for i from 0<=i<state.rules.rules[rule].num:
        log('child rule:', i)
        tmp = parse_children(rule, &state.rules.rules[rule].options[i], state, error)
        if tmp != NULL:
            node.child = tmp
            indent.pop(0)
            return node
    indent.pop(0)
    return NULL

cdef ParseNode* parse_children(unsigned int rule, RuleOption* option, State* state, object error):
    cdef:
        ParseNode* current = NULL
        unsigned int i = 0
        unsigned int at = 0
        ParseNode* tmp = NULL
        RuleItem* item = NULL
        bint ignore
    log('children of', rule)
    indent.append(0)
    for i from 0<=i<option.num:
        item = &option.items[i]
        log('item', i)
        while state.tokens.at < state.tokens.num:
            ignore = False
            for m from 0<=m<state.ignore.num:
                if state.tokens.tokens[state.tokens.at].which == state.ignore.tokens[m]:
                    ignore = True
                    break
            if not ignore:
                break
            log('ignoring white')
            tmp = _new_parsenode(rule)
            tmp.token = &state.tokens.tokens[state.tokens.at]
            tmp.type = NTOKEN
            current = append_nodes(current, tmp)
            state.tokens.at += 1
        if state.tokens.at >= state.tokens.num:
            error[0] = state.tokens.at
            error[1] = ['Not enough tokens -- expecting', rule, i, item.value.which]
            log('not enough tokens')
            indent.pop(0)
            return NULL
        if item.type == RULE:
            at = state.tokens.at
            tmp = parse_rule(item.value.which, state, error)
            if tmp == NULL:
                state.tokens.at = at
                if state.tokens.at >= error[0]:
                    error[0] = at
                    error[1] = [rule, i]
                indent.pop(0)
                return NULL
            current = append_nodes(current, tmp)
            continue
        elif item.type == TOKEN:
            log('token... [looking for', item.value.which, '] got', state.tokens.tokens[state.tokens.at].which)
            if state.tokens.tokens[state.tokens.at].which == item.value.which:
                tmp = _new_parsenode(rule)
                tmp.token = &state.tokens.tokens[state.tokens.at]
                tmp.type = NTOKEN
                current = append_nodes(current, tmp)
                state.tokens.at += 1
            else:
                if state.tokens.at > error[0]:
                    error[0] = state.tokens.at
                    error[1] = [rule, i, option.items[i].value.which]
                log('failed token')
                indent.pop(0)
                return NULL
        elif item.type == LITERAL:
            log('looking for literal', item.value.text)
            if item.value.text == state.tokens.tokens[state.tokens.at].value:
                tmp = _new_parsenode(rule)
                tmp.token = &state.tokens.tokens[state.tokens.at]
                tmp.type = NTOKEN
                current = append_nodes(current, tmp)
                state.tokens.at += 1
                log('success!!')
            else:
                if state.tokens.at > error[0]:
                    error[0] = state.tokens.at
                    error[1] = [rule, i, option.items[i].value.which]
                log('failed...literally')
                indent.pop(0)
                return NULL
        elif item.type == SPECIAL:
            tmp = check_special(rule, item.value.special, current, state, error)
            if tmp == NULL:
                indent.pop(0)
                return NULL
            current = tmp
    indent.pop(0)
    return current

cdef ParseNode* check_special(unsigned int rule, RuleSpecial special, ParseNode* current, State* state, error):
    cdef ParseNode* tmp
    log('special')
    indent.append(0)
    if special.type == STAR:
        log('star!')
        while state.tokens.at < state.tokens.num:
            at = state.tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state.tokens.at = at
                break
            current = append_nodes(current, tmp)
        indent.pop(0)
        return current
    elif special.type == PLUS:
        log('plus!')
        at = state.tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            state.tokens.at = at
            log('failed plus')
            indent.pop(0)
            return NULL
        current = append_nodes(current, tmp)
        while state.tokens.at < state.tokens.num:
            at = state.tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state.tokens.at = at
                break
            current = append_nodes(current, tmp)
        log('ggod plus')
        indent.pop(0)
        return current
    elif special.type == OR:
        log('or!')
        at = state.tokens.at
        for i from 0<=i<special.option.num:
            tmp = parse_children(rule, special.option.items[i].value.special.option, state, error)
            if tmp != NULL:
                current = append_nodes(current, tmp)
                indent.pop(0)
                return current
        indent.pop(0)
        return NULL
    elif special.type == QUESTION:
        log('?maybe')
        at = state.tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            log('not taking it')
            indent.pop(0)
            return current
        current = append_nodes(current, tmp)
        indent.pop(0)
        return current
    else:
        print 'unknown special type:', special.type
        indent.pop(0)
        return NULL
    log('umm shouldnt happen')
    indent.pop(0)
    return NULL

cdef ParseNode* append_nodes(ParseNode* one, ParseNode* two):
    if one == NULL:return two
    cdef ParseNode* tmp = two
    while tmp.prev != NULL:
        tmp = tmp.prev
    one.next = tmp
    tmp.prev = one
    return two





