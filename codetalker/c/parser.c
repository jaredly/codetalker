
#include "parser.h"
#include "stdlib.h"
#include <string.h>
#include "stdio.h"
#include "c/_speed_tokens.h"

#ifdef DEBUG
#define LOG(...) pind();printf(__VA_ARGS__)
#define INDENT() indent += IND
#define DEDENT() indent -= IND
#else
#define LOG(...) // LOG
#define INDENT() // indent
#define DEDENT() // dedent
#endif

char sentinel = 0;
#define UNINITIALIZED ((void *)&sentinel)

int matches(struct cParseNode* node, int which) {
    if (which < 0) {
        if (node->type != NTOKEN || node->token == NULL || node->token->which != -(1 + which)) {
            return 0;
        }
        return 1;
    } else {
        if (node->rule == which) {
            return 1;
        } else {
            return 0;
        }
    }
}

void _kill_ptree(struct cParseNode* node) {
    if (node->type == NTOKEN) {
        free(node);
    } else {
        struct cParseNode* child = node->child;
        free(node);
        while (child != NULL) {
            node = child;
            child = child->prev;
            _kill_ptree(node);
        }
    }
}

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
    return numgrammars-1;
}

struct Grammar* load_grammar(int gid) {
    return &grammars[gid];
};

void free_grammars() {
    free(grammars);
}

int indent = 0;
int IND = 4;

void pind(void) {
    int i;
    for (i=0;i<indent;i++) {
        printf(" ");
    }
}

/** @end grammar storage and loading **/

/** parsing then? **/

struct cParseNode* parse_rule(unsigned int rule, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error);
struct cParseNode* parse_children(unsigned int rule, struct RuleOption* option, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error);
struct cParseNode* append_nodes(struct cParseNode* one, struct cParseNode* two);
struct cParseNode* check_special(unsigned int rule, struct RuleSpecial special, struct cParseNode* current, struct Grammar* grammar, struct TokenStream* tokens,  struct Error* error);
struct cParseNode* _new_parsenode(unsigned int rule);

struct cParseNode* _get_parse_tree(int start, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error) {
    struct cParseNode* parent = parse_rule(start, grammar, tokens, error);
    if (parent == NULL) {
        return NULL;
    }
    struct cParseNode* current = parent->child;
    struct cParseNode* tmp;
    int m, ignore;
    int rule = start;
    LOG("ignore any trailing ignores\n");
    while (tokens->at < tokens->num) {
        ignore = 0;
        for (m=0;m<grammar->ignore.num;m++) {
            if (tokens->tokens[tokens->at].which == grammar->ignore.tokens[m]) {
                ignore = 1;
                break;
            }
        }
        if (ignore == 0) {
            break;
        }
        LOG("ignoring white\n");
        tmp = _new_parsenode(rule);
        tmp->token = &tokens->tokens[tokens->at];
        tmp->type = NTOKEN;
        current = append_nodes(current, tmp);
        LOG("inc token %d %d\n", tokens->at, tokens->at+1);
        tokens->at += 1;
    }
    parent->child = current;
    return parent;
}

struct cParseNode* _new_parsenode(unsigned int rule) {
    struct cParseNode* node = (struct cParseNode*)malloc(sizeof(struct cParseNode));
    node->rule = rule;
    node->next = NULL;
    node->prev = NULL;
    node->child = NULL;
    node->token = NULL;
    node->type = NNODE;
    return node;
}

struct cParseNode* parse_rule(unsigned int rule, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error) {
    struct cParseNode* node = _new_parsenode(rule);
    struct cParseNode* tmp;
    int i;
    LOG("parsing rule #%d %s (token at %d)\n", rule, grammar->rules.rules[rule].name, tokens->at);
    int at = tokens->at;
    INDENT();
    for (i=0; i < grammar->rules.rules[rule].num; i++) {
        tokens->at = at;
        tmp = parse_children(rule, &(grammar->rules.rules[rule].options[i]), grammar, tokens, error);
        if (tmp != NULL) {
            LOG("CHild success! %d\n", i);
            if (tmp != UNINITIALIZED) {
                node->child = tmp;
            }
            DEDENT();
            return node;
        }
    }
    LOG("failed rule %d\n", rule);
    DEDENT();
    tokens->at = at;
    return NULL;
}

