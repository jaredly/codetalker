/**
 * Part of Codetalker
 * author: Jared Forsyth <jared@jaredforsyth.com>
 */

#include "_speed_tokens.h"

/**
 * Backend code for tokenizing strings
 */
int string(int at, char* text, int ln) {
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

int alpha_(char what) {
    return (what >= 'a' && what <= 'z') || (what >= 'A' && what <= 'Z') || what == '_';
}

int num(char what) {
    return (what >= '0' && what <= '9');
}

int id(int at, char* text, int ln) {
    int i = at;
    if (!alpha_(text[i])) {
        return 0;
    }
    i += 1;
    while (i < ln && (alpha_(text[i]) || num(text[i]))) {
        i++;
    }
    return i - at;
}

int white(int at, char* text, int ln) {
    int i = at;
    while (i < ln && (text[i] == ' ' || text[i] == '\t')) {
        i++;
    }
    return i - at;
}

int newline(int at, char* text, int ln) {
    if (text[at] == '\n')
        return 1;
    return 0;
}

int number(int at, char* text, int ln) {
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
        return i - at;
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
        return i - at;
    }
    return 0;
}

int check_token(ttype which, int at, char* text, int ln) {
    switch (which) {
        case tSTRING:
            return string(at, text, ln);
        case tID:
            return id(at, text, ln);
        case tWHITE:
            return white(at, text, ln);
        case tNEWLINE:
            return newline(at, text, ln);
        case tNUMBER:
            return number(at, text, ln);
        default:
            return 0;
    }
}

