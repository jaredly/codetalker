from libc.stdlib cimport malloc, free
from codetalker.pgm.cgrammar.structs cimport *
from codetalker.pgm.cgrammar cimport convert, parser, kill

from codetaler.pgm.errors import ParseError

def process(start, tokens, rules, ignore):
    tree = c_process(start, convert.tokens(tokens), convert.rules(rules), convert.ignore(ignore))
    return tree

cdef object c_process(unsigned int start, TokenStream tokens, Rules rules, IgnoreTokens ignore):
    cdef State state
    state.tokens = tokens
    state.rules = rules
    state.ignore = ignore
    error = [0, None]
    cdef ParseNode* tree = parser.parse_rule(start, &state, error)
    if tree == NULL:
        raise ParseError('parse failed', error)
    back = convert.nodes_back(tree)
    free(tokens.tokens)
    kill.rules(rules)
    kill.nodes(tree)
    return back

