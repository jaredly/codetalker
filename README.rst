CodeTalker
==========

.. image:: https://travis-ci.org/jabapyth/codetalker.png?branch=master
   :target: https://travis-ci.org/jabapyth/codetalker

Codetalker has just undergone major revision! :D

The goal of code talker is to allow for speedy development of parsers +
translators without compromizing performance or flexibility.

Features:

- Completely python-based grammar definitions `[example grammar]
  <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py>`_
- Fast (cythonized) tokenizing and parsing

...what more do you need?

Here's the process:

:tokenize: `produce a list of tokens`

    If you use the builtin tokens, you can get full c performance, and
    if you need a bit more flexibility, you can define your own token - either
    based on ReToken or StringToken

:parse: `produce a ParseTree`

    The parse tree corresponds exactly to your rules + original tokens;
    calling str(tree) returns *the exact orignal code*. Including whitespace,
    comments, etc. This step is perfect of you want to make some automated
    modifications to your code (say, prettyfication), but don't want to
    completely throw out your whitespace and comments.

:Abstract Syntax Tree: `parsetree -> ast` http://docs.python.org/library/ast.html

    An AST is used if you only care about the syntax -- whitespace, etc.
    doesn't matter. This the case during compilation or in some cases
    introspection. I've modeled Codetalker's AST implementation after that of
    python. Codetalker does the ParseTree -> AST conversion for you; you just
    tell it how to populate your tree, base on a given node's children.

:Translate:

    Once you get the AST, you want to do something with it, right? Most often
    it's "traverse the tree and do something with each node, depending on it's
    type". Here's where the `Translator
    <http://github.com/jabapyth/codetalker/blob/master/codetalker/pgm/translator.py>`_
    class comes in. It provied a nice easy interface to systematically
    translate an AST into whatever you want. `Here's an example
    <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py#L39>`_
    of creating and filling out a Translator.

For more info, check out my announcing blog post: `Announcing: CodeTalker
<http://jaredforsyth.com/blog/2010/jul/8/announcing-codetalker/>`_.

Here's the JSON grammar::

    # some custom tokens
    class SYMBOL(ReToken):
        rx = re.compile('[{},[\\]:]')

    class TFN(ReToken):
        rx = re.compile('true|false|null')

    # rules (value is the start rule)
    def value(rule):
        rule | dict_ | list_ | STRING | TFN | NUMBER
        rule.pass_single = True

    def dict_(rule):
        rule | ('{', [commas((STRING, ':', value))], '}')
        rule.astAttrs = {'keys': STRING, 'values': value}
    dict_.astName = 'Dict'

    def list_(rule):
        rule | ('[', [commas(_or(dict_, list_, STRING, TFN, NUMBER))], ']')
        rule.astAttrs = {'values': [dict_, list_, STRING, TFN, NUMBER]}
    list_.astName = 'List'

    grammar = Grammar(start=value,
                    tokens=[STRING, NUMBER, NEWLINE, WHITE, SYMBOL, TFN],
                    ignore=[WHITE, NEWLINE],              # we don't care about whitespace...
                    ast_tokens=[STRING, TFN, NUMBER])     # tokens we want picked up in the Abstract Syntax Tree

Todo
====

- modify codetalker to allow for streamed input