// clean
struct cParseNode* parse_children(unsigned int rule, struct RuleOption* option, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error) {
    LOG("parsing children of %d (token at %d)\n", rule, tokens->at);
    struct cParseNode* current = UNINITIALIZED;
    unsigned int i = 0, m = 0;
    unsigned int at = 0;
    struct cParseNode* tmp = NULL;
    struct RuleItem* item = NULL;
    int ignore;
    INDENT();
    for (i=0;i<option->num;i++) {
        item = &option->items[i];
        if (!grammar->rules.rules[rule].dont_ignore) {
            while (tokens->at < tokens->num) {
                ignore = 0;
                for (m=0;m<grammar->ignore.num;m++) {
                    if (tokens->tokens[tokens->at].which == grammar->ignore.tokens[m]) {
                        ignore = 1;
                        break;
                    }
                }
                if (ignore == 0) {
                    break;
                }
                LOG("ignoring white\n");
                tmp = _new_parsenode(rule);
                tmp->token = &tokens->tokens[tokens->at];
                tmp->type = NTOKEN;
                current = append_nodes(current, tmp);
                LOG("inc token %d %d\n", tokens->at, tokens->at+1);
                tokens->at += 1;
            }
        }
        if (tokens->at < tokens->num) {
            LOG("At token %d '%s'\n", tokens->at, tokens->tokens[tokens->at].value);
        }
        if (item->type == RULE) {
            LOG(">RULE\n");
            /**
            if (0 && tokens->at >= tokens->num) { // disabling
                error->at = tokens->at;
                error->reason = 1;
                error->token = NULL;
                error->text = "ran out";
                // error[1] = ['ran out', rule, i, item->value.which];
                // log('not enough tokens')
                DEDENT();
                return NULL;
            }
            **/
            at = tokens->at;
            tmp = parse_rule(item->value.which, grammar, tokens, error);
            if (tmp == NULL) {
                tokens->at = at;
                if (tokens->at >= error->at && error->reason!=1 && error->reason!=4) {
                    error->at = tokens->at;
                    error->reason = 2;
                    error->token = &tokens->tokens[tokens->at];
                    error->text = "rule failed";
                    error->wanted = item->value.which;
                }
                DEDENT();
                return NULL;
            }
            current = append_nodes(current, tmp);
            continue;
        } else if (item->type == TOKEN) {
            LOG(">TOKEN\n");
            if (tokens->at >= tokens->num) {
                if (item->value.which == tokens->eof) {
                    LOG("EOF -- passing\n");
                    tmp = _new_parsenode(rule);
                    tmp->token = (struct Token*)malloc(sizeof(struct Token));
                    tmp->token->value = NULL;
                    tmp->token->which = tokens->eof;
                    tmp->token->lineno = -1;
                    tmp->token->charno = -1;
                    tmp->type = NTOKEN;
                    current = append_nodes(current, tmp);
                    continue;
                }
                LOG("no more tokens\n");
                error->at = tokens->at;
                error->reason = 1;
                error->token = NULL;
                error->text = "ran out";
                error->wanted = item->value.which;
                DEDENT();
                return NULL;
            }
            if (tokens->tokens[tokens->at].which == item->value.which) {
                LOG("got token! %d\n", item->value.which);
                tmp = _new_parsenode(rule);
                tmp->token = &tokens->tokens[tokens->at];
                tmp->type = NTOKEN;
                current = append_nodes(current, tmp);
                LOG("inc token %d %d\n", tokens->at, tokens->at+1);
                tokens->at += 1;
                continue;
            } else {
                if (tokens->at > error->at) {
                    error->at = tokens->at;
                    error->reason = 3;
                    error->token = &tokens->tokens[tokens->at];
                    error->text = "token failed";
                    error->wanted = option->items[i].value.which;
                }
                LOG("token failed (wanted %d, got %d)\n",
                        item->value.which, tokens->tokens[tokens->at].which);
                DEDENT();
                return NULL;
            }
        } else if (item->type == LITERAL) {
            LOG(">LITERAL\n");
            if (tokens->at >= tokens->num) {
                error->at = tokens->at;
                error->reason = 4;
                error->token = NULL;
                error->text = item->value.text;
                DEDENT();
                return NULL;
            }
            if (strcmp(item->value.text, tokens->tokens[tokens->at].value) == 0) {
                LOG("got literal!\n");
                tmp = _new_parsenode(rule);
                tmp->token = &tokens->tokens[tokens->at];
                tmp->type = NTOKEN;
                current = append_nodes(current, tmp);
                LOG("inc token %d %d\n", tokens->at, tokens->at+1);
                tokens->at += 1;
                continue;
            } else {
                if (tokens->at > error->at) {
                    error->at = tokens->at;
                    error->reason = 5;
                    error->token = &tokens->tokens[tokens->at];
                    error->text = item->value.text;
                }
                LOG("failed....literally: %s\n", item->value.text);
                DEDENT();
                return NULL;
            }
        } else if (item->type == SPECIAL) {
            LOG(">SPECIAL\n");
            tmp = check_special(rule, item->value.special, current, grammar, tokens, error);
            if (tmp == NULL) {
                LOG("FAIL SPECIAL\n");
                DEDENT();
                return NULL;
            }
            current = tmp;
        }
    }
    DEDENT();
    return current;
}

