from cgrammar.structs cimport *
from stdlib cimport *

'''
cdef:
    struct TextStream:
        char* text
        unsigned int at
'''

## SPECIAL TOKENS: EOF=0, INDENT=1, DEDENT=2

cdef Token* tokenize(char* text, unsigned int length, unsigned int* real_tokens,
        Rules tokens, bint check_indent, object error):
    cdef:
        Token* start = NULL
        Token* current = NULL
        Token* tmp = NULL
        char* res
        unsigned int lineno = 0
        unsigned int charno = 0
        unsigned int at = 0
    indent = [0]

    while at < length:
        for i in 1<=i<real_tokens[0]:
            res = token_text(tokens.rules[real_tokens[i]], text, length, at, &tokens, error)
            if res != NULL:
                tmp = <Token*>malloc(sizeof(Token))
                tmp.which = real_tokens[i]
                tmp.lineno = lineno
                tmp.charno = charno
                tmp.value = res
                if start == NULL:
                    start = tmp
                    current = start
                else:
                    current.next = tmp
                    current = tmp
                small = text[at:at+len(current.value)]
                if small == '\n':
                    lineno += 1
                    charno = 0
                    white = get_white(text, at + len(current.value))
                    if check_indent and white != indent[-1]:
                        if white > indent[-1]:
                            tmp = <Token*>malloc(sizeof(Token))
                            tmp.which = 1
                            tmp.lineno = lineno
                            tmp.charno = charno
                            tmp.value = ''
                            current.next = tmp
                            current = tmp
                            indent.append(white)
                        else:
                            while white < indent[-1]:
                                tmp = <Token*>malloc(sizeof(Token))
                                tmp.which = 2
                                tmp.lineno = lineno
                                tmp.charno = charno
                                tmp.value = ''
                                current.next = tmp
                                current = tmp
                                indent.pop(-1)
                            if white != indent[-1]:
                                error[0] = at
                                error[1] = 'invalid indent (%d, %d)' % (lineno, charno)
                                return NULL
                elif '\n' in small:
                    lineno += small.count('\n')
                    charno += len(small[small.rfind('\n'):])
                else:
                    charno += len(small)

                break
        else:
            error[0] = at
            error[1] = 'invalid token'
            return NULL
    return start

cdef unsigned int get_white(char* text, unsigned int at):
    cdef unsigned int white = 0
    while text[at] == ' ':
        white += 1
        at += 1
    return white

cdef char* token_text(Rule token, char* text, unsigned int length, unsigned int at, Rules* tokens, object error):
    cdef char* res
    for i from 0<=i<token.num:
        res = token_children(token.options[i], text, length, at, tokens, error)
        if res != NULL:
            return res
    return NULL

cdef char* token_children(RuleOption option, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    res = ''
    cdef char* tmp
    for i from 0<=i<option.num:
        if at >= length:
            return NULL
        if option.items[i].type == RULE:
            tmp = token_text(tokens.rules[option.items[i].value.which], text, length, at, tokens, error)
            if tmp != NULL:
                at += len(tmp)
                res += tmp
            return NULL
        elif option.items[i].type == LITERAL:
            tmp = option.items[i].value.text
            if tmp == text[at:at + len(tmp)]:
                res += tmp
                at += len(tmp)
            return NULL
        elif option.items[i].type == SPECIAL:
            if option.items[i].value.special.type == STAR:
                while 1:
                    tmp = token_children(option.items[i].value.special.option[0], text, length, at, tokens, error)
                    if tmp == NULL:
                        break
                    res += tmp
                    at += len(tmp)
            elif option.items[i].value.special.type == PLUS:
                tmp = token_children(option.items[i].value.special.option[0], text, length, at, tokens, error)
                if tmp == NULL:
                    return NULL
                res += tmp
                at += len(tmp)
                while 1:
                    tmp = token_children(option.items[i].value.special.option[0], text, length, at, tokens, error)
                    if tmp == NULL:
                        break
                    res += tmp
                    at += len(tmp)
            elif option.items[i].value.special.type == OR:
                for org from 0<=org<option.items[i].value.special.option.num:
                    tmp = token_children(option.items[i].value.special.option.items[org].value.special.option[0], text, length, at, tokens, error)
                    if tmp != NULL:
                        res += tmp
                        at += len(tmp)
                        break
                else:
                    return NULL
            elif option.items[i].value.special.type == QUESTION:
                tmp = token_children(option.items[i].value.special.option[0], text, length, at, tokens, error)
                if tmp != NULL:
                    res += tmp
                    at += len(tmp)
            elif option.items[i].value.special.type ==STRAIGHT:
                print 'this shouldnt happen...'
                return NULL
        else:
            error[1] = 'unknown rule type'
            return NULL
    return res

