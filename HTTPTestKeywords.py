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
        http_session_cli = HttpSession(url)
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

        if url.startswith("https"):
            actual_data, res_type = do_https(http_session_cli, url, method, **kwargs)
            actual_data = parse_string_value(actual_data)
        elif url.startswith('http'):
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
        # jsondb = JsonDB('demo')
        # query_json = {
        #     "url": url,
        #     "method": method,
        #     "headers": headers,
        #     "payload": payload,
        # }
        # todo 考虑如何变更期望结果
        # if judge_expect_exist(jsondb, query_json):  # 若已经存储期望结果则取出期望结果比对
        #     logger.info("已经存储期望结果, 使用jsondb比对")
        #     self.builtin.log("已经存储期望结果, 使用jsondb比对", 'INFO')
        #     query_status, expect_json, query_msg = query_by_cond(jsondb, query_json)
        #     if not query_status:
        #         logger.warn("根据查询条件没有获取无法获取对应的期望结果: condition==>{}".format(query_json))
        #         # self.builtin.log("根据查询条件没有获取无法获取对应的期望结果: condition==>{}".format(query_json), "ERROR")
        #     else:
        #         if query_msg == 'ok':
        #             assert_result(reality_result, expect_json["expectation_result"], expect_json["diffvaluekey"], mode='eq')
        #             logger.info("测试通过")
        #             # self.builtin.log("测试通过", "INFO")
        #         else:
        #             logger.error(query_msg)
        #             # self.builtin.log(query_msg, 'ERROR')
        # else:  # 若无期望结果则生成期望结果, 存储入库, 并执行比对
        #     logger.info("第一次生成期望结果")
        #     # self.builtin.log("第一次生成期望结果", "INFO")
        #     original_json, display_json, expectation_result, diffvaluekey = analyze_expectation(http_session_cli, payload,
        #                                                                                         url, method, headers,
        #                                                                                         count=3)
        #     expect_json = {
        #         "url": url,
        #         "method": method,
        #         "headers": headers,
        #         "payload": payload,
        #         "original_json": original_json,
        #         "display_json": display_json,
        #         "expectation_result": expectation_result,
        #         "diffvaluekey": diffvaluekey
        #     }
        #     jsondb.tb.insert(expect_json)
        #     assert_result(reality_result, expectation_result, diffvaluekey, mode='eq')
        #     logger.info("测试通过")
        #     self.builtin.log("测试通过", "INFO")


        # def debug(method, url, payload, headers):
        #     jsondb = JsonDB('demo')
        #     headers = literal_eval(headers)
        #     payload = literal_eval(payload)
        #     # query_json = {
        #     #     "url": url,
        #     #     "method": method,
        #     #     "headers": headers,
        #     #     "payload": payload
        #     # }
        #
        #     query_json = {
        #         "url": "http://172.16.118.28:8090/lokiRest/zdr/commonchoose/keyword",
        #         "method": "post",
        #         "headers": {'Content-type': 'application/json'},
        #         "payload": {"authcode": "","keywords": [{"regex": "18805103311","items": ["pvalue"]}]}
        #     }
        #
        #     print judge_expect_exist(jsondb, query_json)


if __name__ == '__main__':
    #     url = "http://172.16.118.28:8090/lokiRest/zdr/commonchoose/keyword"
    #     method = "post"
    #     headers = "{'Content-type': 'application/json'}"
    #     payload = '''{"authcode": "","keywords": [{"regex": "18805103311","items": ["pvalue"]}]}'''
    #     debug(method, url, payload, headers)
    # base_url = "http://172.16.118.28:8090/lokiRest/lokiRest/zdr/commonchoose/count"
    test_payload = '''{
        "authcode": "",
        "entityids": ["11120"],
        "filters": [
            {
                "item": "level",
                "value": ["402003"]
            },
        ],
        "items": ["level"],
        "ifcontains": "0"
    }'''
    test_url = "http://172.16.118.28:8090/lokiRest/lokiRest/zdr/commonchoose/count"
    test_method = 'post'
    test_headers = "{'Content-type': 'application/json'}"
    test_expect_data = "{'status': '200', 'sender': 'CommonChoose', 'level': 0, 'areacode': '320000', 'i3': 0, " \
                       "'i2': 0, 'fromareacode': '320000', 'i4': 0, 'i1': 0, 'noid': " \
                       "'3fdab37c-50b3-4afe-8a6e-32dafe22d5b4', 'receiver': 'restJoin', 'msg': '处理成功', 'counts': {" \
                       "'level': [{'count': '1', 'id': '402003', 'label': ''}]}, 'createTime': 1530753579, " \
                       "'msgcreatetime': 1530753579555} "
    test_expect_data_type = "json"
    h = HTTPTestKeywords()
    h.do_test(method=test_method, url=test_url, expect_data=test_expect_data, expect_data_type=test_expect_data_type,
              headers=test_headers, data=test_payload)


    # json_data =   {u'status': u'200', u'sender': u'CommonChoose', u'level': 0, u'areacode': u'320000', u'i3': 0, u'i2': 0, u'fromareacode': u'320000', u'i4': 0, u'i1': 0, u'noid': u'fcac6ed3-7ade-485b-be9b-b4dff72f3758', u'receiver': u'restJoin', u'msg': u'\u5904\u7406\u6210\u529f', u'counts': {u'level': [{u'count': u'1', u'id': u'402003', u'label': u''}]}, u'createTime': 1528706469, u'msgcreatetime': 1528706469145L}
    # expectation_result =  {u'status': u'200', u'sender': u'CommonChoose', u'counts.level.id': u'402003', u'level': 0, u'areacode': u'320000', u'i3': 0, u'i2': 0, u'fromareacode': u'320000', u'i4': 0, u'i1': 0, u'counts.level.count': u'1', u'counts.level.label': u'', u'receiver': u'restJoin', u'msg': u'\u5904\u7406\u6210\u529f'}
    # diffvaluekey = [u'msgcreatetime', u'noid', u'createTime']
    # assert reality result with  expectation_result
