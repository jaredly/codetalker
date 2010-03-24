
class Node:
    def __init__(self, name, index, children = ()):
        self.name = name
        self.index = index
        self.children = list(children)
        self.pos = (0,0)
        self.parent = None

    def add(self, children):
        for child in children:
            child.parent = self
            self.children.append(child)
        

# vim: et sw=4 sts=4