struct cParseNode* check_special(unsigned int rule, struct RuleSpecial special, struct cParseNode* current, struct Grammar* grammar, struct TokenStream* tokens, struct Error* error) {
    struct cParseNode* tmp;
    int at, i;
    LOG("special\n");
    INDENT();
    if (special.type == STAR) {
        LOG("star!\n");
        while (tokens->at < tokens->num) {
            at = tokens->at;
            tmp = parse_children(rule, special.option, grammar, tokens, error);
            if (tmp == NULL) {
                tokens->at = at;
                break;
            }
            current = append_nodes(current, tmp);
            if (at == tokens->at) {
                break;
            }
        }
        LOG("awesome star\n");
        DEDENT();
        return current;
    } else if (special.type == PLUS) {
        LOG("plus!\n");
        at = tokens->at;
        tmp = parse_children(rule, special.option, grammar, tokens, error);
        if (tmp == NULL) {
            tokens->at = at;
            LOG("failed plus\n");
            DEDENT();
            return NULL;
        }
        current = append_nodes(current, tmp);
        if (at == tokens->at) {
            return current;
        }
        while (tokens->at < tokens->num) {
            at = tokens->at;
            tmp = parse_children(rule, special.option, grammar, tokens, error);
            if (tmp == NULL) {
                tokens->at = at;
                break;
            }
            current = append_nodes(current, tmp);
            if (at == tokens->at) {
                break;
            }
        }
        LOG("good plus\n");
        DEDENT();
        return current;
    } else if (special.type == OR) {
        LOG("or!\n");
        at = tokens->at;
        for (i=0;i<special.option->num;i++) {
            // each of the child items with be of the special STRAIGHT option
            // type -> allowing the OR special to have a list of lists
            tmp = parse_children(rule, special.option->items[i].value.special.option, grammar, tokens, error);
            if (tmp != NULL) {
                LOG("got or...\n");
                current = append_nodes(current, tmp);
                DEDENT();
                return current;
            }
        }
        LOG("fail or\n");
        DEDENT();
        return NULL;
    } else if (special.type == QUESTION) {
        LOG("?maybe\n");
        at = tokens->at;
        tmp = parse_children(rule, special.option, grammar, tokens, error);
        LOG("done maybe children\n");
        if (tmp == NULL) {
            LOG("not taking it\n");
            tokens->at = at;
            DEDENT();
            return current;
        }
        current = append_nodes(current, tmp);
        LOG("got maybe\n");
        DEDENT();
        return current;
    } else if (special.type == NOIGNORE) {
        LOG("no ignore (initial %d)\n", grammar->rules.rules[rule].dont_ignore);
        int before_ignore = grammar->rules.rules[rule].dont_ignore;
        at = tokens->at;
        grammar->rules.rules[rule].dont_ignore = 1;
        tmp = parse_children(rule, special.option, grammar, tokens, error);
        grammar->rules.rules[rule].dont_ignore = before_ignore;
        if (tmp == NULL) {
            tokens->at = at;
            LOG("failed ignore\n");
            DEDENT();
            return NULL;
        }
        current = append_nodes(current, tmp);
        LOG("ignore success! back to %d %d", grammar->rules.rules[rule].dont_ignore, before_ignore);
        DEDENT();
        return current;
    } else if (special.type == NOT) {
        LOG("NOT\n");
        at = tokens->at;
        tmp = parse_children(rule, special.option, grammar, tokens, error);
        if (tmp == NULL) {
            if (tokens->at < tokens->num) {
                tmp = _new_parsenode(rule);
                tmp->token = &tokens->tokens[tokens->at];
                tmp->type = NTOKEN;
                tokens->at += 1;
                current = append_nodes(current, tmp);
                LOG("awesome. eating token\n");
            } else {
                LOG("not enough tokens to eat\n");
                at = tokens->at;
                return NULL;
            }
            DEDENT();
            return current;
        }
        LOG("nope, it passed\n");
        tokens->at = at;
        DEDENT();
        return NULL;
    } else {
        LOG("unknown special type: %s\n", special.type);
        DEDENT();
        return NULL;
    }
    LOG("umm shouldnt happen");
    DEDENT();
    return NULL;
}

