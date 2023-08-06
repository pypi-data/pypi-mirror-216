#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
构建空间初始化之后，按照应用需求将target目录下一些文件转移到app目录下
"""

__author__ = '370418'

import os
from apf_ci.app_res.android_plugin import AndroidPlugin
from apf_ci.app_res.language_res import LanguageRes
from apf_ci.resource.language import LanguageResource
from apf_ci.app_res.skin_res import SkinResource
from apf_ci.app_init.utils.variable_utils import Variable
from apf_ci.util.log_utils import logger
from apf_ci.resource.cache_service import CacheService

def main():

    logger.info('按照应用需求将target目录下一些文件，如语言包、皮肤包等转移到app目录下')
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')

    variable = Variable(target_path)
    variables_json = variable.read_variable_json()
    android_json_obj = AndroidPlugin(target_path)
    android_json = android_json_obj.android_json()

    # 解压 皮肤包 到 app/res 下
    skin_resource = SkinResource(target_path, variables_json)
    skin_resource.unzip_skin(android_json_obj, android_json)

    # 解压 语言包 到 app/res 下
    language_res = LanguageRes(target_path, variables_json)
    language_res.unzip_language(android_json_obj, android_json)

    language_resource = LanguageResource(target_path, variables_json)
    download_language_array = language_resource.get_language_resources()
    #resource_config = ResourceConfig(workspace_path)
    app_type = variables_json['build_app_type']
    cache_switch = variables_json['cache_switch']
    cache_service = CacheService(app_type)
     # 处理安卓的英语默认资源下载，解压到/res/values下
    if app_type.lower() == 'android':
        language_res._android_en_language_resource_handle(app_type, download_language_array, cache_switch,
                                                             language_resource,language_res, cache_service, android_json_obj,
                                                             android_json, variables_json)