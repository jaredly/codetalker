
from codetalker.pgm.errors import TokenError
from codetalker.pgm.token import Token
from codetalker.pgm.cgrammar.tokens import CToken

cdef extern from "_speed_tokens.h":
    int check_token(int which, int at, char* text, int ln)

def tokenize(tokens, text, indent=False):
    # print 'tokenizing'
    cdef int at = 0
    cdef int ln = len(text)
    cdef char* ctext = text
    cdef int lineno = 1
    cdef int charno = 1
    cdef int res
    currtext = text
    result = []
    # print 'a'
    while at < ln:
        # print 'at', at
        res = 0
        currtext = ''
        for i, token in enumerate(tokens):
            # print 'checking', i, token
            if issubclass(token, CToken):
                res = check_token(token._check, at, ctext, ln)
            else:
                if not currtext:
                    currtext = text[at:]
                res = token.check(currtext)
            # print 'result from', i, token, res
            if res != 0:
                result.append(token(ctext[at:at+res], lineno, charno))
                break
        else:
            raise TokenError('no token matches the text at (%d, %d) [%s]' % (lineno, charno, text[at:at+10]))
        advance(at, res, ctext, &lineno, &charno, result)
        at += res
    return result

cdef advance(int at, int res, char* ctext, int* lineno, int* charno, object result):
    ## if res == 1 && ctext[at] == <char>'\n':
    ## TODO: indents
    cdef int nlines = 0
    cdef int last = at
    for i from at<=i<at+res:
        if ctext[i] == '\n':
            nlines += 1
            last = i
    lineno[0] += nlines
    if nlines:
        charno[0] = at + res - last
    else:
        charno[0] += res

