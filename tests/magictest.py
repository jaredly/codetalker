#!/usr/bin/env python
import unittest
import inspect

class MagicTest(unittest.TestCase):
    @classmethod
    def _get_test_funcs(cls):
        testcase_methods = dir(unittest.TestCase)
        for m in inspect.classify_class_attrs(cls):
            if m.kind == 'method' and \
                    m.defining_class == cls and \
                    not m.name.startswith('_') and \
                    m.name not in testcase_methods:
                        yield (inspect.findsource(getattr(cls, m.name))[1],
                            m.name)
    
    @classmethod
    def toSuite(cls):
        funcs = sorted(cls._get_test_funcs())
        suite = unittest.TestSuite()
        for lineno, name in funcs:
            suite.addTest(cls(name))
        return suite

    @classmethod
    def runSuite(cls, vb=2):
        return unittest.TextTestRunner(verbosity=vb).run(cls.toSuite())

def suite(mod):
    print 'suiting',mod
    def meta():
        thesuite = unittest.TestSuite()
        module = __import__(mod)
        for sub in mod.split('.')[1:]:
            module = getattr(module, sub)
        for k,v in module.__dict__.iteritems():
            if inspect.isclass(v) and issubclass(v, MagicTest) and v.__module__ == mod:
                thesuite.addTest(v.toSuite())
        return thesuite
    return meta

def modsuite(*mods):
    def meta():
        return unittest.TestSuite(mod.all_tests() for mod in mods)
    return meta



# vim: et sw=4 sts=4
