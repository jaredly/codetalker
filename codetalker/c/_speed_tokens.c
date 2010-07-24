/**
 * Part of Codetalker
 * author: Jared Forsyth <jared@jaredforsyth.com>
 */

#include "stdlib.h"
#include "string.h"
#include "_speed_tokens.h"

/**
 * Backend code for tokenizing strings
 */
int t_tstring(int at, char* text, int ln) {
    int i = at;
    if (ln < at + 6 || (text[i] != '\'' && text[i] != '"')) {
        return 0;
    }
    char which = text[i];
    if (text[i+1] != which || text[i+2] != which) {
        return 0;
    }
    i += 3;
    for (;i<ln-2;i++) {
        if (text[i] == '\\')
            i++;
        else if (text[i] == which && text[i+1] == which && text[i+2] == which) {
            return i + 3 - at;
        }
    }
    return 0;
}

int t_sstring(int at, char* text, int ln) {
    int i = at;
    if (text[i] != '\'') {
        return 0;
    }
    i++;
    for (;i<ln;i++) {
        if (text[i] == '\\')
            i++;
        else if (text[i] == '\'')
            return i + 1 - at;
        else if (text[i] == '\n')
            return 0;
    }
    return 0;
}

int t_string(int at, char* text, int ln) {
    int i = at;
    if (text[i] != '"') {
        return 0;
    }
    i++;
    for (;i<ln;i++) {
        if (text[i] == '\\')
            i++;
        else if (text[i] == '"')
            return i + 1 - at;
        else if (text[i] == '\n')
            return 0;
    }
    return 0;
}

#define alpha_(what) ((what >= 'a' && what <= 'z') || (what >= 'A' && what <= 'Z') || what == '_')

#define num(what) (what >= '0' && what <= '9')

#define hex(what) ((what >= '0' && what <= '9')||(what >= 'a' && what <= 'f')||(what >= 'A' && what <= 'F'))

#define alphanum(what) (alpha_(what) || num(what))

int t_id(int at, char* text, int ln, char* idchars) {
    int i = at;
    if (!alpha_(text[i]) && strchr(idchars, text[i]) == NULL) {
        return 0;
    }
    i += 1;
    while (i < ln && (alpha_(text[i]) || num(text[i]) || strchr(idchars, text[i]) != NULL)) {
        i++;
    }
    return i - at;
}

int t_number(int at, char* text, int ln) {
    int i = at;
    if (text[i] == '-') i++;
    if (i >= ln) return 0;
    if (text[i] == '.') {
        i++;
        if (i >= ln || !num(text[i])) {
            return 0;
        }
        while (i < ln && num(text[i])) {
            i++;
        }
    } else if (num(text[i])) {
        while (i < ln && num(text[i])) {
            i++;
        }
        if (i < ln && text[i] == '.') {
            i++;
        }
        while (i < ln && num(text[i])) {
            i++;
        }
    } else {
        return 0;
    }
    int pre = i;
    if (i < ln-2 && (text[i] == 'e' || text[i] == 'E')) {
        i++;
        if (text[i] == '+' || text[i] == '-') {
            i++;
        }
        if (i >= ln || !num(text[i])) {
            return pre - at;
        }
        i++;
        while (i < ln && num(text[i])) {
            i++;
        }
    }
    return i - at;
}

int t_int(int at, char* text, int ln) {
    int i = at;
    if (text[i] >= '1' && text[i] <= '9') {
        i += 1;
        while (num(text[i])) {
            i += 1;
        }
    }
    return i - at;
}

int t_hex(int at, char* text, int ln) {
    int i = at;
    if (text[i] == '0' && i < ln - 2 && (text[i+1] == 'x' || text[i+1] == 'X') && hex(text[i+2])) {
        i += 3;
        while (i < ln && hex(text[i])) {
            i++;
        }
        return i - at;
    } else {
        return 0;
    }
}

int t_ccomment(int at, char* text, int ln) {
    int i = at;
    if (text[i] != '/' || ln-1 == at) {
        return 0;
    }
    if (text[i+1] == '/') { // this kind
        i += 2;
        for (;i<ln;i++) {
            if (text[i] == '\\') i++;
            else if (text[i] == '\n') {
                return i + 1 - at;
            }
        }
        return i - at;
    }
    return 0;
}

int t_cmcomment(int at, char* text, int ln) {
    int i = at;
    if (text[i] != '/' || ln-1 == at) {
        return 0;
    }
    if (text[i+1] == '*') { /* this kind */
        i += 2;
        for (;i<ln-1;i++) {
            if (text[i] == '\\') i++;
            else if (text[i] == '*' && text[i+1] == '/') {
                return i + 2 - at;
            }
        }
    }
    return 0;
}

int t_pycomment(int at, char* text, int ln) {
    int i = at;
    if (text[i] != '#') {
        return 0;
    }
    i += 1;
    for (;i<ln;i++) {
        if (text[i] == '\\') i++;
        else if (text[i] == '\n') {
            return i + 1 - at;
        }
    }
    return i - at;
}

int t_white(int at, char* text, int ln) {
    int i = at;
    while (i < ln && (text[i] == ' ' || text[i] == '\t')) {
        i++;
    }
    return i - at;
}

int check_ctoken(ttype tid, int at, char* text, int ln, char* idchars) {
    switch (tid) {
        case tTSTRING:
            return t_tstring(at, text, ln);
        case tSSTRING:
            return t_sstring(at, text, ln);
        case tSTRING:
            return t_string(at, text, ln);
        case tID:
            return t_id(at, text, ln, idchars);
        case tNUMBER:
            return t_number(at, text, ln);
        case tINT:
            return t_int(at, text, ln);
        case tHEX:
            return t_hex(at, text, ln);
        case tCCOMMENT:
            return t_ccomment(at, text, ln);
        case tCMCOMMENT:
            return t_cmcomment(at, text, ln);
        case tPYCOMMENT:
            return t_pycomment(at, text, ln);
        case tWHITE:
            return t_white(at, text, ln);
        case tNEWLINE:
            return text[at] == '\n';
        case tANY:
            return 1;
        default:
            return 0;
    }
}

int check_chartoken(char* chars, int num, int at, char* text, int ln) {
    int i;
    for (i=0;i<num;i++) {
        if (text[at] == chars[i]) return 1;
    }
    return 0;
}

int check_stringtoken(char** strings, int num, int at, char* text, int ln) {
    int i, l;
    for (i=0;i<num;i++) {
        l = strlen(strings[i]);
        if (strncmp(text+at, strings[i], l) == 0) {
            return l;
        }
    }
    return 0;
}

int check_idtoken(char** strings, int num, int at, char* text, int ln, char* idchars) {
    int i, l;
    for (i=0;i<num;i++) {
        l = strlen(strings[i]);
        if (strncmp(text+at, strings[i], l) == 0 && (at+l==ln || (!alphanum(text[at+l]) && strchr(idchars, text[at+l]) == NULL))) {
            return l;
        }
    }
    return 0;
}

int check_iidtoken(char** strings, int num, int at, char* text, int ln, char* idchars) {
    int i, l;
    for (i=0;i<num;i++) {
        l = strlen(strings[i]);
        if (strncasecmp(text+at, strings[i], l) == 0 && (at+l==ln || (!alphanum(text[at+l]) && strchr(idchars, text[at+l]) == NULL))) {
            return l;
        }
    }
    return 0;
}

