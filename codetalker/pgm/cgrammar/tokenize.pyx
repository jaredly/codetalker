
from codetalker.pgm.errors import TokenError
from codetalker.pgm.token import Token
from codetalker.pgm.tokens import INDENT, DEDENT
from codetalker.pgm.cgrammar.tokens import CToken

cdef extern from "_speed_tokens.h":
    int check_token(int which, int at, char* text, int ln)
    int white(int at, char* text, int ln)

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
    indents = [0]
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
                tk = token(ctext[at:at+res], lineno, charno)
                tk.which = i
                result.append(tk)
                break
        else:
            raise TokenError('no token matches the text at (%d, %d) [%s]' % (lineno, charno, text[at:at+10]))
        advance(at, res, ctext, ln, &lineno, &charno, result, indents)
        at += res
    return result

cdef object advance(int at, int res, char* ctext, int ln, int* lineno, int* charno, object result, object indents):
    ## TODO: indents
    cdef int nlines = 0
    cdef int last = at
    cdef int ind = 0
    for i from at<=i<at+res:
        if ctext[i] == '\n':
            nlines += 1
            last = i
    lineno[0] += nlines
    if nlines:
        charno[0] = at + res - last
    else:
        charno[0] += res
    if res == 1 and ctext[at] == <char>'\n':
        ind = white(at+1, ctext, ln)
        if ind > indents[-1]:
            indents.append(ind)
            result.append(INDENT('', lineno[0], charno[0]))
        elif ind < indents[-1]:
            while ind < indents[-1]:
                indents.pop(-1)
                result.append(DEDENT('', lineno[0], charno[0]))
            if ind != indents[-1]:
                raise TokenError('invalid indentation at (%d, %d) -- %d (expected %d)' % (lineno[0], charno[0], ind, indents[-1]))

