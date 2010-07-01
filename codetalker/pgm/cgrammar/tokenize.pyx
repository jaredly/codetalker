from codetalker.pgm.cgrammar.structs cimport *
from libc.stdlib cimport *
from libc.string cimport strcpy

'''
cdef:
    struct TextStream:
        char* text
        unsigned int at
'''

_indent = []

def log(*a):
    pass
    # strs = []
    # for e in a:strs.append(str(e))
    # print '  |'*len(_indent), ' '.join(strs)

## SPECIAL TOKENS: EOF=0, INDENT=1, DEDENT=2

cdef Token* tokenize(char* text, unsigned int length, unsigned int* real_tokens,
        Rules tokens, bint check_indent, object error):
    cdef:
        Token* start = NULL
        Token* current = NULL
        Token* tmp = NULL
        char* result = NULL
        unsigned int lineno = 1
        unsigned int charno = 1
        unsigned int at = 0
    indent = [0]
    log('tokenizing')
    _indent.append(0)

    while at < length:
        for i from 1<=i<real_tokens[0]:
            result = token_text(tokens.rules[real_tokens[i]], text, length, at, &tokens, error)
            if result == NULL:
                log('didnt work')
                continue
            else:
                thestuff = result
            result = thestuff
            if result != NULL:
                tmp = <Token*>malloc(sizeof(Token))
                tmp.which = real_tokens[i]
                tmp.lineno = lineno
                tmp.charno = charno
                tmp.value = <char*>malloc(sizeof(char) * len(thestuff) + 1)
                strcpy(tmp.value, thestuff)
                tmp.next = NULL
                if start == NULL:
                    start = tmp
                    current = start
                else:
                    current.next = tmp
                    current = tmp
                small = str(text[at:at+len(result)])
                if small == '\n':
                    lineno += 1
                    charno = 1
                    if check_indent:
                        current = handle_indent(text, at, current, real_tokens[0], lineno, charno, indent, error)
                        if current == NULL:
                            _indent.pop(0)
                            return NULL
                elif '\n' in small:
                    lineno += small.count('\n')
                    charno += len(small[small.rfind('\n'):])
                else:
                    charno += len(small)
                at += len(small)
                break
        else:
            error[0] = at
            error[1] = 'invalid token'
            _indent.pop(0)
            return NULL
    _indent.pop(0)
    return start

cdef Token* handle_indent(char* text, unsigned int at, Token* current, unsigned int num_tokens,
        int lineno, int charno, object indent, object error):
    cdef Token* tmp = NULL
    white = get_white(text, at + len(current.value))
    if white != indent[-1]:
        if white > indent[-1]:
            tmp = <Token*>malloc(sizeof(Token))
            tmp.which = num_tokens - 1
            tmp.lineno = lineno
            tmp.charno = charno
            tmp.value = ''
            current.next = tmp
            current = tmp
            indent.append(white)
        else:
            while white < indent[-1]:
                tmp = <Token*>malloc(sizeof(Token))
                tmp.which = num_tokens
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
    return current

cdef unsigned int get_white(char* text, unsigned int at):
    cdef unsigned int white = 0
    while text[at] == ' ':
        white += 1
        at += 1
    return white

cdef char* token_text(Rule token, char* text, unsigned int length, unsigned int at, Rules* tokens, object error):
    cdef char* res
    for i from 0<=i<token.num:
        _indent.append(0)
        res = token_children(token.options[i], text, length, at, tokens, error)
        _indent.pop(0)
        if res != NULL:
            return res
    return NULL

cdef char* test_literal(RuleItem item, char* text, unsigned int at):
    what = item.value.text
    log('literal >>', what, '<<')
    if what == text[at:at+len(what)]:
        log('success')
        return what
    log('fail:', text[at:at+len(what)])

    return NULL

cdef char* test_special(RuleSpecial special, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    res = ''
    cdef char* tmp
    log('special')
    if special.type == STAR:
        log('star')
        while 1:
            tmp = token_children(special.option[0], text, length, at, tokens, error)
            if tmp == NULL:
                break
            res += tmp
            at += len(tmp)
        return res
    elif special.type == PLUS:
        log('plus')
        tmp = token_children(special.option[0], text, length, at, tokens, error)
        if tmp == NULL:
            return NULL
        res += tmp
        at += len(tmp)
        while 1:
            tmp = token_children(special.option[0], text, length, at, tokens, error)
            if tmp == NULL:
                break
            res += tmp
            at += len(tmp)
        return res
    elif special.type == OR:
        log('or')
        for org from 0<=org<special.option.num:
            tmp = token_children(special.option.items[org].value.special.option[0], text, length, at, tokens, error)
            if tmp != NULL:
                res = tmp
                return res
        else:
            return NULL
    elif special.type == QUESTION:

        tmp = token_children(special.option[0], text, length, at, tokens, error)
        if tmp != NULL:
            res = tmp
            return res
        return ''
    elif special.type ==STRAIGHT:
        print 'failz'
        return NULL
    return NULL

cdef char* token_children(RuleOption option, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    res = ''
    cdef char* tmp
    _indent.append(0)
    for i from 0<=i<option.num:
        if option.items[i].type == RULE:
            if at >= length:
                log('RAN OUT')
                _indent.pop(0)
                return NULL
            log('RULE')
            tmp = token_text(tokens.rules[option.items[i].value.which], text, length, at, tokens, error)
            if tmp != NULL:
                _indent.pop(0)
                at += len(tmp)
                res += tmp
                continue
            _indent.pop(0)
            return NULL
        elif option.items[i].type == LITERAL:
            if at >= length:
                log('RAN OUT')
                _indent.pop(0)
                return NULL
            tmp = test_literal(option.items[i], text, at)
            if tmp == NULL:
                _indent.pop(0)
                return NULL
            res += tmp
            at += len(tmp)
        elif option.items[i].type == SPECIAL:
            tmp = test_special(option.items[i].value.special, text, length, at, tokens, error)
            if tmp == NULL:
                _indent.pop(0)
                return NULL
            res += tmp
            at += len(tmp)
        else:
            error[1] = 'unknown rule type'
            _indent.pop(0)
            return NULL
    _indent.pop(0)
    return res

