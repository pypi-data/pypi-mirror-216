#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

from apf_ci.util.mac_token_utils import *


def get_data(url, errorExit=True):
    """
    通过URL获取相关内容
    :param url:
    :return:
    """
    headers = {}
    return get_data_with_headers(url, headers, errorExit)


def get_data_with_env_headers(url, env, errorExit=True):
    """
    通过URL获取相关内容
    :param url:
    :return:
    """
    headers = {'Dispatch-Environment': env}
    return get_data_with_headers(url, headers, errorExit)


def get_data_with_headers(url, headers, errorExit=True):
    """
    通过URL获取相关内容,支持传入header
    :param url:
    :return:
    """
    logger.debug(" URL(GET) %s " % url)
    r = None
    # 请求失败重连3次
    for i in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=300)
        except Exception:
            error_message = "获取 %s 超时300s,失败" % url
            if r and r.status_code:
                error_message = "获取 %s 超时300s,失败。status_code : %s" % (url, r.status_code)
            logger.error(LoggerErrorEnum.TIME_OUT, error_message)
            if i == 2:
                if errorExit:
                    sys.exit(1)
            else:
                time.sleep(0.5)
                continue
        if r.status_code != 200:
            if errorExit:
                log_error_message(url, r)
            if i == 2:
                if errorExit:
                    sys.exit(1)
            time.sleep(0.5)
        else:
            break
    data = r.content
    return json.loads(data.decode('utf-8'))


def post_for_array(url, request_body_array, is_print=True):
    """
    POST请求
    :param url:
    :param request_body_array: 请求体
    :param is_print: 是否打印响应结果
    :return:
    """
    resp = None
    logger.debug(' URL(POST): %s \nBODY: %s' % (url, request_body_array))
    for i in range(3):
        resp = requests.post(url, json=request_body_array, verify=False)
        if resp.status_code != 200:
            log_error_message(url, resp)
            if i == 2:
                sys.exit(1)
            time.sleep(0.5)
        else:
            break
    response_body = json.loads(resp.text)

    if is_print:
        logger.debug(' RESPONSE BODY: %s' % response_body)
    return response_body


def post_for_array_uc(url, request_body_array, cs_config, is_print=True):
    """
    POST请求
    :param url:
    :param request_body_array: 请求体
    :param is_print: 是否打印响应结果
    :return:
    """
    resp = None
    logger.debug(' URL(POST): %s \nBODY: %s' % (url, request_body_array))
    headers = {
        'Content-Type': "application/json",
    }
    if cs_config != None:
        mac_token = gen_mac_authorization_v9(cs_config, url, "POST")
        headers = {
            "Content-Type": "application/json",
            'Authorization': mac_token,
        }
    for i in range(3):
        resp = requests.post(url, json=request_body_array, headers=headers, verify=False)
        if resp.status_code != 200:
            log_error_message(url, resp)
            if i == 2:
                sys.exit(1)
            time.sleep(0.5)
        else:
            break
    response_body = json.loads(resp.text)

    if is_print:
        logger.debug(' RESPONSE BODY: %s' % response_body)
    return response_body


def log_error_message(req_url, resp):
    error_message = "请求 %s 失败。status_code : %s" % (req_url, resp.status_code)
    logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
    try:
        if hasattr(resp, 'content'):
            content = json.loads(resp.content)
            if content.__contains__('message'):
                logger.warning(content['message'])
    except Exception:
        logger.warning(resp)
        if hasattr(resp, 'content'):
            logger.warning(resp.content)


def search_job_by_text(search_text, search_info):
    result_info = '查找 %s 成功，对应job模板id为：%s ,对应 software_type 为 %s,对应 template_version 为 %s '
    # 预生产环境接口
    getJobTypeListUrl = 'http://jenkins-proxy.pre2.web.nd/v0.1/proxy/jobtype'
    getJobTypeTemplateContentUrlTemp = 'http://jenkins-proxy.pre2.web.nd/v0.1/proxy/jobtype/%s/templatecontent'
    # 生产环境接口
    #getJobTypeListUrl = 'http://jenkins-proxy.pre1.web.nd/v0.1/proxy/jobtype'
    #getJobTypeTemplateContentUrlTemp = 'http://jenkins-proxy.pre1.web.nd/v0.1/proxy/jobtype/%s/templatecontent'
    jobTypeList = get_data(getJobTypeListUrl)
    getJobTypeTemplateContentUrlHead = {}
    getJobTypeTemplateContentUrlHead['Content-Type'] = 'text/plain'
    getJobTypeTemplateContentUrlHead['Accept'] = 'application/xml'
    #print(jobTypeList)
    i = 0
    for item in jobTypeList:
        job_id = item["id"]
        software_type = item["software_type"]
        template_version = item["template_version"]
        getJobTypeTemplateContentUrl = getJobTypeTemplateContentUrlTemp % job_id
        #print(getJobTypeTemplateContentUrl)
        r = requests.get(getJobTypeTemplateContentUrl, headers=getJobTypeTemplateContentUrlHead, timeout=300)
        JobTypeTemplateContent = r.content.decode('utf-8')
        if search_text in JobTypeTemplateContent:
            i = i + 1
            print(result_info % (search_text, job_id, software_type, template_version))

    print('总共查到到 %s 个结果' % i)


if __name__ == "__main__":
    pass
    #search_text = 'jenkins-plugin-app-factory-react-build'
    #search_info = '含有构建离线H5轻应用插件 '
    #search_job_by_text(search_text, search_info)

    #url = 'https://lite-app-server.sdp.101.com/v0.1/app/jssdk'
    #body = {'package_name': 'com.nd.app.factory.ap1571192311096', 'version_code': '3074550', 'env_target': 'product',
    #        'type': 'android', 'update_time': 1571193047248, 'version': '1',
    #        'factory_id': '03daae91-1cdd-4efa-b778-18be3d10566a', 'label': 'lite1016', 'com_test_type': '',
    #        'rn_debug_mode': 'false', 'components': ['com.nd.android.smartcan:i-android-apf:3.1.0.3.release',
    #                                                 'com.nd.uc:thirdlogin:1.0.1.4.release',
    #                                                 'com.nd.android.sdp.social:module_audiorecorder:17.0.6.release',
    #                                                 'com.nd.sdp.android.common:search-widget:1.8.404.release',
    #                                                 'com.nd.sdp.android:appfactory-js-sdk:3.1.7.1.release',
    #                                                 'com.nd.sdp.android:react-wrapper:0.6.1',
    #                                                 'com.nd.sdp.uc:nducsdk:0.0.0.8.nducsdk.release'],
    #        'jssdks': {'MUIMultiPhotoJsSdk': '1.0', 'rnnews-jssdk': '1.0', 'rn-common': '1.0', 'ui-jssdk': '1.0',
    #                   'cs-jssdk': '1.0', 'imJsModuleProvider': '1.0', 'com#nd#social#im': '1.1',
    #                   'MUIAudioJsBridgeSdk': '1.0', 'imAppSettingFontSize': '1.0',
    #                   'com#nd#sdp#component#appfontcomponent': '1.1', 'uc-jssdk': '1.1', 'downloader-jssdk': '0.1',
    #                  R 'org-jssdk': '1.0', 'com#nd#sdp#component#voicetransform': '1.0'}}
    #post_for_array(url, body, True)

