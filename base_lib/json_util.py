#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/7/7 17:09
# @Author   : guo qun
# @FileName : PyCharm.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals


def json_generator(indict, key_value=None):
    """
    written by jiang yue
    :param indict:
    :param key_value:
    :return:
    """
    key_value = key_value[:] if key_value else []

    if isinstance(indict, dict):
        # print "indict===>", type(indict), indict
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield key_value + [key, '{}']
                else:
                    for d in json_generator(value, key_value + [key]):
                        yield d

            elif isinstance(value, list):
                if len(value) == 0:
                    yield key_value + [key, '[]']
                else:
                    for v in value:
                        for d in json_generator(v, key_value + [key]):
                            yield d

            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield key_value + [key, '()']
                else:
                    for v in value:
                        for d in json_generator(v, key_value + [key]):
                            yield d
            else:
                yield key_value + [key, value]

    else:
        if not key_value:
            yield indict
        else:
            yield key_value + [indict]


def structure_flow(json_gen_obj):
    """
    written by jiang yue
    :param json_gen_obj:
    :return:
    """
    structure = {}

    for i in json_generator(json_gen_obj):

        if '.'.join(i[:-1]) in structure.keys() and not isinstance(structure['.'.join(i[:-1])], list):
            structure['.'.join(i[:-1])] = [structure['.'.join(i[:-1])]]
            structure['.'.join(i[:-1])].append(i[-1])

        elif '.'.join(i[:-1]) in structure.keys() and isinstance(structure['.'.join(i[:-1])], list):
            structure['.'.join(i[:-1])].append(i[-1])

        else:
            structure['.'.join(i[:-1])] = i[-1]
    return structure
