
class Node:
    def __init__(self, name, literal = False):
        self.name = name
        self.children = []
        self.isliteral = False
        if literal:
            self.children = [name]
            self.isliteral = True

    def __repr__(self):
        '''txt = self.name+'\n'
        for child in self.children:
            txt += child.__repr__().replace('\n','\n  ')
        txt += self.name.replace('<','</')+'\n'
        return txt'''
        return '<Node %s with %d children>'%(self.name.strip('<>'),len(self.children))

    def __str__(self):
        res = ''
        for c in self.children:
            res += str(c)
        return res

    def getElementsByTagName(self, name):
        res = []
        if self.name == name:
            res.append(self)
        for child in self.children:
            if type(child)!=str:
                res += child.getElementsByTagName(name)
        return res

    def toliteral(self):
        self.children = [str(self)]
        self.isliteral = True

    def __getitem__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0][x]

    def __len__(self):
        if not self.isliteral:return 1#raise Exception,'not a literal'
        return len(self.children[0])

    def __eq__(self,x):
        if not self.isliteral:raise Exception,'not a literal'
        return self.children[0] == x
