
class Node:
    def __init__(self, name, index, children = (), pos=(0,0)):
        self.name = name
        self.index = index
        self.children = list(children)
        self.pos = list(pos)
        self.parent = None
        self._str = None

    def __str__(self):
        if self._str is None:
            self._str = ''.join(str(x) for x in self.children)
        return self._str

    def __repr__(self):
        return '<Node name="%s" children="%d" at="%s">' % (self.name, len(self.children), self.pos)

    def clone(self):
        new = Node(self.name, self.index, self.children, self.pos)
        return new

    def add(self, children):
        for child in children:
            child.parent = self
            self.children.append(child)
            self._str = None

    def appendChild(self, node):
        node.parent = self
        self.children.append(node)
        self._str = None

    def remove(self):
        if self.parent and self in self.parent.children:
            self.parent.removeChild(self)
        else:
            raise Exception,'I have no parents'

    def dirty(self):
        self._str = None
        if self.parent:
            self.parent.dirty()

    def appendAfter(self, node):
        i = self.parent.children.index(self)
        self.parent.insert(i+1, node)

    def removeChild(self, child):
        self.children.remove(child)
        child.parent = None
        self.dirty()

    def insert(self, i, node):
        node.parent = self
        self.children.insert(i, node)
        self.dirty()

    def insertBefore(self, node):
        i = self.parent.children.index(self)
        self.parent.insert(i-1, node)

    def lineage(self):
        if self.parent:
            return self.parent.lineage() + ' > ' + self.name
        return self.name

    def find(self, name):
        if name[0] == '!':
            if str(self) == name[1:]:
                yield self
        elif self.name in (x.strip() for x in name.split(',')):
            yield self
        for child in self.children:
            for one in child.find(name):
                yield one
    
    def sfind(self, name):
        for child in self.children:
            for one in child.sfind(name):
                yield one

    def walk(self, strings=False):
        yield self
        for child in self.children:
            for one in child.walk(strings):
                yield one

    def nextNode(self):
        if not self.parent:
            return None
        i = self.parent.children.index(self)
        if i < len(self.parent.children) - 1:
            return self.parent.children[i+1]
        if self.parent:
            next = self.parent.nextNode()
            if next:
                return next.children[-1]
        return None

    def prevNode(self):
        if not self.parent:
            return None
        i = self.parent.children.index(self)
        if i > 0:
            return self.parent.children[i-1]
        if self.parent:
            prev = self.parent.prevNode()
            if prev:
                return prev.children[-1]
        return None

    def __eq__(self, other):
        if type(other) == str:
            return other[0] == str(self)[0]
        elif type(other) == tuple:
            return other[0] == self.name
        return NotImplemented
    
    def __getitem__(self, i):
        return str(self)[i]

class TextNode(Node):
    def __init__(self, string, i, pos=(0,0)):
        Node.__init__(self, None, i, children=[string], pos=pos)

    def add(self, children):
        self.children[0] += ''.join(children)

    def appendChild(self, string):
        self.children[0] += string

    def insert(self, i, string):
        raise Exception, 'cannot insert into a TextNode'

    def find(self, name):
        if name[0] == '!':
            if self.children[0] == name[1:]:
                yield self

    def sfind(self, name):
        if self.children[0].find(name)!=-1:
            yield self

    def walk(self, strings=False):
        if strings:
            yield self

# vim: et sw=4 sts=4
