#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import sys
import time
import hmac
import base64
import hmac
import datetime
from hashlib import md5, sha1
from  decimal import Decimal
from  decimal import getcontext
from urllib.parse import quote_plus

from apf_ci.util.mac_token_utils import get_uc_token
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.cs_sdk.extend_upload_data import ExtendUploadData
from apf_ci.util.cs_sdk.dentry import Dentry
from apf_ci.util.content_service_config import ContentServiceConfig


def get_cs_session(cs_config):
    """
    获取cs的session值
    :param cs_config: 访问cs的配置对象。内含的属性，参考content_service_config.py
    :return:session
    """
    param = {}
    param["path"] = "/" + cs_config.server_name + "/"
    param["uid"] = cs_config.user_id
    param["role"] = "admin"
    param["service_id"] = cs_config.session_id
    param["expires"] = 10 * 60

    # 获取token
    access_token = get_uc_token(cs_config)

    # 获取session
    session_url = cs_config.host + "/sessions"
    session_header = {
        "Content-Type": "application/json",
        "authorization": "Bearer " + access_token
    }
    for i in range(3):
        session_response = requests.post(session_url, headers=session_header, json=param)
        if session_response.status_code != 200:
            error_message = "第 %s 次 请求 %s 失败。status_code : %s" % (i + 1, session_url, session_response.status_code)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            logger.debug("请求参数为： %s" % param)
            if i == 2:
                sys.exit(1)
            time.sleep(0.5)
        else:
            break
    session_response_body = json.loads(session_response.text)
    return session_response_body.get("session", "")


def get_cs_token(cs_config, upload_path, req_path, req_method, date_gmt):
    # 上传策略，查看方式为公开，path为上传的文件路径
    policy = json.dumps({
                            'path': upload_path,
                            'uid': int(cs_config.user_id),
                            'role': 'admin',
                            'policyType': 'upload',
                            'scope': 1,
                        }, separators=(',', ':'))

    # base64后的策略，与java的有差异后面会多= 需要替换掉
    policy_str = bytes.decode(base64.urlsafe_b64encode(
        policy.encode())).replace('=', '')

    sign_source_str = "{}\n{}\n{}\n{}".format(
        date_gmt, req_path, req_method, policy)
    sign = hmac.new(cs_config.secret_key.encode(),
                    sign_source_str.encode(), sha1).digest()
    sign_str = bytes.decode(base64.urlsafe_b64encode(sign)).replace('=', '')
    token = '{}:{}:{}'.format(cs_config.server_name, cs_config.access_key, sign_str)
    return token, policy_str


def upload_file_to_cs(file_path, upload_cs_path, file_name, cs_config, old_file_path=None):
    flag = False
    if not os.path.exists(file_path):
        logger.debug("文件 %s 不存在，上传失败！")
        raise Exception()

    cs_path = "/" + cs_config.server_name + "/" + upload_cs_path
    # 防止部分外部传错误路径问题
    cs_path = cs_path.replace('//', '/')
    cs_file_path = cs_path + "/" + file_name
    cs_file_path = cs_file_path.replace('//', '/')
    logger.debug("推送文件 %s 到内容服务 %s" % (file_name, cs_path))
    req_url_path = '/v0.1/upload'
    #cs_upload_api = cs_config.host + "/upload?session=" + get_cs_session(cs_config)
    #date_gmt = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    #cs_token, policy_str = get_cs_token(cs_config, cs_file_path, req_url_path, 'POST', date_gmt)
    #
    #cs_upload_api = "%s/upload?token=%s&date=%s&policy=%s" % (
    #    cs_config.host, cs_token, quote_plus(date_gmt), policy_str)
    #logger.debug("[DEBUG] upload_file_to_cs请求： %s" % cs_upload_api)

    upload_data = ExtendUploadData()
    upload_data.file_path = cs_file_path
    upload_data.expire_days = cs_config.expireDays

    denrty = Dentry()
    denrty.path = cs_path
    denrty.name = file_name
    if old_file_path is not None:
        tmp_old_file_path = "/" + cs_config.server_name + "/" + old_file_path
        denrty.filePath = tmp_old_file_path.replace('//', '/')
    denrty.scope = cs_config.scope
    #denrty.cs_upload_api = cs_upload_api
    #denrty.cs_token = cs_token
    denrty.get_cs_token = get_cs_token
    denrty.cs_config = cs_config
    denrty.cs_file_path = cs_file_path
    denrty.req_url_path = req_url_path
    for i in range(3):
        upload_response = denrty.upload(cs_config, file_path, upload_data, upload_progress_call_back)
        if isinstance(upload_response, str):# 只有在参数错误等情况才会直接返回字符串
            error_message = "第 %s 次 请求 失败。失败原因 : %s" % (i + 1, upload_response)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            if i == 2:
                sys.exit(1)
            time.sleep(0.5)
        elif upload_response.status_code != 200:
            logger.debug('\n'.join(['%s:%s' % item for item in upload_response.__dict__.items()]))
            if '_content' in upload_response.__attrs__:
                logger.warning(json.loads(upload_response._content))
            if 'message' in upload_response.__attrs__:
                error_message = "第 %s 次 请求 %s 失败。失败原因 : %s" % (i + 1, cs_upload_api, upload_response.message)
                logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            if i == 2:
                sys.exit(1)
            time.sleep(0.5)
        else:
            flag = True
            break
    logger.debug("上传了 100 %")
    return flag

