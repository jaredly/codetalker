from libc.stdlib cimport *
from codetalker.pgm.cgrammar.structs cimport *
from codetalker.pgm.cgrammar.convert cimport convert_rules, convert_ignore, convert_tokens_back
from codetalker.pgm.cgrammar.tokenize cimport tokenize
from codetalker.pgm.cgrammar.parser cimport parse_rule
from codetalker.pgm.cgrammar.kill cimport kill_rules, kill_ignore, kill_tokens

def process(start, text, rules, tokens, real_tokens, ignore, indent=False):
    cdef Rules crules = convert_rules(rules)
    cdef Rules ctokens = convert_rules(tokens)
    cdef IgnoreTokens cignore = convert_ignore(ignore, tokens)
    cdef unsigned int* creal_tokens = <unsigned int*>malloc(sizeof(unsigned int)*(len(real_tokens)+1))

    creal_tokens[0] = len(real_tokens)+1
    for tk from 0<=tk<creal_tokens[0]-1:
        creal_tokens[tk+1] = real_tokens[tk]

    error = [0, None]
    cdef Token* first_token = tokenize(text, len(text), creal_tokens, ctokens, indent, error)
    if first_token == NULL:
        raise Exception('tokenize failed', error, text[error[0]:error[0]+100])
    cdef unsigned int num_tokens = 1
    cdef Token* tmp_token = first_token
    while tmp_token.next != NULL:
        num_tokens += 1
        tmp_token = tmp_token.next
    cdef TokenStream tokenstream
    tokenstream.tokens = <Token*>malloc(sizeof(Token)*num_tokens)
    tmp_token = first_token
    for i from 0<=i<num_tokens:
        tokenstream.tokens[i] = tmp_token[0]
        tmp_token = tmp_token.next
    error = [0, None]
    cdef State state
    state.rules = crules
    state.tokens = tokenstream
    state.ignore = cignore
    cdef ParseNode* root = parse_rule(start, &state, error)

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
    kill_ignore(cignore)
    kill_rules(crules)
    kill_rules(ctokens)
    if tokenstream == NULL:
        raise Exception('tokenize failed', error, text[error[0]:error[0]+100])
    py_tokens = convert_tokens_back(tokenstream)
    kill_tokens(tokenstream)
    return py_tokens

cdef hello():
    print 'hi'

def yeah():
    print 'umm'
