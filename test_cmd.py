from distutils.core import Command
from distutils.errors import DistutilsOptionError
from distutils.fancy_getopt import longopt_xlate
import string
import sys
from unittest import TestLoader, main

uninitialized = object()

class test(Command):

    """Command to run unit tests after in-place build"""

    description = "run unit tests after in-place build"

    user_options = [
        ('test-type=', 't', 'Which test type to use (e.g. py.test, unittest)'),
    ]
    test_commands = {}

    def initialize_options(self):
        self.test_type = 'py.test'
        for (_,_,_,_,options) in self.test_commands.values():
            for option in options:
                name = string.translate(option[0], longopt_xlate).rstrip('=')
                setattr(self, name, uninitialized)

    @classmethod
    def add_type(cls, name, options=(), required=None, defaults={}, validate=None):
        for option in options:
            cls.user_options.append(option)
        def meta(function):
            cls.test_commands[name] = function, required, defaults, validate, options
        return meta

    def finalize_options(self):
        if self.test_type not in self.test_commands:
            raise DistutilsOptionError('invalid test_type')
        
        function, required, defaults, validate, options = self.test_commands[self.test_type]
        if validate is not None:
            validate(self)
        else:
            for option in options:
                name = string.translate(option[0], longopt_xlate).rstrip('=')
                value = getattr(self, name,)
                if value is uninitialized:
                    if name in defaults:
                        setattr(self, name, defaults[name])
                    elif required is None or name in required:
                        raise DistutilsOptionError('Required option not given: %s' % option[0])

    def with_project_on_sys_path(self, func):
        self.run_command('build')
        cmd = self.get_finalized_command('build_py')

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        from os.path import normpath as normalize_path

        try:
            sys.path.insert(0, normalize_path(cmd.build_lib))
            func()
        finally:
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)

    def run(self):
        self.with_project_on_sys_path(self.run_tests)

    def run_tests(self):
        self.test_commands[self.test_type][0](self)

def make_onetest(function):
    def meta(self):
        return function()
    return meta

def make_testcase(name, functions):
    import unittest
    suite = unittest.TestSuite()
    cls = type(name, (unittest.TestCase,), {})
    for fn in functions:
        real = make_onetest(fn)
        setattr(cls, fn.__name__, real)
        suite.addTest(cls(fn.__name__))
    return suite

import os

@test.add_type('py.test', options=(
    ('test-dir=', 'd', 'Direcotry in which to search for tests'),
    ('test-recursive', 'r', 'Search recursively'),
    ), defaults={'test_recursive':False})
def run_py_test(tester):
    try:
        import py
    except ImportError:
        py = None

    import glob
    import os
    if type(tester.test_dir) == str:
        tester.test_dir = [tester.test_dir]
    test_files = []
    def add_dir(dr):
        for item in os.listdir(dr):
            full = os.path.join(dr, item)
            if os.path.isdir(full) and tester.test_recursive:
                add_dir(full)
            elif os.path.isfile(full) and full.endswith('.py'):
                test_files.append(full)

    for dr in tester.test_dir:
        add_dir(dr)

    if py:
        py.test.cmdline.main(test_files)
    else:
        print 'WARNING: py.test not found. falling back to unittest. For more informative errors, install py.test'
        import unittest
        suite = unittest.TestSuite()
        for filen in test_files:
            mod = get_pyfile(filen)
            suite.addTest(make_testcase(filen,
                (fn for fn in mod.__dict__.values() if getattr(fn, '__name__', '').startswith('test_'))
            ))
        t = unittest.TextTestRunner()
        t.run(suite)

def get_pyfile(fname):
    import sys
    sys.path.insert(0, os.path.dirname(fname))
    mod = __import__(os.path.basename(fname)[:-3], None, None, ['__doc__'])
    return mod

def validate_unittest(tester):
    if tester.test_suite is None:
        if tester.test_modules is None:
            raise DistutilsOptionError(
                "You must specify a module or a suite"
            )
        tester.test_suite = self.test_module+".test_suite"
    elif tester.test_module:
        raise DistutilsOptionError(
            "You may specify a module or a suite, but not both"
        )

@test.add_type('unittest', options=(
        ('test-module=','m', "Run 'test_suite' in specified module"),
        ('test-suite=','s',
            "Test suite to run (e.g. 'some_module.test_suite')"),
    ), validate=validate_unittest)
def run_unittest(tester):
    import unittest
    unittest.main(
        None, None, [unittest.__file__, tester.test_suite],
        testLoader = unittest.TestLoader()
    )