def upload_progress_call_back(totalBytesWritten, totalBytesExpectedToWrite):
    d_context = getcontext()
    d_context.prec = 4
    process = Decimal(totalBytesWritten) / Decimal(totalBytesExpectedToWrite) * 100
    logger.debug('上传了 %s' % process + '%')


def get_cs_config():

    cs_config = ContentServiceConfig()
    cs_config.host = 'http://cs.101.com/v0.1'
    cs_config.server_name = 'release_package_repository'
    cs_config.session_id = '9f2b2b8b-ec4e-4eb0-8896-018fb7d5b695'
    cs_config.user_id = '100000101'
    cs_config.access_key = '717Vqqr218Uh4i03MfqU'
    cs_config.secret_key = 'm9J1MJoznjzS26p6YC07pGgpjD1Bx45Z40KtO78O'
    return cs_config


def get_cs_config_beta():
    cs_config = ContentServiceConfig()
    cs_config.host = 'http://betacs.101.com/v0.1'
    cs_config.server_name = 'preproduction_content_biz_comp_m'
    cs_config.session_id = '56f971f4-eb01-45a7-a9cd-5c996860b334'
    cs_config.user_id = '100000101'
    cs_config.access_key = '8ggjO49B14VHmc5I942h'
    cs_config.secret_key = 'd7i4gNLH509onP636qS7MTwE88NUlUa7N009g0Kg'
    return cs_config


def get_cs_config_x_edu():
    cs_config = ContentServiceConfig()
    cs_config.host = 'http://sdpcs.xue.eduyun.cn/v0.1'
    cs_config.server_name = 'portal_android_grey_x'
    cs_config.session_id = '7da55aa5-e813-4f28-8a3e-f0162e7c4a2d'
    cs_config.user_id = '505459'
    cs_config.access_key = 'yS08LOv6EpbEPG3K'
    cs_config.secret_key = '7hOVx5UCCu9fgdw0Xq8RpFS3joh4EQr2'
    return cs_config

def get_cs_config_private():
    cs_config = ContentServiceConfig()
    cs_config.host = 'http://sdpcs.xue.eduyun.cn/v0.1'
    cs_config.server_name = 'portal_android_grey_x'
    cs_config.session_id = '7da55aa5-e813-4f28-8a3e-f0162e7c4a2d'
    cs_config.user_id = '505459'
    cs_config.access_key = 'yS08LOv6EpbEPG3K'
    cs_config.secret_key = '7hOVx5UCCu9fgdw0Xq8RpFS3joh4EQr2'
    return cs_config

if __name__ == "__main__":
    #run_down()

    #json_test = json.loads('''{"host_id":"cs.101.com","request_id":"0461039e-aba5-4d5d-a87d-d2c2c2c38506","server_time":"2021-01-18T19:40:50.129+0800","code":"CS/UPLOAD_TO_S3_FAILED","message":"[info=\'\xe6\x96\x87\xe4\xbb\xb6\xe4\xb8\x8a\xe4\xbc\xa0\xe5\x88\xb0S3\xe5\xa4\xb1\xe8\xb4\xa5\'] [uuid=184f8bc2-0203-4c60-96a1-fd8473a6589b]","detail":null,"cause":null}''')

    file_path = 'D:\\Downloads\\framework.zip'
    #file_path = 'F:\\workplace\\apf-ci\\13663591898_180525.jpg'
    upload_cs_path = '/dragon_test_flutter'
    file_name = 'framework.zip'
    #file_name = '13663591898_180525.jpg'
    cs_config = ContentServiceConfig()
    cs_config.host = 'http://betacs.101.com/v0.1'
    cs_config.server_name = 'qa_content_suc'
    cs_config.session_id = '4af9a97e-6381-42b1-9917-3fd4e42d3d93'
    cs_config.user_id = '100000101'
    cs_config.access_key = 'QJddkUVd2q9eGLTJ'
    cs_config.secret_key = '4S6f1F1aWm9ZJpBd520LrU2L993iI0PO'
    #cs_config = get_cs_config_beta()
    #cs_config = get_cs_config_beta()
    upload_file_to_cs(file_path, upload_cs_path, file_name, cs_config, '/dragon_test_flutter/framework.zip')


