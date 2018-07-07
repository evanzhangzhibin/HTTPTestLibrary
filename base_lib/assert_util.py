#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/7/7 18:56
# @Author   : guo qun
# @FileName : assert_util.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
from robot.api import logger
from HTTPTestLibrary.base_lib.json_util import structure_flow


def json_assert(a_json, e_json):
    """
    JSON数据比较断言
    :param a_json: 实际的json数据
    :param e_json: 期望的json数据
    :return:
    """
    error_count = 0
    # 转为方便比较的数据结构
    a_flow = structure_flow(a_json)
    e_flow = structure_flow(e_json)

    if sorted(a_flow.keys()) == sorted(e_flow.keys()):
        for k, v in iter(e_flow.items()):
            # 若value为  "{IGNORE}"  则忽略比对
            if v == '{IGNORE}':
                continue
            if a_flow[k] != v:
                logger.error("[!] RESPONSE-JSON==> [{K}]的**VALUE**不同: \n <actual>: {A} \n <expect>: {E}".format(K=k, A=a_flow[k], E=v))
    else:
        logger.error("[!] RESPONSE-JSON==> **KEY**不同: \n <actual>: {A} \n <expect>: {E}".format(A=a_flow.keys(), E=e_flow.keys()))



