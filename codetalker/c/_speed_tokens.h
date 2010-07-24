
typedef enum {
    tTSTRING,  // triple string
    tSSTRING,  // single-quoted string
    tSTRING,   // normal (double-quoted) string
    tID,       // [a-zA-Z_][a-zA-Z_0-9]*
    tNUMBER,   // ([1-9]+(\.\d*))|(\.\d+)
    tINT,      // [1-9][0-9]*
    tHEX,      // 0xdeadb33f
    tCCOMMENT, // // blah\n
    tCMCOMMENT,// /** blah **/
    tPYCOMMENT,// # blah\n
    tWHITE,    // space | \t
    tNEWLINE,  // \n
    tANY       // any char
} ttype;

int check_ctoken(ttype tid, int at, char* text, int ln, char* idchars);
int check_chartoken(char* chars, int num, int at, char* text, int ln);
int check_stringtoken(char** strings, int num, int at, char* text, int ln);
int check_idtoken(char** strings, int num, int at, char* text, int ln, char* idchars);
int check_iidtoken(char** strings, int num, int at, char* text, int ln, char* idchars);

int t_white(int at, char* text, int ln);

