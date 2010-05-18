
def str_node(node):
    text = ''
    for child in node.walk(True):
        if isinstance(child, TextNode):
            text += str(child)
    return text

def xml_node(node, level=10):
    return ''.join(node.walkXML(level))

class Node:
    def __init__(self, name, index, final=True, children = (), pos=(0,0)):
        self.name = name
        self.index = index
        self.children = list(children)
        for child in self.children:
            if isinstance(child,Node):
                child.parent = self
        self.pos = list(pos)
        self.parent = None
        self.final = final
        self._str = None

    def __str__(self):
        if self._str is None:
            self._str = ''.join(str(x) for x in self.children)
        return self._str

    def __repr__(self):
        return '<Node name="%s" children="%d" at="%s">' % (self.name, len(self.children), self.pos)

    def walkXML(self, level=5):
        if level <= 0:
            yield str_node(self) + '\n'
        else:
            start = '<%s at="%s">' % (self.name, self.pos)
            if 1 or len(self.children) > 1:
                start += '\n'
            yield start
            for child in self.children:
                for string in child.walkXML(level-1):
                    string = '  ' + string
                    yield string.replace('\n', '\n  ')
            end = '</%s>' % self.name
            if 1 or self.parent and len(self.parent.children) > 1:
                end += '\n'
            yield end
    
    def finalize(self):
        self.final = True
        for child in self.children:
            child.finalize()

    def clone(self):
        new = Node(self.name, self.index, self.final, self.children, self.pos)
        return new

    def add(self, children):
        for child in children:
            if child.parent is not None:
                child.remove()
            child.parent = self
            self.children.append(child)
            self._str = None

    def appendChild(self, node):
        if node.parent is not None:
            node.remove()
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
        for i,node in enumerate(self.children):
            if child is node:
                break
        else:
            raise Exception,'child not found "%s"' % child
        self.children = self.children[:i] + self.children[i+1:]
        child.parent = None
        self.dirty()

    def insert(self, i, node):
        if node.parent is not None:
            node.remove()
        node.parent = self
        self.children.insert(i, node)
        self.dirty()

    def insertBefore(self, node):
        i = self.parent.children.index(self)
        self.parent.insert(i, node)

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
        children = self.children[:]
        for child in children:
            for one in child.find(name):
                yield one
    
    def sfind(self, name):
        children = self.children[:]
        for child in children:
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
            if type(next) == str:
                return next
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
        if self.final:
            return NotImplemented
        if type(other) == str:
            return other[0] == str(self)[0]
        elif type(other) == tuple:
            return other[0] == self.name
        return NotImplemented
    
    def __getitem__(self, i):
        return str(self)[i]
    
    def reparent(self):
        for child in self.children:
            if child.parent is not None and child.parent is not self:
                child.remove()
            #if child.parent != self:
            #    print 'what?',self.name,[child],[child.parent],[self]
            child.parent = self
            child.reparent()

class TextNode(Node):
    def __init__(self, string, i, final=True, pos=(0,0)):
        Node.__init__(self, None, i, final, children=[string], pos=pos)

    def walkXML(self, level):
        return ''.join(self.children) + '\n'

    def finalize(self):
        self.final = True

    def clone(self):
        return TextNode(self.children[0], self.index, self.final, self.pos)

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

    def reparent(self):
        pass

# vim: et sw=4 sts=4
