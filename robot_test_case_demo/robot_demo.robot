*** Settings ***
Library           HTTPTestLibrary

*** Test Cases ***
test1
    ${test_url}    Set variable    http://localhost:8001/api/v1/fakerfactory
    ${method}    Set variable    GET
    ${params}    Set variable    {"number": 1, "columns": "name,age,job"}
    ${headers}    Set variable    {"Content-type": "application/json"}
    ${expect_data}    Set variable    {"data":{"count":1,"records":[{"age": 22,"job":"{IGNORE}","name":"{IGNORE}"}]},"status":{"code":"0","status":"ok"}}
    ${expect_data_type}    Set variable    json
    Do Test    ${method}    ${test_url}    ${expect_data}    ${expect_data_type}    params=${params}
