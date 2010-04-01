CodeTalker
==========

A python library for parsing, prettifying, and even translating code.

Here's how simple it is::

    import codetalker
    from codetalker.bnf import c
    text = open('myfile.c').read()
    root = codetalker.parse(text, c)
    print root ## this print your code back verbatim

    # say you want to remove all whitespace
    # which isn't actually great -- it will turn "int foo" into "intfoo"
    # -- see examples/minify.py for a smart way to remove whitespace

    whitespace = root.find('whites')
    for node in whitespace:
        node.remove()
    print root

    # or just look at the comments
    comments = root.find('comment')
    for node in comments:
        print node

Features
--------

- parsing is entirely driven by modular grammers in BNF
- modular structure; can accomodate many different formats of BNF
- C parsing (C BNF file included)
- JSON parsing, proof of concept (really small grammar)

Todo
----

- javascript parsing
- python parsing
- build a c to python translator using codetalker

Examples
--------

I currently have one working and one non-working example ;)

To prettyfy some C code, type::

    python examples/prettyc.py test/c/hanoi.c

To parse some json (and return a python object) take a look at
examples/json.py

Or if you want pretty json, try to following::
    
    python examples/prettyjson.py test/json/json.json

