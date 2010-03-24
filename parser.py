### tokenizer

from node import Node
debug = False

class Logger:
    def __init__(self):
        self.level = 0
    def log(self, *stuff):
        if debug:
            print '  '*self.level,
            for i in stuff:
                print i,
            print
    def inc(self):
        self.level += 1
    def dec(self):
        self.level -= 1

logger = Logger()

def matchliteral(text, i, rule):
    '''takes a text array (either strings or Nodes), current index, and the rule to be matched.
    returns (Node, index)
    or Null, index if there's no match'''
    logger.log( i,'match?', text[i], rule)
    if rule[0] == '!':
        if rule == '!':
            # epsilon; matches everythin, doesn't increment the index
            return Node('',i), i
        else:
            char = rule[1:]
            if isinstance(text[i], Node):
                # Node(s) matching a literal
                pre = text[i].pre
                at = text[i].index
                name = text[i].name
                otxt = txt = str(text[i])
                while len(txt)<len(char) and i<len(text)-1:
                    i+=1
                    txt+=str(text[i])
                if txt == char:
                    if txt == otxt:
                        return text[i].clone(), i+1
                    else:
                        n = Node(txt, i, True)
                        n = Node(name, i, False)
                        n.children = [txt]
                        return n, i+1
            elif text[i:i+len(char)] == char:
                # chars matching a literal
                i += len(char)
                return Node(char,i,True), i
    elif rule[0] == '@' and isinstance(text[i],Node) and text[i].name == rule[1:]:
        # rule matching a token
        return text[i], i+1
    return False,0

ignore = ('whites', 'comment')

def parserule(text, i, rule, state):
    grammar = state['grammar']
    at = list(state['at'])

    if i<len(text):logger.log( i,'rule: ',rule,text[i])

    logger.inc()
    state['stack'] += (rule,)
    if i>=len(text):
        if i>state['error'][0]:
            state['error'][3] = 'toolong'
            state['error'][0] = i
            state['error'][1] = state['stack'] + (0,)
            state['error'][2] = None
        logger.dec()
        return False, 0

    ## gather up the whitespace
    whites = []
    while isinstance(text[i], Node) and text[i].name in ignore:
        whites.append(text[i])
        i += 1
        if i>=len(text):
            return False,0

    # check for a literal match
    res, di = matchliteral(text, i, rule)
    if res:
        logger.log( 'yes!')
        if '\n' in str(res):
            state['at'][0] += str(res).count('\n')
            state['at'][1] = i+1
        logger.dec()
        if whites:
            #white = ''.join(str(w) for w in whites)
            old = res
            res = Node(old.name, old.index, True)
            res.children = whites + old.children
        return res, di
    elif rule[0] != '@' or not rule[1:] in grammar.rules: 
        ## should be a literal, didn't match. an error occured
        if i>state['error'][0]:
            state['error'][3] = 'badrule'
            if isinstance(text[i], Node):
                state['error'][4] = text[i].lineno(),text[i].charno()-len(text[i])
            state['error'][0] = i
            state['error'][1] = state['stack']+(str(text[i]),)
            state['error'][2] = text[i]
        state['at'] = at
        logger.dec()
        return False,0

    rule = rule[1:]
    if debug>1:print rule,grammar.firsts[rule]

    # go through rules for the specific rulename, checking each in order
    for n,one in enumerate(grammar.rules[rule]):
        if one == rule:continue
        if debug>1:
            print grammar.firsts[rule][n]
        # check "first" against the current character / Node
        if text[i][0] in grammar.firsts[rule][n] or hasattr(text[i],'name') and (text[i].name,) in grammar.firsts[rule][n]:
            res, di = parse_children(text, i, rule, one, state.copy())
            if not res:
                continue
            logger.dec()
            res.children = whites + res.children
            return res, di
    # nothing was matched, this rule doesn't work. bail out
    if debug>1:print 'no matches'
    if i>state['error'][0]:
        if debug>1:print i,text[i],text[i-2:i+3]
        if isinstance(text[i], Node):
            state['error'][4] = text[i].lineno(),0#text[i].charno()
        state['error'][0] = i
        state['error'][1] = state['stack']+(str(text[i]),)
        state['error'][2] = text[i]
    state['at'] = at
    logger.dec()
    return False, 0

