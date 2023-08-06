#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'gpy'

import json
from urllib.parse import urlparse

import requests

from apf_ci.util.log_utils import logger
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.uc_sdk.nd_uc_new import NdUc, UcEnv
from apf_ci.util.content_service_config import ContentServiceConfig


def gen_mac_authorization_v11(cs_config, request_url, request_method):
    return gen_mac_authorization(cs_config, request_url, request_method, '1.1')


def gen_mac_authorization_v9(cs_config, request_url, request_method):
    return gen_mac_authorization(cs_config, request_url, request_method, '0.93')


def gen_mac_authorization(cs_config, request_url, request_method, uc_version):
    uc_env = UcEnv.ol
    if cs_config.host.find("sdpcs.beta.web.sdp.101.com") >= 0 or cs_config.host.find("betacs.101.com") >= 0:
        uc_env = UcEnv.pre
    elif cs_config.host.find("awscs.101.com") >= 0:
        uc_env = UcEnv.awsca

    #username = "10005015"
    #password = "abc123456!"

    username = "10009560"
    password = "apf123456!"
    nd_uc = NdUc(env=uc_env, uc_version=uc_version)
    nd_uc.set_login_info(username, password, "nd")

    request_uri = urlparse(request_url)
    mac_tocken = nd_uc.get_Authorization(request_uri.path, request_method, request_uri.netloc)
    return mac_tocken


def get_uc_token(cs_config):
    """
    获取UC token。根据config中的host,取不同环境下的token
    :param cs_config:
    :return:
    """
    # 获取access_token
    password = "80fba977d063a6f7262a8a9c95f61140"
    #password = 'f004df5e70ebb3ad432a6c43cbbdb830'
    # WarProperties
    properties = {}
    if cs_config.host.find("sdpcs.beta.web.sdp.101.com") >= 0 or cs_config.host.find("betacs.101.com") >= 0:
        properties["waf.uc.uri"] = "https://ucbetapi.101.com/v0.93/"
    elif cs_config.host.find("awscs.101.com") >= 0:
        properties["waf.uc.uri"] = "https://awsuc.101.com/v0.93/"
        password = "d4eda3a8a20030dbae6ee723a1bb7444"
    elif cs_config.host.find("cs-awsca.101.com") >= 0:
        properties["waf.uc.uri"] = "https://uc-awsca.101.com/v0.93/"
    else:
        properties["waf.uc.uri"] = "https://aqapi.101.com/v0.93/"
    token_uri = properties["waf.uc.uri"] + "bearer_tokens"

    body_json = {
        "login_name": "10005015",
        "password": password
    }
    token_response = requests.post(token_uri, json=body_json)
    if token_response.status_code != 201:
        error_message = "token获取失败 url: %s, \nbody: %s" % (token_uri, body_json)
        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
    token_response = json.loads(token_response.text)
    access_token = token_response["access_token"]
    logger.debug(" 获取的token为: %s" % access_token)
    return access_token


if __name__ == "__main__":
    cs_model = ContentServiceConfig()
    cs_model.host = 'http://betacs.101.com/v0.1'
    cs_model.server_name = 'qa_content_biz_comp_mng'
    cs_model.session_id = 'bb932030--4467-95ab-19898db09f8f'
    cs_model.user_id = '100000101'
    test_request_url = 'http://widget-i18n-store.debug.web.nd/v0.1/widgets/language/app/query'
    test_request_method = 'POST'
    gen_mac_authorization_v11(cs_model, test_request_url, test_request_method)