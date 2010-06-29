from codetalker.pgm.cgrammar.structs cimport *
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
        char* result = NULL
        unsigned int lineno = 0
        unsigned int charno = 0
        unsigned int at = 0
    indent = [0]

    while at < length:
        for i from 1<=i<real_tokens[0]:
            result = token_text(tokens.rules[real_tokens[i]], text, length, at, &tokens, error)
            if result == NULL:
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
                small = text[at:at+len(result)]
                if small == '\n':
                    lineno += 1
                    charno = 0
                    if check_indent:
                        current = handle_indent(text, at, current, lineno, charno, indent, error)
                        if current == NULL:
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
            return NULL
    return start

cdef Token* handle_indent(char* text, unsigned int at, Token* current, int lineno, int charno, object indent, object error):
    cdef Token* tmp = NULL
    white = get_white(text, at + len(current.value))
    if white != indent[-1]:
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

cdef unsigned int get_white(char* text, unsigned int at):
    cdef unsigned int white = 0
    while text[at] == ' ':
        white += 1
        at += 1
    return white

cdef char* token_text(Rule token, char* text, unsigned int length, unsigned int at, Rules* tokens, object error):
    cdef char* res
    for i from 0<=i<token.num:
        print 'TESTING A CHILD'
        res = token_children(token.options[i], text, length, at, tokens, error)
        if res != NULL:
            print 'GOT CHILD', res
            print 'GOT CHILD', res
            return res
    return NULL

cdef char* test_literal(RuleItem item, char* text, unsigned int at):
    what = item.value.text
    print ' LITERAL', [what, text[at:at+len(what)]]
    if what == text[at:at+len(what)]:
        return what
    print ' bad literal'
    return NULL

cdef char* test_special(RuleSpecial special, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    print ' special...'
    cdef char* tmp
    if special.type == STAR:
        print 'start'
        while 1:
            tmp = token_children(special.option[0], text, length, at, tokens, error)
            if tmp == NULL:
                break
            res += tmp
            at += len(tmp)
        return res
    elif special.type == PLUS:
        print 'plus'
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
        print 'or'
        for org from 0<=org<special.option.num:
            tmp = token_children(special.option.items[org].value.special.option[0], text, length, at, tokens, error)
            if tmp != NULL:
                print 'good or', org, tmp
                res = tmp
                return res
        else:
            return NULL
    elif special.type == QUESTION:
        print '?'
        tmp = token_children(special.option[0], text, length, at, tokens, error)
        if tmp != NULL:
            res = tmp
            return res
    elif special.type ==STRAIGHT:
        print '--'
        print 'this shouldnt happen...'
        return NULL
    return NULL

cdef char* token_children(RuleOption option, char* text, unsigned int length, unsigned int at,
        Rules* tokens, object error):
    res = ''
    cdef char* tmp
    print 'getting an option'
    for i from 0<=i<option.num:
        print ' at',i,at
        if at >= length:
            print ' ran out'
            return NULL
        if option.items[i].type == RULE:
            tmp = token_text(tokens.rules[option.items[i].value.which], text, length, at, tokens, error)
            if tmp != NULL:
                at += len(tmp)
                res += tmp
                continue
            return NULL
        elif option.items[i].type == LITERAL:
            tmp = test_literal(option.items[i], text, at)
            if tmp == NULL:
                return NULL
            res += tmp
            at += len(tmp)
        elif option.items[i].type == SPECIAL:
            tmp = test_special(option.items[i].value.special, text, length, at, tokens, error)
            if tmp == NULL:
                return NULL
            res += tmp
            at += len(tmp)
        else:
            error[1] = 'unknown rule type'
            return NULL
    return res

