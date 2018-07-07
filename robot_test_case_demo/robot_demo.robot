*** Settings ***
Library           HTTPTestLibrary

*** Test Cases ***
test1
    ${test_url}    Set variable    http://localhost:8001/api/v1/fakerfactory
    ${method}    Set variable    GET
    ${params}    Set variable    {"number": 1, "columns": "name,age,job"}
    # ${headers}    Set variable    {"Content-type": "application/json"}
    ${expect_data}    Set variable    {"msg": "处理成功"}
    ${expect_data_type}    Set variable    json
    Do Test    ${method}    ${test_url}    ${expect_data}    ${expect_data_type}    params=${params}
