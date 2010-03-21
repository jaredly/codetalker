CodeTalker
==========

A python library for parsing, prettifying, and even translating code.

Features
--------

- parsing is entirely driven by modular grammers in BNF
- modular structue; can accomodate many different formats of BNF
- C parsing (c BNF file included)

Todo
----

- get JSON parsing working again
- javascript parsing
- python parsing
- testing

Examples
--------

I currently have one working and one non-working example ;)

To prettyfy some C code, type::
    python examples/c.py test/hanoi.c

And the json parser (examples/json.py) is not working ATM (it was before, but
some recent radical changes broke it).
