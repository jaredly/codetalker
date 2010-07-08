from libc.stdlib cimport free

cdef void ignore(IgnoreTokens ignore):
    free(ignore.tokens)

cdef void rules(Rules rules):
    for i from 0<=i<rules.num:
        kill_rule(rules.rules[i])
    free(rules.rules)

cdef void kill_rule(Rule rule):
    for i from 0<=i<rule.num:
        kill_option(rule.options[i])
    free(rule.options)

cdef void kill_option(RuleOption option):
    for i from 0<=i<option.num:
        kill_item(option.items[i])
    free(option.items)

cdef void kill_item(RuleItem item):
    if item.type == SPECIAL:
        kill_option(item.value.special.option[0])
        free(item.value.special.option)

cdef void tokens(Token* token):
    if token.value != NULL and len(token.value):
        free(token.value)
    if token.next != NULL:
        tokens(token.next)
    free(token)

cdef void nodes(ParseNode* node):
    if node == NULL:
        return
    if node.prev != NULL:
        nodes(node.prev)
    if node.child != NULL:
        nodes(node.child)
    if node.token != NULL:
        pass
        # free(node.token)
    free(node)

