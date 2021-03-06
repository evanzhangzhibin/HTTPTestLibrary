*** Settings ***
Library           HTTPTestLibrary

*** Test Cases ***
test1
    ${test_url}    Set variable    http://localhost:8001/api/v1/fakerfactory
    ${method}    Set variable    GET
    ${params}    Set variable    {"number": 1, "columns": "name,age,job"}
    ${headers}    Set variable    {"Content-type": "application/json"}
    ${expect_data}    Set variable    {"data":{"count":1,"records":[{"age": "{IGNORE}","job":"{IGNORE}","name":"{IGNORE}"}]},"status":{"code":"0","status":"ok"}}
    ${expect_data_type}    Set variable    json
    ${temp_data}    Do Test    ${method}    ${test_url}    ${expect_data}    ${expect_data_type}    params=${params}
    ${status}    Json Value    ${temp_data}    status
    ${stssus}    Json Value    ${test_url}    status
