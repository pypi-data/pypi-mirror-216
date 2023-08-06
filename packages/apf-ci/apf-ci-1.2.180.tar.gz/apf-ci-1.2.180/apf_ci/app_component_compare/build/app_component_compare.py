#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app对比工具
"""

__author__ = '370418'

import time
import os
import json
from apf_ci.util.log_utils import logger
from apf_ci.app_compare.build.app_compare_utils import save_and_upload
from apf_ci.util.http_utils import post_for_array_uc, get_data, post_for_array
from apf_ci.app_init.utils.build_config_utils import BuildConfig
from apf_ci.app_init.utils.variable_utils import Variable
from apf_ci.config.defines import Defines
from apf_ci.app_init.utils.apps_utils import Apps
from apf_ci.util.content_service_config import *


def main(args):
    #----  获取传入参数
    compare_id = args.appCompareId
    app_id = args.appId
    factory_id = args.factoryId
    version_from = args.versionFrom
    version_to = args.versionTo
    env_jenkins = args.envJenkins
    is_local = args.isLocal == 'true'

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        #----   初始化传入参数及路径
    # 针对 git  clone 需要空目录才能正常，日志文件生成延后到，clone步骤之后。这里日志比较少，直接输出到Console
    logger.delay_init(True)
    logger.info('开始生成app组件对比文件')

    #----   初始化传入参数及路径
    variable_dict = {}
    variable_dict['targetPath'] = target_path
    variable_dict['appCompareId'] = compare_id
    variable_dict['appId'] = app_id
    variable_dict['versionFrom'] = version_from
    variable_dict['versionTo'] = version_to
    variable_dict['envJenkins'] = env_jenkins
    variable_dict['isLocal'] = is_local
    variable_dict['dataUrl'] = ""
    variable = Variable(target_path)
    variable.write_variable_json(variable_dict)

    build_config = BuildConfig(target_path)
    build_config_json_encrypt = build_config.get_build_config(env_jenkins, is_local)
    build_config_json = build_config.decrypy_build_config(build_config_json_encrypt)
    build_config.write_build_config(build_config_json_encrypt)

    storage_host = build_config_json['service_host']['app_native_storage']['default']
    portal_app_server = build_config_json['app_factory_deploy_host']['domain_service']['default']
    biz_component_mng = build_config_json['service_host']['biz_component_mng']['default']
    fac_resource_manage = build_config_json['service_host']['fac_resource_manage']['default']
    app_factory_translate = build_config_json['service_host']['app_factory_translate']['default']
    #app_factory_translate = 'http://192.168.251.186:8081/'
    cs_server = build_config_json['cs_server']

    defines = Defines(target_path)
    defines.download_define_tag(variable_dict, storage_host, factory_id, False)
    defines_json = defines.defines_json()

    components_list = []
    components_map = {}
    for component_name in defines_json.keys():
        #components = components + component_name + ','
        defines_item = defines_json[component_name]
        component_item = {}
        component_item['namespace'] = defines_item['namespace']
        component_item['bizName'] = defines_item['biz_name']
        components_list.append(component_item)
        component_key = component_item['namespace'] + ':' + component_item['bizName']
        components_map[component_key] = component_item

    cs_config = ContentServiceConfig()
    cs_config.user_id = cs_server["cs_user_id"]
    cs_config.host = cs_server["cs_host"]
    cs_config.server_name = cs_server["cs_server_name"]
    cs_config.session_id = cs_server["cs_session_id"]
    cs_config.secret_key = cs_server["secret_key"]
    cs_config.access_key = cs_server["access_key"]

    # 获取不同版本的组件基本信息
    get_component_xml(biz_component_mng, version_from, components_map, cs_config)
    get_component_xml(biz_component_mng, version_to, components_map, cs_config)

    # 获取不同版本的组件的默认皮肤信息
    resource_id = get_resource_id(fac_resource_manage, 'skin')
    get_default_skin(fac_resource_manage, resource_id, version_from, components_map)
    get_default_skin(fac_resource_manage, resource_id, version_to, components_map)

    # 获取不同版本的组件， 在所在应用的多语言默认翻译信息
    app_info = Apps(target_path)
    app_json = app_info.get_app_info(storage_host, factory_id)
    i18n_map = app_json['i18n']
    language_resource_id = get_language_resource_id(fac_resource_manage)
    default_language = get_default_language(fac_resource_manage, language_resource_id, version_from, components_map)
    get_default_translate(app_factory_translate, version_from, components_map, default_language, i18n_map, cs_config)

    default_language = get_default_language(fac_resource_manage, language_resource_id, version_to, components_map)
    get_default_translate(app_factory_translate, version_to, components_map, default_language, i18n_map, cs_config)

    data = {}

    get_products_info(portal_app_server, data, app_id)
    data_components = []
    for component_key in components_map.keys():
        data_components.append(components_map[component_key])

    data['components'] = data_components

    data_url = save_and_upload(target_path, build_config_json, compare_id, 'data.json', data)
    logger.info("app组件对比文件上传cs成功：" + data_url)
    #summary_url = save_and_upload(target_path, build_config_json, compare_id, 'summary.json', data['summary'])
    #logger.info("app对比概要文件上传cs成功：" + summary_url)
    #download_url = get_download_url(build_config_json, data_url)
    #logger.info("app对比报告地址：" + download_url)
    variable_dict['dataUrl'] = data_url
    #variable_dict['downloadUrl'] = download_url
    #variable_dict['summaryUrl'] = summary_url
    variable.write_variable_json(variable_dict)

    logger.info('完成生成app组件对比文件')


def get_resource_id(fac_resource_manage, resource_name):
    """
     获取对应资源的资源id
    """
    resconfig_url = fac_resource_manage + 'v0.1/resconfig/' + resource_name
    resconfig = get_data(resconfig_url)
    for resconfig_item in resconfig:
        if resconfig_item['name'] == 'skin-resource':
            return resconfig_item['id']


def get_language_resource_id(fac_resource_manage):
    """
     获取权重最高的语言id，用于后续获取默认语言资源
    """
    resconfig_url = fac_resource_manage + 'v0.1/resconfig/language/tree'
    resconfig = get_data(resconfig_url)
    # 返回权重最高的语言id
    return resconfig[0]['id']


def get_default_skin(fac_resource_manage, resource_id, version, components_map):
    """
     获取组件的默认皮肤资源
    """
    get_default_skin_url = fac_resource_manage + 'v0.1/default/batch/' + resource_id
    components = get_version_component(version, components_map)

    post_body = {}
    post_body['comps'] = components
    resp = post_for_array(get_default_skin_url, post_body)

    for resp_item in resp:
        component_key = resp_item['namespace'] + ':' + resp_item['biz_name']
        if component_key in components_map.keys():
            components_map[component_key][version]['skin'] = resp_item['items']


def get_default_language(fac_resource_manage, resource_id, version, components_map):
    """
     获取组件的默认语言资源，用于后续获取翻译资源
    """
    get_default_url = fac_resource_manage + 'v0.1/default/batch/' + resource_id
    components = get_version_component(version, components_map)

    post_body = {}
    post_body['comps'] = components
    resp = post_for_array(get_default_url, post_body)

    return resp


def get_default_translate(app_factory_translate, version, components_map, default_language, i18n_map,
                          cs_config):
    """
     获取组件的默认翻译资源
    """
    get_default_url = app_factory_translate + 'v1.0/resources/actions/batch-comps/'
    os_bodys = {}

    # 根据 不同的系统+组件类型  构造出接口请求参数
    for component_item in default_language:
        if 'items' in component_item:
            language_items = component_item['items']
            for language_item in language_items:
                os_key = language_item['os_type'] + ':' + language_item['component_type']
                if not os_key in os_bodys.keys():
                    os_item = {}
                    os_item['app_id'] = 'platform-default'
                    os_item['os'] = language_item['os_type']
                    os_item['type'] = language_item['component_type']
                    os_item['state'] = 'pass'
                    os_components = []
                    os_item['components'] = os_components
                    os_bodys[os_key] = os_item
                os_component = {}
                os_component['namespace'] = component_item['namespace']
                os_component['name'] = component_item['biz_name']
                os_component['version'] = language_item['version']
                os_bodys[os_key]['components'].append(os_component)

    i18n_keys = i18n_map.keys()
    components_language = {}
    for i18n in i18n_keys:
        components_language[i18n] = []

    for os_key in os_bodys.keys():
        os_item = os_bodys[os_key]
        # 根据 不同的系统+组件类型  请求组件所有的翻译资源
        resp = post_for_array_uc(get_default_url, os_item, cs_config)
        for resp_item in resp:
            component_key = resp_item['extra_infos']['namespace'] + ':' + resp_item['extra_infos']['name']
            language_type = resp_item['language']
            if component_key in components_map.keys() and language_type in i18n_keys:
                if not 'language' in components_map[component_key][version]:
                    components_language = {}
                    for i18n in i18n_keys:
                        components_language[i18n] = []
                    components_map[component_key][version]['language'] = components_language
                language_item = {}
                language_item['osType'] = resp_item['os']
                language_item['componentType'] = resp_item['type']
                language_item['resourceUrl'] = resp_item['uri']
                language_item['version'] = resp_item['version']
                components_map[component_key][version]['language'][language_type].append(language_item)


def get_component_xml(biz_component_mng, version, components_map):
    """
     获取组件的组件定义、版本等信息
    """
    components = get_version_component(version, components_map)
    #get_components_url = biz_component_mng + 'v1.0/batch/define'
    get_components_url = biz_component_mng + 'v1.0/bizs/versions?isGetTagName=true'

    post_body = {}
    post_body['comps'] = components
    resp = post_for_array(get_components_url, post_body)

    for resp_item in resp:
        component_key = resp_item['namespace'] + ':' + resp_item['biz_name']
        if component_key in components_map.keys():
            version_item = {}
            version_item['xml'] = resp_item['xml']
            version_item['label'] = resp_item['label']
            if 'versionNumber' in resp_item['lifecycle']:
                version_item['version'] = resp_item['lifecycle']['versionNumber']
            else:
                logger.warning("组件版本不存在：")
                logger.warning(json.dumps(resp_item))
            if 'versionDescription' in resp_item['lifecycle']:
                version_item['versionDescription'] = resp_item['lifecycle']['versionDescription']
            else:
                logger.warning("组件版本描述不存在：")
                logger.warning(json.dumps(resp_item))
                #version_item['tagSnapshotName'] = resp_item['lifecycle']['tagSnapshotName']
            components_map[component_key][version] = version_item


def get_version_component(version, components_map):
    """
     获取组件的组合string
    """
    components = ''
    for component_item in components_map.keys():
        component_version = component_item + ':' + version
        if components == '':
            components = components + component_version
        else:
            components = components + ',' + component_version

    return components


def get_products_info(portal_app_server, data, app_id):
    """
     获取组件的组件定义、版本等信息
    """
    #get_components_url = biz_component_mng + 'v1.0/batch/define'
    get_components_url = portal_app_server + '/v1.0/products/' + app_id

    resp = get_data(get_components_url)
    data["data_time"] = int(round(time.time()) * 1000)
    data["sdp_app_id"] = resp['id']
    data["factory_id"] = resp['factory_id']
    data["label"] = resp['label']
    data["name"] = resp['name']


