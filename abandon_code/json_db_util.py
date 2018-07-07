#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/6/12 14:12  
# @Author   : guo qun
# @FileName : DbUtil.py
# @Project  : Demo

from __future__ import unicode_literals

from abandon_code.config import DATABASES
from tinydb import TinyDB, Query


class JsonDB(object):
    def __init__(self, tb_name):
        """
        使用特殊的表名
        :param table_name:
        :return:
        """
        self.db = TinyDB(DATABASES['json_db']['NAME'])
        self.Q = Query()
        self.tb = self.db.table(tb_name)

    def insert(self, one_json):
        """
        插入单个json数据
        :param one_json:
        :return:
        """
        try:
            self.db.insert(one_json)
        except Exception as err:
            print "无法插入json数据: ", one_json
            raise err

    def insert_multiple(self, list_of_json):
        """
        插入一组json数据
        :param list_of_json:
        :return:
        """
        try:
            self.db.insert_multiple(list_of_json)
        except Exception as err:
            print "无法批量插入json数据: ", list_of_json
            raise err


def judge_expect_exist(jd_obj, query_json):
    """
    判断期望json数据是否已经入库
    :param jd_obj json数据库对象
    :param query_json:
    :return:
    """
    q_obj = jd_obj.Q
    query_res = jd_obj.tb.search((q_obj.headers == query_json['headers'])
                                 & (q_obj.param == query_json['payload'])
                                 & (q_obj.test_url == query_json['url'])
                                 & (q_obj.method == query_json['method']))
    if query_res:
        return True
    else:
        return False


def query_by_cond(jd_obj, query_json):
    """
    根据查询条件获取期望结果
    :param jd_obj:
    :param query_json:
    :return:
    """
    q_obj = jd_obj.Q
    query_res = jd_obj.tb.search((q_obj.headers == query_json['headers'])
                                 & (q_obj.param == query_json['payload'])
                                 & (q_obj.test_url == query_json['url'])
                                 & (q_obj.method == query_json['method']))

    if query_res:
        if len(query_res) == 1:
            expect_json = {
                "expectation_result": query_res[0]["expectation_result"],
                "diffvaluekey": query_res[0]["diffvaluekey"]
            }
            return True, expect_json, 'ok'
        else:
            return False, {}, '查询条件的期望结果不唯一'
    else:
        return False, {}, '没有期望结果'


def run():
    json_data = {'headers': {'Content-type': 'application/json'},
                 'payload': {'ifcontains': '0', 'authcode': '', 'entityids': ['11120'],
                             'filters': [{'item': 'level', 'value': ['402003']}], 'items': ['level']},
                 'display_json': {u'status': u'200', u'sender': u'CommonChoose', u'level': 0, u'areacode': u'320000',
                                  u'i3': 0, u'i2': 0, u'fromareacode': u'320000', u'i4': 0, u'i1': 0,
                                  u'noid': '90911682-7ce2-4822-977d-8be4b64efa14,[change value,not check]',
                                  u'receiver': u'restJoin', u'msg': u'\u5904\u7406\u6210\u529f',
                                  u'counts': {u'level': [{u'count': u'1', u'id': u'402003', u'label': u''}]},
                                  u'createTime': '1528785213,[change value,not check]',
                                  u'msgcreatetime': '1528785213369,[change value,not check]'},
                 'expectation_result': {u'status': u'200', u'sender': u'CommonChoose', u'counts.level.id': u'402003',
                                        u'level': 0, u'areacode': u'320000', u'i3': 0, u'i2': 0,
                                        u'fromareacode': u'320000', u'i4': 0, u'i1': 0, u'counts.level.count': u'1',
                                        u'counts.level.label': u'', u'receiver': u'restJoin',
                                        u'msg': u'\u5904\u7406\u6210\u529f'},
                 'original_json': {u'status': u'200', u'sender': u'CommonChoose', u'level': 0, u'areacode': u'320000',
                                   u'i3': 0, u'i2': 0, u'fromareacode': u'320000', u'i4': 0, u'i1': 0,
                                   u'noid': u'90911682-7ce2-4822-977d-8be4b64efa14', u'receiver': u'restJoin',
                                   u'msg': u'\u5904\u7406\u6210\u529f',
                                   u'counts': {u'level': [{u'count': u'1', u'id': u'402003', u'label': u''}]},
                                   u'createTime': 1528785213, u'msgcreatetime': 1528785213369L}, 'method': 'post',
                 'url': 'http://172.16.118.28:8090/lokiRest/lokiRest/zdr/commonchoose/count',
                 'diffvaluekey': [u'msgcreatetime', u'noid', u'createTime']}
    jd = JsonDB('demo')
    print judge_expect_exist(jd, json_data)


if __name__ == '__main__':
    run()
