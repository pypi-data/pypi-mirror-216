#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app对比工具
"""

__author__ = '370418'

from apf_ci.util.upload_utils import *
from apf_ci.app_init.utils.build_config_utils import BuildConfig
from apf_ci.app_init.utils.variable_utils import Variable
from apf_ci.app_compare.build.app_compare_android import main as app_compare_android
from apf_ci.app_compare.build.app_compare_ios import main as app_compare_ios
from apf_ci.app_compare.build.app_compare_utils import save_and_upload, get_download_url

aapt_path = 'aapt'
#aapt_path = 'D://software//Java//Android//sdk_studio//build-tools//27.0.3//aapt.exe'



def main(args):
    #----  获取传入参数
    package_old = args.packageOld
    package_new = args.packageNew
    app_compare_id = args.appCompareId
    app_type = args.appType
    env_jenkins = args.envJenkins
    is_local = args.isLocal == 'true'

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        #----   初始化传入参数及路径
    # 针对 git  clone 需要空目录才能正常，日志文件生成延后到，clone步骤之后。这里日志比较少，直接输出到Console
    logger.delay_init(True)
    logger.info('开始生成app对比文件')

    #----   初始化传入参数及路径
    variable_dict = {}
    variable_dict['targetPath'] = target_path
    variable_dict['appCompareId'] = app_compare_id
    variable_dict['appType'] = app_type
    variable_dict['packageOld'] = package_old
    variable_dict['packageNew'] = package_new
    variable_dict['envJenkins'] = env_jenkins
    variable_dict['isLocal'] = is_local
    variable_dict['dataUrl'] = ""
    variable = Variable(target_path)
    variable.write_variable_json(variable_dict)

    build_config = BuildConfig(target_path)
    build_config_json_encrypt = build_config.get_build_config(env_jenkins, is_local)
    build_config_json = build_config.decrypy_build_config(build_config_json_encrypt)
    build_config.write_build_config(build_config_json_encrypt)

    data = {}
    if app_type.lower() == 'android':
        data = app_compare_android(variable_dict, build_config_json)
    elif app_type.lower() == 'ios':
        data = app_compare_ios(variable_dict, build_config_json)

    data_url = save_and_upload(target_path, build_config_json, app_compare_id, 'data.json', data)
    logger.info("app对比文件上传cs成功：" + data_url)
    summary_url = save_and_upload(target_path, build_config_json, app_compare_id, 'summary.json', data['summary'])
    logger.info("app对比概要文件上传cs成功：" + summary_url)
    download_url = get_download_url(build_config_json, data_url)
    logger.info("app对比报告地址：" + download_url)
    variable_dict['dataUrl'] = data_url
    variable_dict['downloadUrl'] = download_url
    variable_dict['summaryUrl'] = summary_url
    variable.write_variable_json(variable_dict)

    logger.info('完成生成app对比文件')




