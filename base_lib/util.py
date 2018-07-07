#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/7/5 10:39  
# @Author   : guo qun
# @FileName : util.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
from ast import literal_eval
import json


def parse_string_value(str_value):
    """
     parse string to python data structure if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         '{"a": 1}' => {"a": 1}
    """
    try:
        return literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        return str_value


def dict2json(dict_data):
    """
    将字典dumps为json对象
    :param dict_data:
    :return:
    """
    try:
        return json.dumps(dict_data)
    except IOError as err:
        raise IOError, err
