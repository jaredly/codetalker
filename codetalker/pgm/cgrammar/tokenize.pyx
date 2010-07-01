from codetalker.pgm.cgrammar.structs cimport *
from libc.stdlib cimport *
from libc.string cimport strncpy

'''
cdef:
    struct TextStream:
        char* text
        unsigned int at
'''

_indent = []

def log(*a):pass
def log_(*a):
    strs = []
    for e in a:strs.append(str(e))
    print '  |'*len(_indent), ' '.join(strs)


## SPECIAL TOKENS: EOF=0, INDENT=1, DEDENT=2

cdef Token* tokenize(char* text, unsigned int length, unsigned int* real_tokens,
        Rules tokens, bint check_indent, object error):
    cdef:
        Token* start = NULL
        Token* current = NULL
        Token* tmp = NULL
        char* txt = NULL
        int result = -1
        unsigned int lineno = 1
        unsigned int charno = 1
        unsigned int at = 0
    indent = [0]
    log('tokenizing')
    _indent.append(0)

    while at < length:
        for i from 1<=i<real_tokens[0]:
            log('looking for token at', at)
            result = token_text(tokens.rules[real_tokens[i]], text, length, at, &tokens, error)
            if result == -1:
                log('didnt work')
                continue
            else:
                log('got a token!', result, [text[at:at+result]])
                tmp = <Token*>malloc(sizeof(Token))
                tmp.which = real_tokens[i]
                tmp.lineno = lineno
                tmp.charno = charno
                tmp.value = <char*>malloc(sizeof(char) * result + 1)
                strncpy(tmp.value, text+at, result)
                tmp.value[result] = '\0'
                log('and the real value:', [tmp.value], text+at, result)
                tmp.next = NULL
                if start == NULL:
                    start = tmp
                    current = start
                else:
                    current.next = tmp
                    current = tmp
                small = str(tmp.value)
                if small == '\n':
                    log('CHECKING INDENT')
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
                log('INC AT:', [at, small], at+len(small))
                at += result
                break
        else:
            if at > error[0]:
                error[0] = at
                error[1] = 'no token matches'
            _indent.pop(0)
            return NULL
    _indent.pop(0)
    return start

cdef Token* handle_indent(char* text, unsigned int at, Token* current, unsigned int num_tokens,
        int lineno, int charno, object indent, object error):
    cdef Token* tmp = NULL
    white = get_white(text, at + len(current.value))
    log('WHITE:', white)
    log('[last indent: %d]' % indent[-1])
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
    while text[at] == 32:
        white += 1
        at += 1
    return white

cdef int token_text(Rule token, char* text, unsigned int length, unsigned int at, Rules* tokens, object error):
    cdef int res
    for i from 0<=i<token.num:
        _indent.append(0)
        res = token_children(token.options[i], text, length, at, tokens, error)
        _indent.pop(0)
        if res != -1:
            return res
    return -1

cdef int test_literal(RuleItem item, char* text, unsigned int at):
    what = item.value.text
    # log('literal >>', what, '<<', at)
    if str(what) == str(text[at:at+len(what)]):
        log('success', what, '::', at)
        return len(what)
    log('fail:', [what, text[at:at+len(what)]], at)

    return -1

cdef int test_special(RuleSpecial special, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    cdef int res = 0
    cdef int tmp = 0
    log('special')
    if special.type == STAR:
        log('star')
        while 1:
            tmp = token_children(special.option[0], text, length, at, tokens, error)
            if tmp == -1:
                break
            res += tmp
            # log('INC AT (special*)', (at, tmp), at + len(tmp))
            at += tmp
        log('from special', res)
        return res
    elif special.type == PLUS:
        log('plus')
        tmp = token_children(special.option[0], text, length, at, tokens, error)
        if tmp == -1:
            return -1
        res += tmp
        # log('INC AT (special+)', (at, tmp), at + len(tmp))
        at += tmp
        while 1:
            tmp = token_children(special.option[0], text, length, at, tokens, error)
            if tmp == -1:
                break
            res += tmp
            # log('INC AT (special++)', (at, tmp), at + len(tmp))
            at += tmp
        log('from special', res)
        return res
    elif special.type == OR:
        log('or')
        for org from 0<=org<special.option.num:
            tmp = token_children(special.option.items[org].value.special.option[0], text, length, at, tokens, error)
            if tmp != -1:
                res = tmp
                log('from special', res)
                return res
        else:
            return -1
    elif special.type == QUESTION:
        tmp = token_children(special.option[0], text, length, at, tokens, error)
        if tmp != -1:
            res = tmp
            log('from special', res)
            return res
        return 0
    elif special.type == STRAIGHT:
        print 'failz'
        return -1
    return -1

cdef int token_children(RuleOption option, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    cdef int res = 0
    cdef int tmp = 0
    _indent.append(0)
    for i from 0<=i<option.num:
        if option.items[i].type == RULE:
            if at >= length:
                log('RAN OUT')
                _indent.pop(0)
                error[0] = at
                error[1] = 'ran out of tokens'
                return -1
            log('RULE')
            tmp = token_text(tokens.rules[option.items[i].value.which], text, length, at, tokens, error)
            if tmp != -1:
                _indent.pop(0)
                # log('IN#C AT (RULE)', (at, tmp), at + len(tmp))
                at += tmp
                res += tmp
                continue
            _indent.pop(0)
            if at > error[0]:
                error[0] = at
                error[1] = 'failed rule', option.items[i].value.which
            return -1
        elif option.items[i].type == LITERAL:
            if at >= length:
                log('RAN OUT')
                error[0] = at
                error[1] = 'ran out of tokens'
                _indent.pop(0)
                return -1
            tmp = test_literal(option.items[i], text, at)
            if tmp == -1:
                _indent.pop(0)
                if at > error[0]:
                    error[0] = at
                    error[1] = 'Invalid tokenzing; got %s (at %d), expected %s' %\
                            (text[at:at+len(option.items[i].value.text)], at, option.items[i].value.text)
                return -1
            res += tmp
            # log('INC AT (literal)', (at, tmp), at + len(tmp))
            at += tmp
        elif option.items[i].type == SPECIAL:
            tmp = test_special(option.items[i].value.special, text, length, at, tokens, error)
            if tmp == -1:
                _indent.pop(0)
                return -1
            res += tmp
            # log('INC AT (special)', (at, tmp), at + len(tmp), option.items[i].value.special.type)
            at += tmp
        else:
            error[1] = 'unknown rule type'
            _indent.pop(0)
            return -1
    _indent.pop(0)
    return res

