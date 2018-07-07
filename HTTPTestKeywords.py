#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/6/14 17:11
# @Author   : guo qun
# @FileName : HTTPTestKeywords.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
from HTTPTestLibrary.base_lib.util import parse_string_value
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from HTTPTestLibrary.base_lib.http_client import HttpSession
from HTTPTestLibrary.base_lib.http_util import do_http, do_https

# from HTTPTestLibrary.assert_model import assert_result
# from HTTPTestLibrary.analyze_expect import analyze_expectation


class HTTPTestKeywords(object):
    """
    HTTP接口测试库
    """
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self.builtin = BuiltIn()

    def do_test(self, method, url, expect_data, expect_data_type, **kwargs):
        """
        执行测试, 自动比对期望结果
        """
        http_kwargs_key = ['params', 'data', 'headers', 'cookies', 'files', 'auth', 'timeout', 'allow_redirects',
                           'proxies', 'hooks', 'stream', 'verify', 'json', 'password', 'certificate']
        # bool_key_value = {'allow_redirects': [True, False], 'stream': [True, False], 'verify': [True, False]}
        for key in kwargs:
            if key not in http_kwargs_key:
                logger.error("传入的请求参数错误, 请检查: {K}={V}".format(K=key, V=kwargs[key]))
                raise KeyError
                # if key in bool_key_value and kwargs[key] not in bool_key_value[key]:
                #     logger.error("传入参数的值错误, 请检查: {K}={V}".format(K=key, V=kwargs[key]))
                #     raise ValueError
        logger.info('====raw kwargs ===>{}'.format(kwargs))
        http_session_cli = HttpSession()
        # todo Robot里面传过来的值, 有部分要进行eval转换才能用
        if 'params' in kwargs:
            kwargs['params'] = parse_string_value(kwargs[str('params')])
        if 'data' in kwargs:
            kwargs['data'] = parse_string_value(kwargs[str('data')])
        if 'headers' in kwargs:
            kwargs['headers'] = parse_string_value(kwargs[str('headers')])
        if 'timeout' in kwargs:
            kwargs['timeout'] = parse_string_value(kwargs[str('timeout')])
        expect_data_type = expect_data_type.lower()
        logger.info('====new kwargs ===>{}'.format(kwargs))
        if url.startswith("https"):
            logger.info("===========>按照HTTPS   来处理!")
            actual_data, res_type = do_https(http_session_cli, url, method, **kwargs)
            actual_data = parse_string_value(actual_data)
        elif url.startswith('http'):
            logger.info("===========>按照HTTP  来处理!")
            actual_data, res_type = do_http(http_session_cli, url, method, **kwargs)
            actual_data = parse_string_value(actual_data)
        else:
            logger.error("请检查URL输入是否正确!")
            raise AssertionError
        if res_type != expect_data_type:
            logger.error("实际响应体数据类型与期望响应体数据类型不一致! <actual>: {A}, <expect>: {E}".format(A=res_type, E=expect_data_type))
            raise AssertionError
        elif res_type == expect_data_type:
            # todo 执行响应体比较
            if expect_data_type == "json":
                expect_data = parse_string_value(expect_data)
                # json_assert(expect_data, actual_data)
            elif expect_data_type == "html":
                # html_assert(expect_data, actual_data)
                pass
            elif expect_data_type == "xml":
                # xml_assert(expect_data, actual_data)
                pass
            else:
                pass
        else:
            logger.error("未知错误! <actual>: {A}, <expect>: {E}".format(A=res_type, E=expect_data_type))
            raise AssertionError
        '''
        进行比对(注意字符编码的统一转换, 都转为unicode编码后比对):
        I. 先比对类型是否一致
        II. 再比对结果是否一致
            1. 若为JSON格式结果
                1) 期望结果全量比对
                    a. 比对所有的key以及key对应的value
                2) 期望结果定制比对
                    a. 比对所有的key
                    b. 忽略部分key对应的value
            json类型的返回结果，要注意数组对象的排序后再比较
            2. 若为XML或HTML格式的结果(同一层级节点的顺序没有什么影响, 对于内容的传递是一样的, 注意排序后比较)
                1) 期望结果全量比对
                    a. 比较所有node以及node的attribute和value
                2) 期望结果定制比对
                    a. 比较所有node以及node的attribute
                    b. 忽略部分node的value
        '''


if __name__ == '__main__':
    pass
