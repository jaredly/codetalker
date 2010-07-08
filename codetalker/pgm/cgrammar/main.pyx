from libc.stdlib cimport malloc, free
from codetalker.pgm.cgrammar.structs cimport *
from codetalker.pgm.cgrammar cimport convert, parser, kill
from codetalker.pgm.cgrammar.convert import pyToken, pyParseNode

from codetalker.pgm.errors import ParseError

def process(start, tokens, rules, ignore, tokens_list):
    tree = c_process(start, convert.tokens(tokens), convert.rules(rules), convert.ignore(ignore), tokens, rules, tokens_list)
    return tree

cdef object c_process(unsigned int start, TokenStream tokens, Rules rules, IgnoreTokens ignore, object py_tokens, object py_rules, object tokens_list):
    cdef State state
    state.tokens = tokens
    state.rules = rules
    state.ignore = ignore
    state.tokens.eof = len(tokens_list) - 1
    error = [0, None]
    cdef ParseNode* tree = parser.parse_rule(start, &state, error)
    if tree == NULL and error[1] is not None:
        if error[1][0] == 'rule':
            raise ParseError('failed to parse rule %s (at token %r)' % (py_rules[error[1][1]], py_tokens[error[0]]))
        elif error[1][0] == 'token':
            raise ParseError('failed to parse rule %s (at token %r) -- looking for %s' % (py_rules[error[1][1]], py_tokens[error[0]], tokens_list[error[1][3]]))
        elif error[1][0] == 'literal':
            raise ParseError('failed to parse rule %s (at token %r) -- looking for \'%s\'' % (py_rules[error[1][1]], py_tokens[error[0]], error[1][4].encode('string_escape')))
        elif error[1][0] == 'ran out':
            raise ParseError('insufficient tokens while parsing rule %s' % (py_rules[error[1][1]].builder), error)
        raise ParseError('parse failed', error)
    elif tree == NULL:
        return None
    back = convert.nodes_back(tree)
    free(tokens.tokens)
    kill.rules(rules)
    kill.nodes(tree)
    return back

