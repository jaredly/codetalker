#!/usr/bin/env python

from something import star, _or
from tokens import NAME, NUMBER, STRING

import ast

def test(rule):
    rule | (or_test, ['if', or_test, 'else', test]) | lambdef
    rule.astName = 'IfExp'
    rule.astAttrs = {'test':'@or_test[0]', 'body':'@or_test[1]', 'orelse':'@or_test[2]'}

def or_test(rule):
    rule | (and_test, star('or', and_test))
    rule.attr_list('tests', and_test)

def and_test(rule):
    rule | (not_test, star('and', not_test))
    rule.astName = 'BoolOp'
    rule.astAttrs = {'op':'!And', 'values':'@not_test[]'}

def not_test(rule):
    rule | ('not', not_test) | comparison
    rule.astName = 'UnaryOp'
    rule.astAttrs = {'op':'!Not', 'operand':'@not_test'} # if no [], assume [0]

def comparison(rule):
    rule | (expr, star(comp_op, expr))
    rule.astName = 'Compare'
    rule.astAttrs = {'left':'@expr[0]', 'ops':'@comp_op[]', 'comparators':'@expr[1:]'}

def comp_op(rule):
    rule | _or(*'< > == >= <= <> != in'.split()) | ('not', 'in') | ('is', 'not') | 'is')

def binop(child_type):
    op_types = {
        '|': 'BitOr',
        '^': 'BitXor',
        '&': 'BitAnd',
        '<<': 'LShift',
        '>>': 'RShift',
        '+': 'Add',
        '-': 'Sub',
        '*': 'Mult',
        '/': 'Div',
        '%': 'Mod',
        '**': 'Pow',
        '//': 'FloorDiv'
    }
    def ast_node(tree, parent):
        ops = tree.get_children(child_type)
        num = 0
        pnode = ast.make_node('BinOp')
        pnode.op = ast.make_node(op_types[str(tree.children[1])])
        pnode.right = parent.conv_node(ops.pop(-1))
        anode = pnode
        while len(ops) > 1:
            num += 1
            nnode = ast.make_node('BinOp')
            nnode.op = ast.make_node(op_types[str(tree.children[num + 1])])
            nnode.right = parent.conv_node(ops.pop(-1))
            anode.left = nnode
            anode = nnode
        anode.left = parent.conv_node(ops[0])
        return pnode
    return ast_node

def expr(rule):
    rule | (xor_expr, star('|', xor_expr))
    rule.astGen = binop('xor_expr')

def xor_expr(rule):
    rule | (and_expr, star('^', and_expr))
    rule.astGen = binop('and_expr')

def and_expr(rule):
    rule | (shift_expr, star('&', shift_expr))
    rule.astGen = binop('shift_expr')

def shift_expr(rule):
    rule | (arith_expr, star(_or('<<', '>>'), arith_expr))
    rule.astGen = binop('shift_expr')

def arith_expr(rule):
    rule | (term, star(_or('+', '-'), term))
    rule.astGen = binop('term')

def term(rule):
    rule | (factor, star(_or('*', '//', '%', '/'), factor))
    rule.astGen = binop('factor')

def factor(rule):
    rule | (_or('+', '-', '~'), factor) | power
    rule.astName = 'UnaryOp'
    def gen(tree):
        name = {'+':'UAdd', '-':'USub', '~':'Invert'}[str(tree.children[0])]
        return ast.make_node(name)
    rule.astGen = gen

def power(rule):
    rule | (trailing, ['**', factor])
    rule.astName = 'BinOp'
    rule.astAttrs = {'left':'@trailing', 'op':'!Pow', 'right':'@factor'}

def trailing(rule):
    rule | (atom, star(trailer))

def atom(rule):
    rule | ('(', [_or(yield_expr, testlist_gexp)], ')')
    rule | ('[', [listmaker], ']')
    rule | ('{', [dictmaker], '}')
    rule | ('`', testlist1, '`')
    rule | NAME | NUMBER | STRING+

def commas(func):
    return star(',', func), [',']

def testlist_comp(rule):
    rule | (test, _or(comp_for, commas(test)))

def trailer(rule):
    rule | ('(', [arglist], ')') | ('[', subscriptlist, ']') | ('.', NAME)

def subscriptlist(rule):
    rule | (subscript, ) + commas(subscript)

def subscript(rule):
    rule | ([test], ':', [test], [sliceop]) | test

def sliceop(rule):
    rule | (':', [test])

def exprlist(rule):
    rule | (star_expr, commas(star_expr))

def testlist(rule):
    rule | (test, commas(test))

def dictorsetmaker(rule):
    rule | (test, ':', test, _or(comp_for, commas((test, ':', test)))) | (test, _or(comp_for, commas(test)))

# vim: et sw=4 sts=4
