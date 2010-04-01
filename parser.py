#!/usr/bin/env python

from node import Node, TextNode

debug = 0

class Logger:
    def __init__(self):
        self.level = 0
    def log(self, *stuff):
        if debug:
            print '..'*self.level,
            for i in stuff:
                print i,
            print
    def inc(self):
        self.level += 1
    def dec(self):
        self.level -= 1

logger = Logger()

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
    if i >= len(const['text']):
        if rule == '!':
            return Node(None, i, False), i
        return False, i
    logger.log('match? "%s" "%s"' % (rule, const['text'][i]), i)
    node = const['text'][i]
    ppos = const['pos'][:]
    oi = i

    if rule[0] == '@':
        ## rule -- must match a token Node
        if isinstance(node, Node) and node.name == rule[1:]:
            return node.clone(), i+1
    else:
        # essentially espilon; matches anything and doesn't consume
        if rule == '!': 
            return Node(None, i, False), i
        # other literal
        literal = rule[1:]
        if isinstance(node, Node):
            text = str(node)
            while len(text) < len(literal) and i < len(const['text'])-1:
                i += 1
                text += str(const['text'][i])
            if text == literal:
                if text == str(node):
                    return node.clone(), i+1
                new = node.clone()
                new.children = [TextNode(text,i, False)]
                return new, i+1
        elif const['text'][i:i+len(literal)] == literal:
            logger.log('match!',rule)
            node = TextNode(literal, i, False, pos = const['pos'])
            if '\n' in literal:
                const['pos'][0] += literal.count('\n')
                const['pos'][1] = 0
            const['pos'][1] += len(literal.split('\n')[-1])
            return node, i + len(literal)
        else:
            logger.log([const['text'][i:i+len(literal)]],i,len(literal),[literal])

    const['pos'] = ppos
    return False, oi

def parse_rule(rule, i, const):
    '''parse the text for a certain rule'''
    if i < len(const['text']):
        logger.log('parse "%s" "%s"' % (rule,const['text'][i]))
    const['stack'].append(rule)
    logger.inc()
    oi = i
    white, i = match_whitespace(i, const)
    node, i = match_rule(rule, i, const)
    if node:
        const['stack'].pop(-1)
        logger.dec()
        return white + [node], i
    elif i < len(const['text']):
        node = const['text'][i]
        logger.log('no match', i, rule, len(const['text']), [node])

    if i >= len(const['text']):
        logger.log('what? out of input',len(const['text']),i)
        set_error(const, i, rule, 'Ran out of input')
        const['stack'].pop(-1)
        logger.dec()
        return [], oi
    if rule[0] == '!' or rule[1:] not in const['grammar'].rules:
        set_error(const, i, rule)
        logger.log('nope. wanted "%s" got "%s"' % (rule[1:],const['text'][i]))
        const['stack'].pop(-1)
        logger.dec()
        return [], oi
        

    name = rule[1:]
    node = const['text'][i]
    for o, option in enumerate(const['grammar'].rules[name]):
        if node in const['grammar'].firsts[name][o]:
            #logger.log(const['grammar'].firsts[name][o], node)
            logger.log('first good',[node],rule)
            result, i = parse_option(rule, i, option, const)
            if result:
                const['stack'].pop(-1)
                logger.dec()
                return white + [result], i
    set_error(const,i,rule,'No matches found for rule "%s" on input "%s"' % (rule, node))
    #if debug:
    #    print const['grammar'].firsts[name]
    const['stack'].pop(-1)
    logger.dec()
    return [], oi

def parse_option(rule, i, option, const):
    '''parses for one option of a rule'''
    oi = i
    ppos = const['pos'][:]

    node = Node(rule[1:], i, False)
    node.pos = const['pos']

    olen = len(option)
    o = 0
    while o < olen:

        if o < olen - 1: # check repeaters
            if option[o+1] == '+':
                nodes, i = parse_rule(option[o], i, const)
                if not nodes:
                    const['pos'] = ppos
                    return False, oi
                node.add(nodes)

            if option[o+1] in '+*':
                while 1:
                    #ppos = const['pos'][:]

                    if o < olen-2 and option[o+2] == '?':
                        # non greedy
                        logger.log('speculate...')
                        result, i = parse_option(rule, i, option[o+3:], const)
                        if result:
                            node.children += result.children
                            logger.log('spec done')
                            return node, i
                        logger.log('spec failed')
                    nodes, i = parse_rule(option[o], i, const)
                    if not nodes:
                        break
                    node.add(nodes)
                o += 2
                continue
            elif option[o+1] == '?':
                nodes, ni = parse_rule(option[o], i ,const)
                if nodes:
                    node.add(nodes)
                    i = ni
                o += 2
                continue
            elif option[o+1] == ':':
                nodes, ni = parse_rule(option[o], i, const)
                const['pos'] = ppos
                if not nodes:
                    return False, oi
                o += 2
                continue
        if option[o] == rule:
            pass # o+=1;continue ? that eliminates recursion....right?
        nodes, i = parse_rule(option[o], i, const)
        if not nodes:
            const['pos'] = ppos
            return False, oi
        node.add(nodes)
        o += 1
    return node, i

def set_error(const, i, rule, message = None):
    if message is None:
        message = 'Found "%s", expected "%s"' % (const['text'][i], rule[1:])
        message += '\n' + ''.join(str(a) for a in const['text'][i-10:i])
    if i >= const['error']['i']:
        const['error'] = {'i':i, 'pos':const['pos'],
                'stack':const['stack'][:],
                'message':message}

import sys

def parse(text, grammar, ignore=('whites','comment')):
    const = {'pos':[0,0],'ignore':ignore,'text':text,'stack':[],'error':{'i':0},'grammar':grammar}
    nodes, i = parse_rule('@start', 0, const)
    last_white = len(text) - 1
    while isinstance(text[last_white],Node) and text[last_white].name in ignore:
        last_white -= 1

    if not nodes:
        print>>sys.stderr, 'Parsing Aborted'
        print
        if const['error'] == {'i':0}:
            print>>sys.stderr, '    Strange error...'
        else:
            print>>sys.stderr, '    Error found at %s: %s' % (const['error']['pos'],
                    const['error']['message'])
            print>>sys.stderr, '    stack:',const['error']['stack']
        sys.exit(1)

    elif i < last_white:
        print>>sys.stderr, 'Not everything was parsed: %d out of %d items' % (i, len(text))
        print
        if const['error'] == {'i':0}:
            print>>sys.stderr, '    Strange error...'
        else:
            print>>sys.stderr, '    Error found at %s: %s' % (const['error']['pos'],
                    const['error']['message'])
            print>>sys.stderr, '    stack:',const['error']['stack']
            print>>sys.stderr, 'text:',''.join(str(a) for a in const['text'][const['error']['i']-5:const['error']['i']+5])
        sys.exit(1)

    root = nodes[-1]
    for node in nodes[:-1]:
        node.parent = root
    root.children = nodes[:-1] + root.children
    root.add(text[last_white + 1:])
    
    return root, i, const






    

# vim: et sw=4 sts=4
