### tokenizer

from node import Node
debug = False

def matchliteral(text, i, rule):
    if debug:print 'match?', text[i], rule
    if rule == 'e':
        return Node('',i), i
    if rule[0] == "'":
        char = rule[1:-1] or "'"
        if isinstance(text[i], Node):
            txt = str(text[i])
            while len(txt)<len(char) and i<len(text)-1:
                i+=1
                txt+=str(text[i])
            if txt == char:
                return char, i+1
        elif text[i:i+len(char)] == char:
            i += len(char)
            return char, i
    elif isinstance(text[i],Node) and text[i].name == rule:
        return text[i], i+1
    return False,0

def parserule(text, i, rule, state):
    grammar = state['grammar']
    at = list(state['at'])
    if debug:print 'rule: ',text[i],rule
    state['stack'] += (rule,)
    if i>=len(text):
        if i>state['error'][0]:
            state['error'][3] = 'toolong'
            state['error'][0] = i
            state['error'][1] = state['stack'] + (0,)
            state['error'][2] = None
        state['at'] = at
        return False, 0
    res, di = matchliteral(text, i, rule)
    if res:
        if not isinstance(res, Node):
            state['at'][1] += len(res)
            #print 'inc at',res,len(res),state['at']
            if '\n' in res:
                state['at'][0]+=1
                state['at'][1] = 0
        return res, di
    elif not rule in grammar.rules: ## should be a literal, didn't match. an error occured
        if i>state['error'][0]:
            state['error'][3] = 'badrule'
            if isinstance(text[i], Node):
                ## TODO: is that last subtraction really nessecary?
                state['error'][0] = text[i].lineno(),text[i].charno()-len(text[i])
            else:
                state['error'][0] = i
            state['error'][1] = state['stack']+(str(text[i]),)
            state['error'][2] = text[i]
        state['at'] = at
        return False,0

    for n,one in enumerate(grammar.rules[rule]):
        if text[i][0] in grammar.firsts[rule][n] or hasattr(text[i],'name') and text[i].name in grammar.firsts[rule][n]:
            res, di = parse_children(text, i, rule, one, state.copy())
            if not res:
                continue
            return res, di
    #if i>state['error'][0]:
    #    print i,text[i],text[i-2:i+3]
    #    if isinstance(text[i], Node):
    #        state['error'][0] = text[i].lineno(),text[i].charno()
    #    else:
    #        state['error'][0] = i
    #    state['error'][1] = state['stack']+(str(text[i]),)
    #    state['error'][2] = text[i]
    state['at'] = at
    return False, 0

def parse_children(text, i, rule, children, state):
    grammar = state['grammar']
    if debug:print 'children:',text[i], rule, children
    at = list(state['at'])
    node = Node(rule, i)
    node.lno, node.cno = state['at']
    a = 0
    clen = len(children)
    while a < clen:
        if a < clen-1:
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
            elif children[a+1] == '~':
                a += 2
                res, di = parserule(text, i, children[a], state.copy())
                if not res:
                    continue
                node.children.append(res)
                i = di
        res, di = parserule(text, i, children[a], state.copy())
        if not res:
            if i>state['error'][0]:
                state['error'][3] = 'nochildren'
                if isinstance(text[i], Node):
                    state['error'][0] = text[i].lineno(),text[i].charno()
                else:
                    state['error'][0] = i
                state['error'][1] = state['stack']+(str(text[i]),)
                state['error'][2] = text[i]
            state['at']=at
            return False, 0
        node.children.append(res)
        i = di
        a += 1
    return node, i

def totokens(node):
    assert node.name == '<start>'
    for tokenw in node.children:
        tokenw.children[0].children[0].toliteral()
        yield tokenw.children[0].children[0]

def parse(text, grammar):
    error = [0, None, None, 'unknown error']
    state = {'error':error, 'stack':(), 'grammar':grammar, 'at':[0,0]}
    node, char = parserule(text, 0, '<start>', state.copy())
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
            print 'idk what happened...'
            fail
    if not node:
        raise Exception,str(state['error'])
    if char<len(text):
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
    res = parse(open(code).read(), grammar.tokens)
    tokens = res.tokens()
    for i in tokens:
        print i,i.name,i.lineno(),i.charno()
    global debug
    #debug = True
    full = parse(tokens, grammar.main)
    print full
    for a in full.children:print a,a.name

