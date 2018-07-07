*** Settings ***
Library           HTTPTestLibrary

*** Test Cases ***
test1
    ${test_url}    Set variable    http://baike.baidu.com/api/openapi/BaikeLemmaCardApi
    ${method}    Set variable    GET
    ${params}    Set variable    {'scope': 103, 'format': 'json", 'appid': 379020, 'bk_key': '银魂', 'bk_length': 600}
    ${headers}    Set variable    {'Content-type': 'application/json'}
    ${expect_data}    Set variable    {'status': '200', 'sender': 'CommonChoose', 'level': 0, 'areacode': '320000', 'i3': 0, 'i2': 0, 'fromareacode': '320000', 'i4': 0, 'i1': 0, 'noid': '3fdab37c-50b3-4afe-8a6e-32dafe22d5b4', 'receiver': 'restJoin', 'msg': '处理成功', 'counts': {'level': [{'count': '1', 'id': '402003', 'label': ''}]}, 'createTime': 1530753579, 'msgcreatetime': 1530753579555}
    ${expect_data_type}    Set variable    json
    Do Test    ${method}    ${test_url}    ${expect_data}    ${expect_data_type}    params=${params}    headers=${headers}
