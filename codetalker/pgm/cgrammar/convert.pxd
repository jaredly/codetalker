from structs cimport *

cdef Rules convert_rules(object rules)
cdef IgnoreTokens convert_ignore(object ignore, object tokens)
cdef object convert_tokens_back(Token* first)
cdef object convert_nodes_back(ParseNode* root)

