from rules import RuleLoader
from tokens import EOF, INDENT, DEDENT, Token
from errors import *

from nodes import AstNode, ParseTree, TokenStream
from logger import logger
import inspect

# from codetalker.pgm.cgrammar.tokenize import tokenize
# from codetalker.pgm.cgrammar import main
# from text import Text, IndentText

from codetalker.cgrammar import consume_grammar, get_tokens, get_parse_tree, get_ast

import time

TIME = False

def camelCase(text):
    return text.replace('_', ' ').title().replace(' ', '')

class Grammar:
    '''This is the main driving class -- it sets up the grammar,
    tokenizes, parses, and translates into an AST.

    "process" is the main entry point (currently) -- you feed it
    text, it gives you back a ParseTree (tokenizes and parses)
    '''
    special_tokens = (INDENT, DEDENT, EOF)
    def __init__(self, start, tokens=(), ignore=(), idchars='', indent=False, ast_tokens=()):
        '''Grammar constructor

            start: the start rule [function]
            tokens: an iterable of Token subclasses [used to tokenize text]
            ignore: tokens to ignore while parsing [often WHITE and COMMENT]
            indent: boolean (default false) indicating whether to output
                    INDENT and DEDENT tokens while tokenizing (got use in indentation
                    sensitive languages such as python) self.start = start
        '''
        self.start = start
        self.tokens = list(tokens) # + self.special_tokens
        self.ignore = tuple(ignore)
        for i in ignore:
            if i not in self.tokens and i not in self.special_tokens:
                self.tokens.append(i)
        for i in ast_tokens:
            if i not in self.tokens and i not in self.special_tokens:
                self.tokens.append(i)
        self.ast_tokens = tuple(self.tokens.index(tok) for tok in ast_tokens)
        self.indent = indent
        self.idchars = idchars

        self.token_rules = []
        self.token_names = []
        self.token_dict  = {}

        self.rules      = []
        self.rule_dict  = {}
        self.rule_names = []
        self.real_rules = []
        self.ast_attrs  = []
        self.ast_classes = type('ClassHolder', (), {})

        self.load_rule(self.start)
        self.replace_tokens()

        ## cache the grammar definition
        self.GID = consume_grammar(self.rules, self.ignore, self.indent,
                                   self.idchars, self.rule_names, self.rule_dict,
                                   self.tokens, self.ast_attrs)

    def load_rule(self, builder):
        '''Load a rule into the grammar and cache it for
        future use
        
        example rule:
            
            def start(rule):
                rule | (ID, '=', plus(value))
                rule.astAttrs = {'left':{'type':ID, 'single':True},
                                 'right':{'type':value}}
                rule.astName = 'main'

        self.ast_attrs[num] = ((name, which, single, start, end), ...)

            name: string
            which: int; positive for rule_id, negative for token_id
            single: boolean - restrict to one
            start: int
            end: int; for slicing
            optional: bool - default False
        '''
        if builder in self.rule_dict:
            return self.rule_dict[builder]
        num = len(self.rules)
        name = getattr(builder, 'astName', None)
        if name is None:
            name = camelCase(builder.__name__)
        
        rule = RuleLoader(self)
        rule.name = name

        self.rule_dict[builder] = num
        self.rules.append(rule)
        self.rule_names.append(name)
        self.real_rules.append(rule)
        self.ast_attrs.append(())
        builder(rule)
        rule.builder = builder
        if not rule.options:
            raise Exception('no rule options specified in %r' % builder)
        attrs = []
        for attr, dct in rule.astAttrs.iteritems():
            if type(dct) != dict:
                dct = {'type':dct}
            if type(dct['type']) not in (tuple, list):
                types = [dct['type']]
            else:
                types = dct['type']
            for typ in types:
                if inspect.isclass(typ):
                    if not issubclass(typ, Token):
                        raise AstError('invalid ast "type": %s (must be a token or rule)' % typ)
                    elif typ not in self.tokens:
                        self.tokens.append(typ)
                elif inspect.isfunction(typ):
                    if typ not in self.rule_dict:
                        raise AstError('invalid ast "type": %s (must be a token or rule)' % typ)
                else:
                    raise AstError('invalid ast "type": %s (must be a token or rule)' % typ)

        '''
        for attr, dct in rule.astAttrs.iteritems():
            error_suffix = ' for astAttr "%s" in rule "%s"' % (attr, name)
            if type(dct) != dict:
                dct = {'type':dct}
            if not 'type' in dct:
                raise RuleError('must specify a type' + error_suffix)
            if type(dct['type']) not in (tuple, list):
                dct['type'] = (dct['type'],)
            whiches = tuple(self.which(that) for that in dct['type'])
            attrs.append((attr, whiches, dct.get('single', False), dct.get('start', 0), dct.get('end', None), dct.get('optional', False)))
            '''
        self.ast_attrs[num] = {'attrs':rule.astAttrs, 'pass_single':getattr(rule, 'pass_single', False)}
        if len(rule.astAttrs):
            ## TODO: convert name to TitleCase for class name?
            setattr(self.ast_classes, name, type(name, (AstNode,), {'__slots__':('_tree',) + tuple(rule.astAttrs.keys())}))
        return num

    def replace_tokens(self):
        self.tokens = tuple(self.tokens) + self.special_tokens
        for rule in self.rules:
            for option in rule.options:
                self.replace_ind(option)

    def replace_ind(self, option):
        for i,item in enumerate(option):
            if inspect.isclass(item) and issubclass(item, Token):
                option[i] = -(1 + self.tokens.index(item))
            elif type(item) in (tuple, list):
                t = type(item)
                tmp = list(item)
                self.replace_ind(tmp)
                option[i] = t(tmp)

    def get_tokens(self, text):
        return get_tokens(self.GID, text)
        # return tokenize(self.tokens, text, self.indent)

    def get_ast(self, text, start=None):
        if start is None:
            start = self.start
        start_i = self.rule_dict[start]
        return get_ast(self.GID, text, start_i, self.ast_classes, self.ast_tokens)

    def get_parse_tree(self, text, start=None): ## , start=None, debug = False):
        '''main entry point for parsing text.

            text: string - to parse
            start: optional custom start function (for advanced parsing)
            # debug: boolean (default false) to output debug parse tracing
        '''
        if start is None:
            start = self.start
        if start not in self.rule_dict:
            raise KeyError("Invalid start rule", start, self.rule_dict.keys())
        start_i = self.rule_dict[start]
        return get_parse_tree(self.GID, text, start_i)
    process = get_parse_tree
    
    def which(self, obj):
        if isinstance(obj, Token):
            if not obj.__class__ in self.tokens:
                raise RuleError('invalid token specified: %r' % obj)
            return -(self.tokens.index(obj.__class__) + 1)
        # unused
        elif inspect.isclass(obj) and issubclass(obj, Token):
            if not obj in self.tokens:
                raise RuleError('invalid token specified: %r' % obj)
            return -(self.tokens.index(obj) + 1)
        elif obj in self.tokens:
            return -(self.tokens.index(obj) + 1)
        elif isinstance(obj, ParseTree):
            return obj.rule
        else:
            return self.rule_dict[obj]

    def which_(self, child):
        if isinstance(child, main.pyToken):
            return -(child.type + 1)
        elif isinstance(child, main.pyParseNode):
            return child.rule
        if type(child) == tuple:
            return -(child[0]+1)
        return child[0]

    def to_ast(self, tree):
        raise Exception('not using this one anymore')
        if isinstance(tree, main.pyToken):
            return self.tokens[tree.type](tree.value, tree.lineno, tree.charno)
        rule = tree.rule
        name = self.rule_names[rule]
        if self.ast_attrs[rule]:
            node = getattr(self.ast_classes, name)()
            node.name = name
            node._rule = rule
            node._tree = tree
            for attr, whiches, single, start, end, optional in self.ast_attrs[rule]:
                children = [child for child in tree.children if self.which_(child) in whiches]
                if single and len(children) <= start:
                    if optional:
                        setattr(node, attr, None)
                        continue
                    raise RuleError('ast attribute not found: %s' % attr)
                if single:
                    setattr(node, attr, self.to_ast(children[start]))
                else:
                    setattr(node, attr, tuple(self.to_ast(child) for child in children[start:end]))
            return node
        else:
            rload = self.real_rules[rule]
            if rload.pass_single:
                for child in tree.children:
                    if isinstance(child, main.pyToken):
                        if self.tokens[child.type] in self.ast_tokens:
                            return self.tokens[child.type](child.value, child.lineno, child.charno)
                    else:
                        return self.to_ast(child)
                raise RuleError('failure -- nothing to ast-tize %s %s' % (rload, tree))
            else:
                items = []
                for child in tree.children:
                    if isinstance(child, main.pyToken):
                        child = self.tokens[child.type](child.value, child.lineno, child.charno)
                        if child.rule in self.ast_tokens:
                            items.append(child)
                    else:
                        items.append(self.to_ast(child))
                return items

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
            if rule not in self.dont_ignore:
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
                        tokens.at = at
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
