from tokenize import tokenize
from text import Text, IndentText
from rules import RuleLoader
from tokens import EOF, INDENT, DEDENT, Token
from errors import *

from nodes import AstNode, ParseTree, TokenStream
from logger import logger

import time

TIME = False

def timeit(func, *args, **kwargs):
    start = time.time()
    res = func(*args, **kwargs)
    total = time.time() - start
    print >> logger, 'time to execute %s: %s' % (func, total)
    return res

class Grammar:
    '''This is the main driving class -- it sets up the grammar,
    tokenizes, parses, and translates into an AST.

    "process" is the main entry point (currently) -- you feed it
    text, it gives you back a ParseTree (tokenizes and parses)'''
    special_tokens = (INDENT, DEDENT, EOF)
    def __init__(self, start, tokens, ignore=(), indent=False):
        '''Grammar constructor

            start: the start rule [function]
            tokens: an iterable of Token subclasses [used to tokenize text]
            ignore: tokens to ignore while parsing [often WHITE and COMMENT]
            indent: boolean (default false) indicating whether to output
                    INDENT and DEDENT tokens while tokenizing (got use in indentation
                    sensitive languages such as python) self.start = start
        '''
        self.start = start
        self.tokens = tuple(tokens) + self.special_tokens
        self.ignore = tuple(ignore)
        self.indent = indent
        if TIME: timeit(self.load_grammar)
        else: self.load_grammar()

    def load_grammar(self):
        self.rules      = []
        self.rule_dict  = {}
        self.rule_names = []
        self.real_rules = []
        self.no_ignore  = []
        self.load_rule(self.start)
        if logger.output:print>>logger, self.rule_names
        if logger.output:print>>logger, self.rules

    def load_rule(self, func):
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

    def process(self, text, start=None, debug = False):
        '''main entry point for parsing text.

            text: string - to parse
            start: optional custom start function (for advanced parsing)
            debug: boolean (default false) to output debug parse tracing
        '''
        logger.output = debug
        if self.indent:
            text = IndentText(text)
        else:
            text = Text(text)
        # get tokens
        if TIME: tokens = timeit(self.get_tokens, text)
        else: tokens = self.get_tokens(text)
        # set starting rule
        if start is not None:
            start = self.rule_dict[start]
        else:
            start = 0
        error = [0, None]

        # go for it
        if TIME: tree = timeit(self.parse_rule, start, tokens, error)
        else: tree = self.parse_rule(start, tokens, error)

        # either not everything was parsed or nothing was returned
        if tokens.hasNext() or tree is None:
            raise ParseError(error[1])

        return tree
    
    def toAst(self, tree):
        if isinstance(tree, Token):
            return tree
        rule = tree.rule
        attrs = getattr(self.real_rules[rule], 'astAttrs', None)
        if attrs is None:
            if getattr(self.real_rules[rule], 'astAll', None):
                node = AstNode(self.rule_names[rule])
                node._tree = tree
                node.items = [self.toAst(child) for child in tree.children]
                return node
            children = [self.toAst(child) for child in tree.children if isinstance(child, ParseTree)]
            if not children:
                raise ParseError('no ast children for node %s' % tree.name)
            return children
        node = AstNode(self.rule_names[rule])
        node._tree = tree
        for key, value in attrs.iteritems():
            parts = tuple(part.strip() for part in value.split(','))
            if len(parts) == 1:
                if value.endswith('[]'):
                    item = [self.toAst(child) for child in tree.children if isinstance(child, ParseTree) and\
                            child.name == value[:-2] or child.__class__.__name__ == value[:-2]]
                elif '[' in value and value.endswith(']'):
                    name, slice = value.split('[', 1)
                    start, end = slice[:-1].split(':')
                    if start: start = int(start)
                    else: start = None
                    if end: end = int(end)
                    else: end = None
                    item = [child for child in tree.children if isinstance(child, ParseTree) and\
                            child.name == name or child.__class__.__name__ == name]
                    #print 'splitting for', value, 
                    item = [self.toAst(child) for child in item[start:end]]
                else:
                    for child in tree.children:
                        if isinstance(child, ParseTree) and child.name == value\
                                or child.__class__.__name__ == value:
                            item = self.toAst(child)
                            break
                    else:
                        raise ParseError('No child matching %s' % value)
            else:
                item = [self.toAst(child) for child in tree.children if isinstance(child, ParseTree) and\
                        child.name in parts or child.__class__.__name__ in parts]
            setattr(node, key, item)
        return node

    def parse_rule(self, rule, tokens, error):
        if rule < 0 or rule >= len(self.rules):
            raise ParseError('invalid rule: %d' % rule)
        if logger.output:print>>logger, 'parsing for rule', self.rule_names[rule]
        logger.indent += 1
        node = ParseTree(rule, self.rule_names[rule])
        for option in self.rules[rule]:
            res = self.parse_children(rule, option, tokens, error)
            if res is not None:
                if logger.output:print>>logger, 'yes!',self.rule_names[rule], res
                logger.indent -= 1
                node.children = res
                return node
        if logger.output:print>>logger, 'failed', self.rule_names[rule]
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
            if logger.output:print>>logger, 'parsing child',current,i
            if type(current) == int:
                if current < 0:
                    ctoken = tokens.current()
                    if isinstance(ctoken, self.tokens[-(current + 1)]):
                        res.append(ctoken)
                        tokens.advance()
                        i += 1
                        continue
                    else:
                        if logger.output:print>>logger, 'token mismatch', ctoken, self.tokens[-(current + 1)]
                        if tokens.at > error[0]:
                            error[0] = tokens.at
                            error[1] = 'Unexpected token %s; expected %s (while parsing %s)' % (repr(ctoken), self.tokens[-(current + 1)], self.rule_names[rule])
                        return None
                else:
                    ctoken = tokens.current()
                    at = tokens.at
                    sres = self.parse_rule(current, tokens, error)
                    if sres is None:
                        tokens.at = at
                        if tokens.at >= error[0]:
                            error[0] = tokens.at
                            error[1] = 'Unexpected token %s; expected %s (while parsing %s)' % (repr(ctoken), self.rule_names[current], self.rule_names[rule])
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
                    error[1] = 'Unexpected token %s; expected \'%s\' (while parsing %s)' % (repr(ctoken), current.encode('string_escape'), self.rule_names[rule])
                if logger.output:print>>logger, 'FAIL string compare:', [current, tokens.current().value]
                return None
            elif type(current) == tuple:
                st = current[0]
                if st == '*':
                    if logger.output:print>>logger, 'star repeat'
                    while 1:
                        if logger.output:print>>logger, 'trying one'
                        at = tokens.at
                        sres = self.parse_children(rule, current[1:], tokens, error)
                        if sres:
                            if logger.output:print>>logger, 'yes! (star)'
                            res += sres
                        else:
                            if logger.output:print>>logger, 'no (star)'
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
