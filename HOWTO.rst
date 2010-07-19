The Only CodeTalker Introduction You'll Ever Need
=================================================

Or at least that's the idea. I tried to design CodeTalker such that you don't
need to pore over pages of API docs... This document + the example contrib parsers
provided should be enough (let me know if they aren't).

Defining a Grammar
------------------

Specifying Tokens
*****************

- CTokens (built-in, c optimized)

 - STRING
 - SSTRING
 - TSTRING
 - CCOMMENT
 - PYCOMMENT
 - NUMBER
 - INT
 - ID

- CharToken

 - also c-optimized; matches 'one of the specified characters'.
 - example: SYMBOLS

- StringToken

 - matches 'one of the specified strings'
 - example: RESERVED_WORDS

- ReToken

 - this is the most flexible, but also the slowest. Use only when needed
   (uses the python ``re`` module to match tokens)

Defining Rules
**************

.. code-block:: python

    def rulename(rule):
        rule | option1 | option2
        rule | option3

:option:

    ``child`` or ``(child, child, ...)``

:child: 

    - ``"string literal"``
    - ``[optional, children, ...]``
    - ``star(zero, or_more)``
    - ``plus(one, or_more)``
    - ``or_(one, of, these)``
    - ``TOKEN``

Abstract Syntax Tree Attributes
*******************************

By default, none of the rules you create will become nodes in the AST - that's
because you haven't defined what attributes such a node would have. Adding to
our generic rule, you specify an ``astAttrs`` attribute.

.. code-block:: python

    def rulename(rule):
        rule | option1 | option2
        rule.astAttrs = {
            "attr1": spec,
            "attr2": spec
        }

It's a dictionary where the *keys* are the attribute names that you want, and
the values are a specification of the value to be populated. The ``spec``
comes in two flavors -- simple or complex. As you'll see, the simple flavor is
just a shortcut, but makes the definition clearer & simpler in many cases. (in
the following examples, ``atype`` is the name of a rule or token).

Simple
++++++

:atype:

    match the first element of atype [raises an error if there are no elements
    matching atype]

:[atype]: match all elements of atype [becomes a list]
:[atype, anothertype]:

    match all elements of the contained types [becomes a list]

Complex
+++++++

The complex definition is a dictionary, where the ``type`` parameter follows
the *simple* definition above.

:type: atype | [atype] | [atype, anothertype]
:start: (int) used for slicing (default: None)
:end: (int) also for slicing (default: None
:step: (int) (default: 1)

As you can see, if you don't need slicing, you can just use the simple spec.

And here's an example from a calculator:

.. code-block:: python

    def addsub_expression(rule):
        rule | (value, star(_or('+', '-'), value))
        rule.astAttrs = {
            'left': value,      # matches only the first 'value' node
            'ops': [OP],        # matches all the operator tokens ('+' or '-')
            'values': {
                'type': [value],
                'start': 1
            }                   # matches all but the first value. 
    
AST Name
********

The (class)name of the resulting AST node defaults to the function name,
converted to TitleCase (e.g. some_rule => SomeRule). You can customize this
name by setting the ``astName`` attribute of the *function*. example:

.. code-block:: python

    def foo(rule):
        # stuff
    foo.astName = 'FooBar'

Actually Making the Grammar
***************************

.. code-block:: python

    grammar = Grammar(start, tokens, indent=False, ignore=[], ast_tokens=[])

:start: the start rule
:tokens: a list of tokens to use
:indent:

    (bool) if true, insert INDENT and DEDENT tokens in the appropriate places
    (necessary if you want to parse indentation-based languages like python)

:ignore:

    list of tokens to ignore while parsing (usually [WHITE], or [WHITE,
    NEWLINE])

:ast_tokens:

    list of tokens to *not* ignore while constructing the AST (often [NUMBER,
    ID])

Translating
-----------

This is the final step - doing something with the AST you just made. The ast
classes are auto generated, and stored in grammar.ast_classes. I generally put
``ast = grammar.ast_classes`` at the start of my translator.

.. note::

    AST Nodes have only the attributes you defined for them, populated with
    the parse tree.

    Tokens have three attributes:

    :value: (str)
    :lineno: (int)
    :charno: (int)

A translator function can return anything you like...

A Translator is really just a pretty transparent shortcut for taking an AST
and turning it into what you really wanted in the first place.

Instead of writing:

.. code-block:: python

    def deal_with_ast(node):
        if isinstance(node, ast.Foo):
            return deal_with_foo(node)
        elif isinstance(node, ast.Bar):
            return deal_with_bar(node)
        ...

You get:

.. code-block:: python

    t = Translator(grammar)

    @t.translates(ast.Foo)
    def deal_with_foo(node, scope):
        ...

    @t.translates(ast.Bar)
    def deal_with_bar(node, scope):
        ...

Within a ``deal_with_baz`` function, if you want to translate a child node,
call ``t.translate(node.somechild, scope)`` -- it will deal with that node in
the way you'd expect.

The ``scope`` variable that you saw me passing around is an anonymous object
that is really useful if you need to maintain any kind of state while
translating (local variables, etc.).

Once you've populated your translator, you can call ``t.from_string(text,
**args)`` to first turn the ``text`` into an AST, and then translate the AST.

``args`` is a dictionary used to prepopulate the attributes of ``scope``.

Here's a really simple example of a translator function (taken from the `json
grammar
<http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py#L39>`_):

.. code-block:: python

    @JSON.translates(ast.List)
    def t_list(node, scope):
        return list(JSON.translate(value, scope) for value in node.values)

Now you're ready to look at the examples:

- `JSON
  <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py>`_
- `math
  <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/math.py>`_

