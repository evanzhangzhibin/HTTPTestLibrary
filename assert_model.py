#!/usr/bin/env python
# coding: utf-8
# author: yjiang
from __future__ import unicode_literals
from HTTPTestLibrary.json_generator import structure_flow


def assert_result(reality_result, expectation_result, diffvaluekey, mode='eq'):
    """
    :param reality_result:
    :param expectation_result:
    :param mode: assert mode
    :return:
    """

    reality_result = structure_flow(reality_result)

    assert str(sorted(reality_result.keys())) == str(sorted(expectation_result.keys() + diffvaluekey)), (
        "响应返回的键不同，返回数据与期望结果或多或少。\n 实际返回的键:{0}，\n 期望返回的键:{1}".format(sorted(reality_result.keys()),
                                                                    sorted(expectation_result.keys() + diffvaluekey)))

    for key, value in expectation_result.iteritems():
        assert reality_result[key] == value, (
            "响应返回{0}键的值不同，实际返回值：{1},期望返回值：{2}".format(key, reality_result[key], value))
