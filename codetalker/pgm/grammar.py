from tokenize import tokenize
from text import Text, IndentText
from rules import RuleLoader
from tokens import EOF, INDENT, DEDENT
from errors import *

import sys

DEBUG = False

class ParseError(CodeTalkerException):
    pass

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tuple(tokens)
        self.at = 0

    def current(self):
        if self.at >= len(self.tokens):
            return EOF('')
            raise ParseError('ran out of tokens')
        return self.tokens[self.at]
    
    def next(self):
        self.at += 1
        if self.at > len(self.tokens):
            return EOF('')
            raise ParseError('ran out of tokens')
    advance = next

    def hasNext(self):
        return self.at < len(self.tokens) - 1

class ParseTree(object):
    def __init__(self, name):
        self.children = []

    def add(self, child):
        self.children.append(child)

class Logger:
    def __init__(self, output=True):
        self.indent = 0
        self.output = output
        self.text = ''

    def quite(self):
        self.output = False

    def loud(self):
        self.output = True

    def write(self, text):
        text = ' '*self.indent + text
        if self.output:
            sys.stdout.write(text)
        self.text += text

logger = Logger(DEBUG)
import time

class Grammar:
    def __init__(self, start, tokens, indent=False, ignore=[]):
        self.start = start
        self.tokens = tuple(tokens) + (INDENT, DEDENT, EOF)
        self.indent = indent
        self.ignore = tuple(ignore)
        t = time.time()
        self.load_grammar()
        print 'to load', time.time()-t

    def load_grammar(self):
        self.rules = []
        self.rule_dict = {}
        self.rule_names = []
        self.real_rules = []
        self.no_ignore = []
        self.load_func(self.start)
        print>>logger, self.rule_names
        print>>logger, self.rules

    def load_func(self, func):
        if func in self.rule_dict:
            return self.rule_dict[func]
        num = len(self.rules)
        self.rule_dict[func] = num
        rule = RuleLoader(self)
        self.rules.append(rule.options)
        name = getattr(func, 'astName', func.__name__)
        self.rule_names.append(name)
        self.real_rules.append(rule)
        func(rule)
        if getattr(rule, 'no_ignore', False):
            self.no_ignore.append(num)
        return num

    def get_tokens(self, text):
        return TokenStream(tokenize(self.tokens, text))

    def process(self, text, debug = False):
        logger.output = debug
        if self.indent:
            text = IndentText(text)
        else:
            text = Text(text)
        t = time.time()
        tokens = self.get_tokens(text)
        print 'tokenize', time.time()-t
        error = [0, None]
        t = time.time()
        tree = self.parse_rule(0, tokens, error)
        print 'parse', time.time()-t
        if tokens.hasNext() or tree is None:
            raise ParseError(error[1])
        return tree

    def parse_rule(self, rule, tokens, error):
        if rule < 0 or rule >= len(self.rules):
            raise ParseError('invalid rule: %d' % rule)
        print>>logger, 'parsing for rule', self.rule_names[rule]
        logger.indent += 1
        node = ParseTree(self.rule_names[rule])
        for option in self.rules[rule]:
            res = self.parse_children(rule, option, tokens, error)
            if res is not None:
                print>>logger, 'yes!',self.rule_names[rule], res
                logger.indent -= 1
                node.children = res
                return node
        print>>logger, 'failed', self.rule_names[rule]
        logger.indent -= 1
        return None
    
    def parse_children(self, rule, children, tokens, error):
        i = 0
        res = []
        while i < len(children):
            if rule not in self.no_ignore:
                while isinstance(tokens.current(), self.ignore):
                    res.append(tokens.current())
                    tokens.advance()
            current = children[i]
            print>>logger, 'parsing child',current,i
            if type(current) == int:
                if current < 0:
                    ctoken = tokens.current()
                    if isinstance(ctoken, self.tokens[-(current + 1)]):
                        res.append(ctoken)
                        tokens.advance()
                        i += 1
                        continue
                    else:
                        print>>logger, 'token mismatch', ctoken, self.tokens[-(current + 1)]
                        if tokens.at > error[0]:
                            error[0] = tokens.at
                            error[1] = 'Unexpected token %s; expected %s (while parsing %s)' % (ctoken, self.tokens[-(current + 1)], self.rule_names[rule])
                        return None
                else:
                    ctoken = tokens.current()
                    at = tokens.at
                    sres = self.parse_rule(current, tokens, error)
                    if sres is None:
                        tokens.at = at
                        if tokens.at >= error[0]:
                            error[0] = tokens.at
                            error[1] = 'Unexpected token %s; expected %s (while parsing %s)' % (ctoken, self.rule_names[current], self.rule_names[rule])
                        return None
                    res.append(sres)
                    i += 1
                    continue
            elif type(current) == str:
                ctoken = tokens.current()
                if current == ctoken.value:
                    res.append(ctoken)
                    tokens.advance()
                    i += 1
                    continue
                if tokens.at > error[0]:
                    error[0] = tokens.at
                    error[1] = 'Unexpected token %s; expected \'%s\' (while parsing %s)' % (ctoken, current.encode('string_escape'), self.rule_names[rule])
                print>>logger, 'FAIL string compare:', [current, tokens.current().value]
                return None
            elif type(current) == tuple:
                st = current[0]
                if st == '*':
                    print>>logger, 'star repeat'
                    while 1:
                        print>>logger, 'trying one'
                        at = tokens.at
                        sres = self.parse_children(rule, current[1:], tokens, error)
                        if sres:
                            print>>logger, 'yes! (star)'
                            res += sres
                        else:
                            print>>logger, 'no (star)'
                            tokens.at = at
                            break
                    i += 1
                    continue
                elif st == '+':
                    at = tokens.at
                    sres = self.parse_children(rule, current[1:], tokens, error)
                    if sres is not None:
                        res += sres
                    else:
                        return None
                    while 1:
                        at = tokens.at
                        sres = self.parse_children(rule, current[1:], tokens, error)
                        if sres:
                            res += sres
                        else:
                            tokens.at = at
                            break
                    i += 1
                    continue
                elif st == '|':
                    at = tokens.at
                    for item in current[1:]:
                        if type(item) != tuple:
                            item = (item,)
                        sres = self.parse_children(rule, item, tokens, error)
                        if sres:
                            res += sres
                            break
                        else:
                            tokens.at = at
                    else:
                        return None
                    i += 1
                    continue
                elif st == '?':
                    at = tokens.at
                    sres = self.parse_children(rule, current[1:], tokens, error)
                    if sres:
                        res += sres
                    else:
                        at = tokens.at
                    i += 1
                    continue
                else:
                    raise ParseError('invalid special token: %s' % st)
            return None
        return res


# vim: et sw=4 sts=4
