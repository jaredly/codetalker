
class Node:
    def __init__(self, name, index, literal = False):
        self.name = name
        self.index = index
        self.lno = -1
        self.cno = -1
        self.pre = ''
        self.children = []
        self.post = ''
        self.isliteral = False
        if literal:
            self.children = [name]
            self.isliteral = True

    def lineno(self):
        if self.lno>=0:return self.lno
        return self.children[0].lineno()
    
    def charno(self):
        if self.cno>=0:return self.cno
        return self.children[0].charno()

    def __repr__(self):
        return '<Node %s with %d children>'%(self.name.strip('<>'),len(self.children))

    def __str__(self):
        res = ''
        for c in self.children:
            res += str(c)
        return res
    
    def full(self):
        res = self.pre
        for c in self.children:
            if type(c) == str:
                res += c
            else:
                res += c.full()
        return res + self.post
    
    def toXML(self):
        if not self.name:return ''
        name = self.name.strip('<>')
        return '<%s>\n  %s\n</%s>' % (name, 
                ('\n'.join((isinstance(c,Node) and c.toXML() or str(c)) for c in self.children)).replace('\n','\n  '), 
                name)
    
    def tokens(self):
        return list(a.children[0] for a in self.getElementsByTagName('token') if a.children[0].toliteral())

    def getElementsByTagName(self, name):
        res = []
        if self.name == name:
            res.append(self)
        for child in self.children:
            if type(child)!=str:
                res += child.getElementsByTagName(name)
        return res
    
    gETN = getElementsByTagName

    def toliteral(self):
        self.children = [str(self)]
        self.isliteral = True
        return True
    
    def appendChild(self, child):
        self.children.append(child)

    def __getitem__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0][x]

    def __len__(self):
        if not self.isliteral:return 1#raise Exception,'not a literal'
        return len(self.children[0])

    def __eq__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0] == x or self.name == x
