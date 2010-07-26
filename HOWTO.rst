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

 - STRING # normal " string
 - SSTRING # single-quoted ' string
 - TSTRING # triple-quoted ''' or """ pythonic string
 - CCOMMENT # c-style comment /** \**/ //
 - PYCOMMENT # python-style comment
 - NUMBER # an integer or float
 - INT # an integer
 - HEX # an 0xabc012 hex number.
 - ID # usually [a-zA-Z\_][a-zA-Z_0-9]*
 - ANY # matches any single char

- CharToken

 - also c-optimized; matches 'one of the specified characters'.
 - example: SYMBOLS

- StringToken

 - matches 'one of the specified strings'

- IdToken

 - matches 'one of the specified strings' *followed by a non-id character*
 - example: RESERVED_WORDS

- IIdToken

 - same as IdToken, but caseInsensitive

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
    - ``(nested, (tuples, are), collapsed)``
    - ``star(zero, or_more)``
    - ``plus(one, or_more)``
    - ``_or(one, of, these)``
    - ``_not(this, stuff)`` # checks the content, and if it *does not* match,
      consumes **a single** token.
    - ``TOKEN_NAME``

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

    match the first element of atype [becomes None if there are no elements
    matching atype]

:[atype]: match all elements of atype [becomes a list]
:[atype, anothertype]:

    match all elements of the contained types [becomes a list]

Complex
+++++++

The complex definition is a dictionary, where the ``type`` parameter follows
the *simple* definition above.

:type: atype | [atype] | [atype, anothertype]
:single: (bool) only use if you want to override the normal inference.
:start: (int) used for slicing (default: 0)
:end: (int) also for slicing (default: 0 [means no limit])
:step: (int) (default: 1)

As you can see, if you don't need to slice or override the "single" aspect,
you can just use the simple spec.

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

    grammar = Grammar(start, tokens, idchars='', indent=False, ignore=[], ast_tokens=[])

:start: the start rule
:tokens: a list of tokens to use
:idchars:

    extra characters you want to be considered ID-like (e.g. '$' for
    javascript, PHP)

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

    t = Translator(grammar, bar=0)

    @t.translates(ast.Foo)
    def deal_with_foo(node, scope):
        ...

    @t.translates(ast.Bar)
    def deal_with_bar(node, scope):
        ...

Within a ``deal_with_baz`` function, if you want to translate a child node,
call ``t.translate(node.somechild, scope)`` -- it will deal with that node in
the way you'd expect.

The ``scope`` variable that you saw me passing around is an object
that is really useful if you need to maintain any kind of state while
translating (local variables, etc.). To "turn on" scope usage, pass some
keyword arguments to the translator, which will populate the default
attributes of the scope. example:

.. code-block:: python

    t = Translator(grammar, variables={}, call_stack=[])

The ``scope`` object that gets passed around will then have the attributes
"variables" and "call_stack". For a good example of using the translation
scope, look at `CleverCSS2 <http://jaredforsyth.com/projects/clevercss2/>`_.
*If you don't "turn on" the scope, it doesn't get passed around -- your
translating functions should only take one argument.*

Once you've populated your translator, you can call ``t.from_string(text)`` to
first turn the ``text`` into an AST, and then translate the AST.

Here's a really simple example of a translator function (taken from the `json
grammar
<http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py#L39>`_):

.. code-block:: python

    @JSON.translates(ast.List)
    def t_list(node):
        return list(JSON.translate(value) for value in node.values)

Now you're ready to look at the examples:

- `JSON
  <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/json.py>`_
- `math
  <http://github.com/jabapyth/codetalker/blob/master/codetalker/contrib/math.py>`_
- `CleverCSS2
  <http://github.com/jabapyth/clevercss2/blob/master/clevercss/grammar.py>`_
- `python-css <http://github.com/jabapyth/css/blob/master/css/grammar.py>`_

If you have any suggestion as to how to improve this document, feel free to
let me know at jared@jaredforsyth.com