struct cParseNode* append_nodes(struct cParseNode* one, struct cParseNode* two) {
    LOG("appending nodes; %d to %d\n", (int)one, (int)two);
    if (one == UNINITIALIZED) {
        LOG("good (noone)\n");
        return two;
    } else if (one == NULL) {
        return two;
    } else if (two == NULL) {
        return one;
    } else if (two == UNINITIALIZED) {
        return one;
    }
    struct cParseNode* tmp = two;
    LOG("getting prev\n");
    while (tmp->prev != NULL) {
        tmp = tmp->prev;
    }
    LOG("got prev\n");
    one->next = tmp;
    LOG("mid\n");
    tmp->prev = one;
    LOG("good\n");
    return two;
}

/** tokenizing **/

struct TokenState {
    int at;
    int ln;
    char* text;
    int lineno;
    int charno;
    int* indents;
    int num_indents;
    int max_indents;
};

struct Token* advance_token(int res, struct Token* current, int indent, struct TokenState* state, char* text, int ID_t, int DD_t, struct cTokenError* error);

struct Token* c_get_tokens(struct Grammar* grammar, char* text, int indent, struct cTokenError* error) {
    struct Token* start = NULL;
    struct Token* current = NULL;
    struct Token* tmp = NULL;

    struct TokenState state;
    state.at = 0;
    state.ln = strlen(text);
    // state.text = text;
    state.lineno = 1;
    state.charno = 1;
    state.indents = (int*)malloc(sizeof(int)*100);
    state.indents[0] = 0;
    state.max_indents = 100;
    state.num_indents = 1;

    struct PToken ptoken;

    int ID_t = grammar->tokens.num;
    int DD_t = grammar->tokens.num+1;

    int res = 0;

    int dirty;

    // printf("with text:: %s\n\n", text);

