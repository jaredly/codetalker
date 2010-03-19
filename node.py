
class Node:
    def __init__(self, name, index, literal = False):
        self.name = name
        self.index = index
        self.children = []
        self.isliteral = False
        if literal:
            self.children = [name]
            self.isliteral = True

    def __repr__(self):
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
        return self.children[0] == x or self.name == x
