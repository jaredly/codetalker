
#include "parser.h"
#include "stdlib.h"

/** grammar storage and loading **/

struct Grammar* grammars = 0;
int numgrammars = 0;
int gsize = 0;

int store_grammar(struct Grammar gram) {
    int i;
    if (gsize == numgrammars) {
        struct Grammar* oldgrammars = grammars;
        grammars = (struct Grammar*)malloc(sizeof(struct Grammar)*(gsize + 5));
        for (i=0;i<numgrammars;i++) {
            grammars[i] = oldgrammars[i];
        }
        if (numgrammars != 0) {
            free(oldgrammars);
        }
        gsize += 5;
    }
    grammars[numgrammars] = gram;
    numgrammars += 1;
}

struct Grammar* load_grammar(int gid) {
    return &grammars[gid];
}

void free_grammars() {
    free(grammars);
}

/** @end grammar storage and loading **/

/** parsing then? **/

struct ParseNode _get_parse_tree(struct Grammar* gram, struct TokenStream tokens, struct Error error) {

}

struct ParseNode* _new_parsenode(unsigned int rule) {
    struct ParseNode* node = (struct ParseNode*)malloc(sizeof(struct ParseNode));
    node->rule = rule;
    node->next = NULL;
    node->prev = NULL;
    node->child = NULL;
    node->token = NULL;
    node->type = NNODE;
    return node;
}

/**
// indent = []

def log(*a):pass
def log_(*a):
    strs = []
    for e in a:strs.append(str(e))
    print '  |'*len(indent), ' '.join(strs)
    **/
struct ParseNode* parse_children(unsigned int rule, struct RuleOption* option, struct Grammar* state, struct Error* error);

// clean
struct ParseNode* parse_rule(unsigned int rule, struct Grammar* state, struct Error* error) {
    struct ParseNode* node = _new_parsenode(rule);
    struct ParseNode* tmp;
    int i;
    // log('parsing rule', rule)
    // indent.append(0);
    for (i=0; i < state->rules.rules[rule].num; i++) {
        // log('child rule:', i)
        tmp = parse_children(rule, &(state->rules.rules[rule].options[i]), state, error);
        if (tmp != NULL) {
            // log('child success!', i)
            node->child = tmp;
            // indent.pop(0)
            return node;
        }
    }
    // indent.pop(0)
    return NULL;
}

