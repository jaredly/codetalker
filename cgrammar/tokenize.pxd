from structs cimport *

cdef Token* tokenize(char* text, unsigned int length, unsigned int* real_tokens,
        Rules tokens, bint do_indent, object error)

