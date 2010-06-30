from structs cimport *
cdef void kill_ignore(IgnoreTokens ignore)
cdef void kill_rules(Rules rules)
cdef void kill_tokens(Token* start)
cdef void kill_nodes(ParseNode* node)

