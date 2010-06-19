
class Child:
    empty = False
    def __init__(self, *items):
        self.items = items
    def __iter__(self):
        return iter(self.items)
    def process(self, parent):
        self.items = parent.process(items)
    def check(self, check):
        return check(self.items[0])
    def first(self, first):
        return first(self.items[0])

class plus(Child):
    pass

class star(Child):
    empty = True

class maybe(Child):
    empty = True

class _or(Child):
    def check(self, check):
        for item in self.items:
            if check(item):
                return True
    def first(self, first):
        items = []
        for child in self.items:
            items += first(child)

class expand(Child):
    def __init__(self, text):
        self.text = text
        self._or = _or(self.individuals())
    def __iter__(self):
        return self_or.__iter__()
    def check(self, check):
        return self._or.check(check)
    def process(self, parent):
        pass

'''
Grammar is stored in an expanded, optimized format.

rules = {
    'name': (option1, option2)
}
option1 = (child1, child2, ...)
child1 =
    '@rule_name'
    '!literal'
'''

import types

class Rules:
    def __init__(self):
        self.rule_ids = {}
        self.name_ids = {}
        self.rule_funcs = {}
        self.rules = []
        self.first = None

    def start(self, func):
        self.first = func
        self.do_rule(func)

    def process(self, option):
        res = []
        for child in option:
            if isinstance(child, Special):
                res.append(child)
                child.process(self)
            elif type(child) == str:
                res.append(child)
            elif type(child) == types.FunctionType:
                num = self.do_rule(child)
                res.append(self.rule_funcs[child])
            elif type(child) == tuple:
                res += self.process(child)
            elif type(child) == list:
                if len(child) == 1:
                    res.append(self.process(child))
                else:
                    nc = maybe(*child)
                    nc.process(self)
                    res.append(nc)
            else:
                raise TypeError('invalid child ', child)
        return res

    def do_rule(self, func):
        if func not in self.rule_ids:
            self.rule_ids[func] = self.name_ids[func.__name__] = len(self.rules)
            rule = Rule(self, func)
            self.rule_funcs[func] = rule
            self.rules.append(rule)
        return self.rule_ids[func]

class Rule:
    def __init__(self, parent, function):
        self.options = []
        self.parent = parent
        self.function = function
        self.name = function.__name__
        function(self)

    def __or__(self, other):
        if type(other) != tuple:
            other = [other]
        self.add_option(*other)
        return self

    def add_option(self, *children):
        if len(children) == 1 and isinstance(children[0], _or):
            for item in children[0]:
                self.add_option(item)
            return
        self.options.append(self.parent.process(children))

    def firsts(self, char):
        for option in self.options:
            for item in option.firsts(char):
                yield item


# vim: et sw=4 sts=4
