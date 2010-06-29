from libc.stdlib cimport *
from codetalker.pgm.cgrammar.structs cimport *
from codetalker.pgm.cgrammar.convert cimport convert_rules, convert_ignore, convert_tokens_back
from codetalker.pgm.cgrammar.tokenize cimport tokenize

def process(start, text, rules, tokens, real_tokens, ignore, indent=False):
    cdef Rules crules = convert_rules(rules)
    cdef Rules ctokens = convert_rules(tokens)
    cdef IgnoreTokens cignore = convert_ignore(ignore, tokens)
    cdef unsigned int* creal_tokens = <unsigned int*>malloc(sizeof(unsigned int)*(len(real_tokens)+1))

    creal_tokens[0] = len(real_tokens)+1
    for tk from 0<=tk<creal_tokens[0]-1:
        creal_tokens[tk+1] = real_tokens[tk]

    error = [0, None]
    cdef Token* tokenstream = tokenize(text, len(text), creal_tokens, ctokens, indent, error)
    if tokenstream == NULL:
        print 'tokenize failed'
        raise Exception('tokenize failed', error, text[error[0]:error[0]+100])
    return convert_tokens_back(tokenstream)

def just_tokens(text, rules, tokens, real_tokens, ignore, indent=False):
    cdef Rules crules = convert_rules(rules)
    cdef Rules ctokens = convert_rules(tokens)
    cdef IgnoreTokens cignore = convert_ignore(ignore, tokens)
    cdef unsigned int* creal_tokens = <unsigned int*>malloc(sizeof(unsigned int)*(len(real_tokens)+1))
    creal_tokens[0] = len(real_tokens)+1
    for tk from 0<=tk<creal_tokens[0]-1:
        creal_tokens[tk+1] = real_tokens[tk]

    error = [0, None]
    cdef Token* tokenstream = tokenize(text, len(text), creal_tokens, ctokens, indent, error)
    if tokenstream == NULL:
        print 'tokenize failed:', error, text[error[0]:error[0]+100]
        return []
    return convert_tokens_back(tokenstream)

cdef hello():
    print 'hi'

def yeah():
    print 'umm'
