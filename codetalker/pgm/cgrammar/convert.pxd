from structs cimport *

cdef TokenStream tokens(object tokens)
cdef Rules rules(object rules)
cdef IgnoreTokens ignore(object ignore)
cdef object tokens_back(Token* first)
cdef object nodes_back(ParseNode* root)

