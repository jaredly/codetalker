
from codetalker.pgm.token import Token

cdef extern from "_speed_tokens.h":
    enum ttype:
        tSTRING
        tID
        tWHITE
        tNEWLINE
        tNUMBER

cdef no_check(int at, char* text, int ln):
    return 0

class CToken(Token):
    _check = -1

class STRING(CToken):
    _check = tSTRING

class ID(CToken):
    _check = tID

class NEWLINE(CToken):
    _check = tNEWLINE

class WHITE(CToken):
    _check = tWHITE

class NUMBER(CToken):
    _check = tNUMBER