// clean
struct ParseNode* parse_children(unsigned int rule, struct RuleOption* option, struct Grammar* state, struct Error* error) {
    struct ParseNode* current = NULL;
    unsigned int i = 0, m = 0;
    unsigned int at = 0;
    struct ParseNode* tmp = NULL;
    struct RuleItem* item = NULL;
    int ignore;
    // indent.append(0)
    for (i=0;i<option->num;i++) {
        item = &option->items[i];
        while (state->tokens.at < state->tokens.num) {
            ignore = 0;
            for (m=0;m<state->ignore.num;m++) {
                if (state->tokens.tokens[state->tokens.at].which == state->ignore.tokens[m]) {
                    ignore = 1;
                    break;
                }
            }
            if (ignore == 0) {
                break;
            }
            // log('ignoring white')
            tmp = _new_parsenode(rule);
            tmp->token = &state->tokens.tokens[state->tokens.at];
            tmp->type = NTOKEN;
            current = append_nodes(current, tmp);
            state->tokens.at += 1;
        }
        if (item->type == RULE) {
            if (0 && state->tokens.at >= state->tokens.num) { // disabling
                error->at = state->tokens.at;
                error->reason = 1;
                error->token = NULL;
                error->text = "ran out";
                // error[1] = ['ran out', rule, i, item->value.which];
                // log('not enough tokens')
                // indent.pop(0)
                return NULL;
            }
            at = state->tokens.at;
            tmp = parse_rule(item->value.which, state, error);
            if (tmp == NULL) {
                state->tokens.at = at;
                if (state->tokens.at >= error->at) {
                    error->at = state->tokens.at;
                    error->reason = 2;
                    error->token = &state->tokens.tokens[state->tokens.at];
                    error->text = "rule failed";
                }
                // indent.pop(0)
                return NULL;
            }
            current = append_nodes(current, tmp);
            continue;
        } else if (item->type == TOKEN) {
            if (state->tokens.at >= state->tokens.num) {
                if (item->value.which == state->tokens.eof) {
                    // log('EOF -- passing')
                    tmp = _new_parsenode(rule);
                    tmp->token = (struct Token*)malloc(sizeof(struct Token));
                    tmp->token->value = NULL;
                    tmp->token->which = state->tokens.eof;
                    tmp->token->lineno = -1;
                    tmp->token->charno = -1;
                    tmp->type = NTOKEN;
                    current = append_nodes(current, tmp);
                    continue;
                }
                error->at = state->tokens.at;
                error->reason = 1;
                error->token = NULL;
                error->text = "ran out";
                // log('not enough tokens')
                // indent.pop(0)
                return NULL;
            }
            // log('token... [looking for', item->value.which, '] got', state->tokens.tokens[state->tokens.at].which)
            if (state->tokens.tokens[state->tokens.at].which == item->value.which) {
                tmp = _new_parsenode(rule);
                tmp->token = &state->tokens.tokens[state->tokens.at];
                tmp->type = NTOKEN;
                current = append_nodes(current, tmp);
                state->tokens.at += 1;
                continue;
            } else {
                if (state->tokens.at > error->at) {
                    error->at = state->tokens.at;
                    error->reason = 3;
                    error->token = &state->tokens.tokens[state->tokens.at];
                    error->text = "token failed";
                    error->wanted = option->items[i].value.which;
                }
                // log('failed token')
                // indent.pop(0)
                return NULL;
            }
        } else if (item->type == LITERAL) {
            if (state->tokens.at >= state->tokens.num) {
                error->at = state->tokens.at;
                error->reason = 1;
                error->token = NULL;
                error->text = "ran out";
                // log('not enough tokens')
                // indent.pop(0)
                return NULL;
            }
            // log('looking for literal', item->value.text)
            if (item->value.text == state->tokens.tokens[state->tokens.at].value) {
                tmp = _new_parsenode(rule);
                tmp->token = &state->tokens.tokens[state->tokens.at];
                tmp->type = NTOKEN;
                current = append_nodes(current, tmp);
                state->tokens.at += 1;
                continue;
                // log('success!!')
            } else {
                if (state->tokens.at > error->at) {
                    error->at = state->tokens.at;
                    error->reason = 4;
                    error->token = &state->tokens.tokens[state->tokens.at];
                    error->text = item->value.text;
                }
                // log('failed...literally', state->tokens.tokens[state->tokens.at].value)
                // indent.pop(0)
                return NULL;
            }
        } else if (item->type == SPECIAL) {
            tmp = check_special(rule, item->value.special, current, state, error);
            if (tmp == NULL) {
                // indent.pop(0)
                return NULL;
            }
            current = tmp;
        }
    }
    // indent.pop(0)
    return current;
}

/**
struct ParseNode* check_special(unsigned int rule, struct RuleSpecial special, struct ParseNode* current, struct Grammar* state, struct Error error):
    struct ParseNode* tmp
    // log('special')
    // indent.append(0)
    if special.type == STAR:
        // log('star!')
        while state->tokens.at < state->tokens.num:
            at = state->tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state->tokens.at = at
                break
            current = append_nodes(current, tmp)
        // log('awesome star')
        // indent.pop(0)
        return current
    elif special.type == PLUS:
        // log('plus!')
        at = state->tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            state->tokens.at = at
            // log('failed plus')
            // indent.pop(0)
            return NULL
        current = append_nodes(current, tmp)
        while state->tokens.at < state->tokens.num:
            at = state->tokens.at
            tmp = parse_children(rule, special.option, state, error)
            if tmp == NULL:
                state->tokens.at = at
                break
            current = append_nodes(current, tmp)
        // log('good plus')
        // indent.pop(0)
        return current
    elif special.type == OR:
        // log('or!')
        at = state->tokens.at
        for i from 0<=i<special.option->num:
            tmp = parse_children(rule, special.option->items[i].value.special.option, state, error)
            if tmp != NULL:
                // log('got or...')
                current = append_nodes(current, tmp)
                // indent.pop(0)
                return current
        // log('fail or')
        // indent.pop(0)
        return NULL
    elif special.type == QUESTION:
        // log('?maybe')
        at = state->tokens.at
        tmp = parse_children(rule, special.option, state, error)
        if tmp == NULL:
            // log('not taking it')
            // indent.pop(0)
            return current
        current = append_nodes(current, tmp)
        // log('got maybe')
        // indent.pop(0)
        return current
    else:
        print 'unknown special type:', special.type
        // indent.pop(0)
        return NULL
    // log('umm shouldnt happen')
    // indent.pop(0)
    return NULL

ParseNode* append_nodes(ParseNode* one, ParseNode* two):
    if one == NULL:return two
    ParseNode* tmp = two
    while tmp->prev != NULL:
        tmp = tmp->prev
    one.next = tmp
    tmp->prev = one
    return two
**/

