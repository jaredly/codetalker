#!/usr/bin/env python

from nnode import Node

import logging
logger = logging.getLogger('refresh')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(name)s:\t\t%(message)s'))

logger.addHandler(ch)

def match_whitespace(i, const):
    white = []
    while i < len(const['text']) and \
            isinstance(const['text'][i], Node) and\
            const['text'][i].name in const['ignore']:
                white.append(const['text'][i])
                txt = str(const['text'][i])
                if '\n' in txt:
                    const['pos'][0] += txt.count('\n')
                    const['pos'][1] = len(txt.split('\n')[-1])
                else:
                    const['pos'][1] += len(txt)
                i += 1
    return white, i

def match_rule(rule, i, const):
    node = const['text'][i]
    ppos = const['pos'][:]
    oi = i

    if rule[0] == '@':
        ## rule -- must match a token Node
        if isinstance(node, Node) and node.name == rule[1:]:
            return node.copy(), i+1
    else:
        # essentially espilon; matches anything and doesn't consume
        if rule == '!': 
            return Node('', i), i
        # other literal
        literal = rule[1:]
        if isinstance(node, Node):
            text = str(node)
            while len(txt) < len(literal) and i < len(const['text'])-1:
                i += 1
                text += str(const['text'][i])
            if text == literal:
                if text == str(node):
                    return node.clone(), i+1
                new = node.clone()
                new.children = [text]
                return new, i+1
        elif const['text'][i:i+len(literal)] == literal:
            node = Node(None, i, children = [literal], pos = const['pos'])
            if '\n' in literal:
                const['pos'][0] += literal.count('\n')
                const['pos'][1] = 0
            const['pos'][1] += len(literal.split('\n')[-1])
            return node, i + len(literal)

    const['pos'] = ppos
    return False, oi

def parse_rule(rule, i, const):
    '''parse the text for a certain rule'''
    oi = i
    white, i = match_whitespace(i, const)
    node, i = match_rule(rule, i, const)
    if node:
        return white + [node], i

    if rule[0] == '!' or rule[1:] not in const['grammar'].rules:
        set_error(const, 'Expected: %(rule)s, found %(name)s')
        return [], oi

    name = rule[1:]
    node = const['text'][i]
    for o, option in enumerate(const['grammar'].rules[name]):
        if node in const['grammar'].firsts[name][o]:
            node, i = parse_option(rule, i, option, const)
            if node:
                return white + [node], i
    return [], oi

def parse_option(rule, i, option, const):
    '''parses for one option of a rule'''
    oi = i
    ppos = const['pos'][:]

    node = Node(rule, i)
    node.pos = const['pos']

    olen = len(option)
    o = 0
    while o < olen:

        if o < olen - 1: # check repeaters
            if option[o+1] == '+':
                nodes, i = parse_rule(option[o], i, const)
                if not result:
                    const['pos'] = ppos
                    return False, oi
                node.add(nodes)

            if option[o+1] in '+*':
                while 1:
                    #ppos = const['pos'][:]

                    if o < olen-2 and option[o+2] == '?':
                        # non greedy
                        result, i = parse_children(rule, i, option[o+3:], const)
                        if result:
                            node.children += result.children
                            return node, i
                    nodes, i = parse_rule(option[o], i, const)
                    if not result:break
                    node.add(nodes)
                o += 2
                continue
            elif option[o+1] in ':?':
                nodes, i = parse_rule(option[o], i, const)
                if not nodes:
                    if option[o+1] == '?':
                        o += 2
                        continue
                    const['pos'] = ppos
                    return False, oi
                if option[o+1] != ':':
                    node.add(nodes)
                o += 2
                continue
        if option[o] == rule:
            pass # o+=1;continue ? that eliminates recursion....right?
        nodes, i = parse_rule(option[o], i, const)
        #if not result:
        #    set_error(const, 'Expected
        if not result:
            const['pos'] = ppos
            return False, oi
        node.add(nodes)
        o += 1
    return node, i

def parse(text, grammar):
    const = {'pos':[0,0],'text':text,'error':{},'grammar':grammar}
    nodes, i = parse_rule('@start', 0, const)
    if not nodes:
        print 'error'
    print 'ya'
    print nodes






    


# vim: et sw=4 sts=4