    while (state.at < state.ln) {
        int i;
        dirty = 0;
        for (i=0;i<grammar->tokens.num;i++) {
            // printf("looking for token: %d\n", i);
            ptoken = grammar->tokens.tokens[i];
            switch (ptoken.type) {
                case CTOKEN:
                    res = check_ctoken(ptoken.value.tid, state.at, text, state.ln, grammar->idchars);
                    break;
                case CHARTOKEN:
                    res = check_chartoken(ptoken.value.chars, ptoken.num, state.at, text, state.ln);
                    break;
                case STRTOKEN:
                    res = check_stringtoken(ptoken.value.strings, ptoken.num, state.at, text, state.ln);
                    break;
                case IDTOKEN:
                    res = check_idtoken(ptoken.value.strings, ptoken.num, state.at, text, state.ln, grammar->idchars);
                    break;
                case IIDTOKEN:
                    res = check_iidtoken(ptoken.value.strings, ptoken.num, state.at, text, state.ln, grammar->idchars);
                    break;
                default:
                    res = 0;
            }
            if (res > 0) {
                tmp = (struct Token*)malloc(sizeof(struct Token));
                tmp->value = (char*)malloc(sizeof(char)*(res+1));
                strncpy(tmp->value, text + state.at, res);
                tmp->value[res] = '\0';
                // printf("got token! %d (%s)\n", res, tmp->value);
                tmp->which = ptoken.which;
                tmp->next = NULL;
                tmp->lineno = state.lineno;
                tmp->charno = state.charno;
                if (start == NULL) {
                    start = tmp;
                } else {
                    current->next = tmp;
                }
                current = tmp;
                current = advance_token(res, current, indent, &state, text, ID_t, DD_t, error);
                if (current == NULL) {
                    return NULL;
                }
                state.at += res;
                dirty = 1;
                break;
            }
        }
        if (!dirty) {
            error->text = "no valid token found";
            error->lineno = state.lineno;
            error->charno = state.charno;
            return NULL;
        }
    }
    return start;
}

void add_indent(struct TokenState* state, int ind);

struct Token* advance_token(int res, struct Token* current, int indent, struct TokenState* state, char* text, int ID_t, int DD_t, struct cTokenError* error) {
    int numlines = 0;
    int cindent;
    int last = state->at;
    int ind = 0;
    struct Token* tmp;
    int i;

    for (i=state->at; i < state->at + res; i++) {
        if (text[i] == '\n') {
            numlines += 1;
            last = i;
        }
    }
    state->lineno += numlines;
    if (numlines) {
        state->charno = state->at + res - last;
    } else {
        state->charno += res;
    }
    if (!indent || res != 1 || text[state->at] != '\n') {
        return current;
    }
    ind = t_white(state->at+1, text, state->ln);
    if (ind < 0) {
        return current;
    }
    cindent = state->indents[state->num_indents-1];
    if (ind > cindent) {
        add_indent(state, ind);
        tmp = (struct Token*)malloc(sizeof(struct Token));
        tmp->value = "";
        tmp->which = ID_t;
        tmp->next = NULL;
        tmp->lineno = state->lineno;
        tmp->charno = state->charno;
        current->next = tmp;
        current = tmp;
    } else if (ind < cindent) {
        while (ind < cindent) {
            state->num_indents -= 1;
            tmp = (struct Token*)malloc(sizeof(struct Token));
            tmp->value = "";
            tmp->which = DD_t;
            tmp->next = NULL;
            tmp->lineno = state->lineno;
            tmp->charno = state->charno;
            current->next = tmp;
            current = tmp;
            cindent = state->indents[state->num_indents - 1];
        }
        if (ind != cindent) {
            // etxt = "invalid indentation -- %d (expected %d)' % (ind, cindent)";
            error->text = "invalid indentation";
            error->lineno = state->lineno;
            error->charno = state->charno;
            // error->wanted = cindent;
            return NULL;
        }
    }
    return current;
}

void add_indent(struct TokenState* state, int ind) {
    int* indents;
    int i;
    if (state->num_indents == state->max_indents) {
        indents = (int*)malloc(sizeof(int)*state->max_indents*2);
        for (i=0;i<state->max_indents;i++) {
            indents[i] = state->indents[i];
        }
        free(state->indents);
        state->indents = indents;
        state->max_indents *= 2;
    }
    state->indents[state->num_indents] = ind;
    state->num_indents += 1;
}

