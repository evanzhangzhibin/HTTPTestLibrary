#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/6/14 17:11
# @Author   : guo qun
# @FileName : HTTPTestKeywords.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
from HTTPTestLibrary.base_lib.util import eval_string_value
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
        http_session_cli = HttpSession()
        method = method.upper()
        # todo Robot里面传过来的值, 有部分要进行eval转换才能用
        if 'params' in kwargs:
            kwargs['params'] = eval_string_value(kwargs['params'])
        if 'data' in kwargs:
            kwargs['data'] = eval_string_value(kwargs['data'])
        if 'headers' in kwargs:
            kwargs['headers'] = eval_string_value(kwargs['headers'])
        if 'timeout' in kwargs:
            kwargs['timeout'] = eval_string_value(kwargs['timeout'])
        if url.startswith('https'):
            logger.info('===========>按照HTTPS   来处理!')
            actual_data, actual_type = do_https(http_session_cli, url, method, **kwargs)
        elif url.startswith('http'):
            logger.info('===========>按照HTTP  来处理!')
            actual_data, actual_type = do_http(http_session_cli, url, method, **kwargs)
        else:
            logger.error("请检查URL输入是否正确!")
            raise AssertionError

        _expect_data_type = expect_data_type.lower()
        if actual_type != _expect_data_type:
            logger.error(
                "实际响应体数据类型与期望响应体数据类型不一致! <actual>: {A}, <expect>: {E}".format(A=actual_type, E=_expect_data_type))
            raise AssertionError
        elif actual_type == _expect_data_type:
            # todo 执行响应体比较
            _expect_data = eval_string_value(expect_data)
            # TODO 相应返回的结果要不要转换为Unicode, 服务端的输入是不可靠的
            # _actual_data = parse_string_value(actual_data)
            if expect_data_type == "json":
                logger.info(_expect_data)
                # logger.info(_actual_data)
                print("raw_expect==> {}".format(expect_data))
                print("expect==> {}".format(_expect_data))
                print("raw_actual==> {}".format(actual_data))
                # print("actual==> {}".format(_actual_data))
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
    test_url = 'http://localhost:8001/api/v1/fakerfactory'
    test_method = 'get'
    test_params = '{"number": 1, "columns": "name,age,job"}'
    # test_headers = '{"Content-type": "application/json"}'
    expect_data = '{"data":{"count":1,"records":[{"age":"12","job":"渔业实验人员","name":"莫韶丽"}]},"status":{"code":"0","status":"ok"}}'
    expect_data_type = 'json'
    test_kw = HTTPTestKeywords()
    test_kw.do_test(test_method, test_url, expect_data, expect_data_type, params=test_params)
