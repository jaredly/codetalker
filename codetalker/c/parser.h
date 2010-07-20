
struct Token;
struct TokenStream;
struct RuleSpecial;
struct RuleOption;

struct Token {
    unsigned int which;
    unsigned int lineno;
    unsigned int charno;
    char* value;
    struct Token* next;
};

struct TokenStream {
    struct Token* tokens;
    unsigned int num;
    unsigned int at;
    unsigned int eof;
};

struct IgnoreTokens {
    unsigned int* tokens;
    unsigned int num;
};

enum RuleItemType {
    LITERAL, RULE, TOKEN, SPECIAL
};

enum RuleSpecialType {
    STAR, PLUS, QUESTION, OR, STRAIGHT
};

struct RuleSpecial {
    enum RuleSpecialType type;
    struct RuleOption* option;
};

union ItemValue {
    unsigned int which;
    struct RuleSpecial special;
    char* text;
};

struct RuleItem {
    enum RuleItemType type;
    union ItemValue value;
};

struct RuleOption {
    struct RuleItem* items;
    unsigned int num;
};

struct Rule {
    struct RuleOption* options;
    unsigned int num;
    int dont_ignore;
    unsigned int which;
};

struct Rules {
    unsigned int num;
    struct Rule* rules;
};

enum NodeType {
    NNODE, NTOKEN
};

struct cParseNode {
    unsigned int rule;
    enum NodeType type;
    struct Token* token;
    struct cParseNode* next;
    struct cParseNode* prev;
    struct cParseNode* child;
};

struct AstAttr {
    char* name;
    unsigned int single;
    unsigned int numtypes;
    int* types;
    int pass_single;
    int start;
    int end;
    int step;
};

struct AstAttrs {
    unsigned int num;
    struct AstAttr* attrs;
};

struct Grammar {
    struct Rules rules;
    struct IgnoreTokens ignore;
    struct AstAttrs* ast_attrs;
    char** rule_names;
};

struct Error {
    int at;
    int reason;
    struct Token* token;
    char* text;
    int wanted;
};

int store_grammar(struct Grammar);
struct Grammar* load_grammar(int);
void free_grammars(void);
struct cParseNode* _get_parse_tree(int start, struct Grammar*, struct TokenStream*, struct Error*);

