#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/7/5 10:39  
# @Author   : guo qun
# @FileName : util.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
from _ast import Str, Num, Tuple, List, Dict, Name, BinOp, Add, Sub, Expression, PyCF_ONLY_AST
import json


def parse(source, filename='<unknown>', mode='exec'):
    """
    Parse the source into an AST node.
    Equivalent to compile(source, filename, mode, PyCF_ONLY_AST).
    """
    return compile(source, filename, str(mode), PyCF_ONLY_AST)


def unicode_literal_eval(node_or_string):
    """
    handle unicode object if the version of python is 2 -- by guo qun
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None.
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, basestring):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body

    def _convert(node):
        if isinstance(node, Str):
            return node.s
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v
                        in zip(node.keys, node.values))
        elif isinstance(node, Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif not (not isinstance(node, BinOp)
                  or not isinstance(node.op, (Add, Sub))
                  or not isinstance(node.right, Num)
                  or not isinstance(node.right.n, complex)
                  or not isinstance(node.left, Num)
                  or not isinstance(node.left.n, (int, long, float))):
            left = node.left.n
            right = node.right.n
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
        raise ValueError('malformed string')

    return _convert(node_or_string)


def eval_string_value(_value):
    """
     parse string to python data structure if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         '{"a": 1}' => {"a": 1}
    """
    try:
        return unicode_literal_eval(_value)
        # return literal_eval(_value)
    except Expression:
        raise Expression(_value)
    except SyntaxError:
        raise SyntaxError(_value)


def dict2json(dict_data):
    """
    将字典dumps为json对象
    :param dict_data:
    :return:
    """
    try:
        return json.dumps(dict_data)
    except IOError as err:
        raise IOError(err)
