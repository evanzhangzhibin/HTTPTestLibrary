#!/usr/bin/env python
# coding: utf-8
# author: yjiang

from __future__ import unicode_literals
import time
from HTTPTestLibrary.json_generator import structure_flow
from collections import Counter
from collections import defaultdict
import json


def run_auto(http_cli, param, test_url, method, headers):
    resp = http_cli.request(method=method, url=test_url, data=json.dumps(param), headers=headers)
    assert resp.status_code == 200
    try:
        json_data = resp.json()

        return json_data
    except Exception as json_err:

        print json_err
        return ''


def analyze_expectation(http_cli, param, test_url, method, headers, count=10):
    """

    :param http_cli:
    :param param:
    :param test_url:
    :param method:
    :param headers:
    :param count: response count
    :return:
    """

    expectation = []
    for i in range(count):
        time.sleep(1)
        json_data = run_auto(http_cli, param, test_url, method, headers)
        assert isinstance(json_data, dict)
        expectation.append(structure_flow(json_data))  #
    # get all key
    allkey = [allkey for once in expectation for allkey in once.keys()]

    first_statistical = dict(Counter(allkey))
    # analyze all  response and get same key
    samekey = [key for key, value in first_statistical.iteritems() if value == len(expectation)]

    # get value if value is list ,to change str before sorted
    compare = defaultdict(list)
    for key in samekey:
        for once in expectation:
            allvalue = once[key]
            if isinstance(once[key], list):
                allvalue = str(sorted(once[key]))
            compare[key].append(allvalue)

    # get same value key and different value key
    # samevaluekey = [key for key,value in compare.iteritems() if len(set(value)) ==1 ]
    diffvaluekey = [key for key, value in compare.iteritems() if len(set(value)) != 1]

    original_json = json_data.copy()
    # get display response and tag different value
    display_json = json_data.copy()
    for diffkey in diffvaluekey:
        for key in diffkey.split('.')[:-1]:
            display_json = display_json[key]
        display_json[diffkey.split('.')[-1]] = '{0},{1}'.format(display_json[diffkey.split('.')[-1]],
                                                                '[change value,not check]')

    expectation_result = expectation[-1]

    # del diff key from "once_expectation"
    [expectation_result.pop(key) for key in diffvaluekey]

    # return  original response and expect result
    return original_json, display_json, expectation_result, diffvaluekey
