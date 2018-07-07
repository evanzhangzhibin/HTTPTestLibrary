#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/6/14 17:11  
# @Author   : guo qun
# @FileName : http_util.py
# @Project  : HTTPTestLibrary

from __future__ import unicode_literals
import OpenSSL
from robot.api import logger
from requests import HTTPError


def do_http(http_cli, test_url, method, **kwargs):
    """
    发起请求获取响应
    :param http_cli:
    :param test_url:
    :param method:
    :return:
    """

    try:
        resp = http_cli.request(method=method, url=test_url, **kwargs)
    except Exception as request_err:
        logger.error("执行请求错误, ERROR: {ERR}".format(ERR=request_err))
        raise HTTPError
    else:
        # todo 是否需要指定所有响应使用utf-8编码
        # resp.encoding = 'utf-8'
        return handle_response(resp)


def do_https(http_cli, test_url, method, **kwargs):
    """
    发起请求获取响应, HTTPS by 丁飞飞
    :param http_cli:
    :param test_url:
    :param method:
    :return:
    """
    if "certificate" in kwargs:
        if kwargs[str("certificate")].endswith(".p12") and "password" not in kwargs:
            logger.error("Need password for .p12 certificate.")
            raise HTTPError
        else:
            cert = p12_to_pem(kwargs[str("certificate")], kwargs[str("password")])
            kwargs["cert"] = cert
            kwargs.pop(str("password"))
            kwargs.pop(str("certificate"))
            kwargs['verify'] = False
            try:
                resp = http_cli.request(method=method, url=test_url, **kwargs)
            except Exception as request_err:
                logger.error("执行请求错误, ERROR: {ERR}".format(ERR=request_err))
                raise HTTPError
            else:
                return handle_response(resp)
    else:
        logger.error("No certificate file found for https request.")
        raise HTTPError



def p12_to_pem(cert_name, pwd="000000"):
    """
    Change the .p12 certificate to .pem file Writen by 丁飞飞
    :param cert_name: certificate file location
    :param pwd: password for certificate
    :return: .pem file
    """
    if cert_name.endswith('.p12'):
        pem_name = cert_name.replace('.p12', '.pem')
        with open(pem_name, "wb") as f_pem:
            p12file = cert_name
            p12 = OpenSSL.crypto.load_pkcs12(open(p12file, 'rb').read(), pwd)
            f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
            ca = p12.get_ca_certificates()
            if ca is not None:
                for cert in ca:
                    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        return pem_name
    else:
        return cert_name


def handle_response(resp_obj):
    """
    处理HTTP(S)响应
    :param resp_obj:
    :return:
    """
    http_code = resp_obj.status_code
    # todo 如果有重定向呢？这种情况不需要解析响应的, requests对除了HEAD以外的请求方式默认
    http_code_dict = {
        200: "请求成功, HTTP状态码为: {}",
        202: "请求已经进入后台排队, HTTP状态码为: {}",
        204: "请求数据删除成功, HTTP状态码为: {}",
        400: "请求错误, 请检查请求是否正确, HTTP状态码为: {}",
        406: "请求的格式不正确, 请检查请求是否正确, HTTP状态码为: {}",
        410: "请求的资源被永久删除, HTTP状态码为: {}",
        422: "请求在执行时发生验证错误, HTTP状态码为: {}",
        500: "服务器发生错误, HTTP状态码为: {}",
    }
    if str(http_code).startswith('20'):  # 根据HTTP状态不同打印不同的请求日志
        logger.info(http_code_dict[http_code].format(http_code))
    else:
        logger.error(http_code_dict[http_code].format(http_code))
        return "", 'error'
    try:
        json_data = resp_obj.json()
        return json_data, 'json'  # 获取json成功则返回json数据以及数据类型
    except Exception as get_json_err:
        resp_data = resp_obj.text
        logger.warn("响应体没有JSON对象: {}".format(get_json_err))
        return resp_data, 'text'