def parse_children(text, i, rule, children, state):
    '''parses the text for a sequence of "child" tokens/chars.
    '''
    grammar = state['grammar']
    logger.log('children:',text[i], rule, children)
    at = list(state['at'])
    node = Node(rule, i)
    node.lno = state['at'][0]
    node.cno = i - state['at'][1]
    a = 0
    clen = len(children)
    while a < clen:
        if debug>1:
            print 'child of %s; item %d: %s' % (rule, a, children[a])
        # check for repeaters
        if a < clen-1:
            if debug>3:print 'check multi;',children[a+1],a,children[a]
            if children[a+1] == '+':
                res, di = parserule(text, i, children[a], state.copy())
                if not res:
                    state['at']=at
                    return False, 0
                node.children.append(res)
                i = di
            if children[a+1] in '+*':
                while 1:
                    at = list(state['at'])
                    if a < clen-2 and children[a+2] == '?':
                        # non-greedy
                        res, di = parse_children(text, i, rule, children[a+3:], state.copy())
                        if res:
                            node.children += res.children
                            return node, di
                    res, di = parserule(text, i, children[a], state.copy())
                    if not res:break
                    node.children.append(res)
                    i = di
                state['at'] = at
                a += 2
                continue
            elif children[a+1] == ':':
                # check, but don't consume
                res, di = parserule(text, i, children[a], state.copy())
                if not res:
                    state['at']=at
                    return False, 0
                a += 2
                continue
            elif children[a+1] == '?':
                if debug>3:print 'trying', children[a]
                res, di = parserule(text, i, children[a], state.copy())
                a += 2
                if not res:
                    continue
                elif debug>3:print 'good',res,children[a]
                node.children.append(res)
                i = di
                continue
        if children[a] == rule:
            a+=1
            continue
        # otherwise, try it straight
        logger.log( 'nomods')
        res, di = parserule(text, i, children[a], state.copy())
        if not res:
            logger.log(i, 'bailing out of %s; %s' % (rule, children[a]))
            if i > state['error'][0]:
                if isinstance(text[i], Node):
                    state['error'][4] = text[i].lineno(),text[i].charno()
                state['error'][3] = 'nochildren'
                state['error'][0] = i
                state['error'][1] = state['stack']+(str(text[i]),)
                state['error'][2] = text[i]
            state['at']=at
            return False, 0
        else:
            logger.log( 'good!',children[a])
        node.children.append(res)
        i = di
        a += 1
    return node, i

def totokens(node):
    assert node.name == 'start'
    for tokenw in node.children:
        tokenw.children[0].children[0].toliteral()
        yield tokenw.children[0].children[0]

def parse(text, grammar):
    error = [0, None, None, 'unknown error', (0,0)]
    state = {'error':error, 'stack':(), 'grammar':grammar, 'at':[0,0]}
    #print grammar.rules['<start>']
    node, char = parserule(text, 0, '@start', state.copy())
    if not node:
        if state['error'][1]:
            etext = "Syntax error while parsing %s: found '%s', expected %s"%(state['error'][1][-3],state['error'][1][-1],state['error'][1][-2])
            print 'error type:',state['error'][3]
            if type(state['error'][0]) in (list,tuple):
                lno, cno = state['error'][0]
                print 'Error at line %d, char %d' % (lno+1, cno+1)
            print etext#,state['error']
            sys.exit(1)
            #raise Exception,etext
        else:
            print 'idk what happened...',state['error']
            fail
    if not node:
        raise Exception,str(state['error'])
    last = len(text)-1
    while last > 0 and isinstance(text[last],Node) and text[last].name == 'whites':
        last -= 1
    if char < last:
        print "error",state['error']
        raise Exception,"Didn't parse the whole thing: %d - %d"%(char,len(text))
    return node

def gettokens(text):
    '''not to be used in production'''
    tokens = list(totokens(parse(text, 'data/tokenize.bnf')))
    #print [str(x) for x in tokens],tokens
    return parse(tokens, 'data/json.bnf')

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: parse.py [code file]'
        sys.exit(1)
    code, = sys.argv[1:]
    ext = code.split('.')[-1]
    if ext == 'py':
        from bnf import python as grammar
    elif ext == 'json':
        from bnf import json as grammar
    elif ext == 'js':
        from bnf import js as grammar
    elif ext == 'c':
        from bnf import c as grammar
    else:
        raise Exception,'no grammar found for that file type'
    debug=False
    #debug = True
    res = parse(open(code).read(), grammar.tokens)
    tokens = res.tokens()
    #print tokens
    junk = ()
    #junk = ('whites',)
    '''
    junkn = Node('',-1)
    for t in tokens:
        if t.name in junk:
            junkn.post += str(t)
        else:
            t.pre = junkn.full() + t.pre
            junkn = Node('',-1)
    '''

    tokens = tuple(t for t in tokens if t.name not in junk)
    #debug = True

    # print ''.join(a.full() for a in tokens)
    # for t in tokens:
    #    if t.name == 'keyword':
    #        print t,str(t),t.children
    # print 'tokened!'
    # debug = 1

    full = parse(tokens, grammar.main)
    print full

