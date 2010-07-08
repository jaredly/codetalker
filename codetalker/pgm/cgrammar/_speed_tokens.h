
typedef enum { tSTRING, tID, tWHITE, tNEWLINE, tNUMBER } ttype;
int check_token(ttype which, int at, char* text, int ln);
int white(int at, char* text, int ln);

