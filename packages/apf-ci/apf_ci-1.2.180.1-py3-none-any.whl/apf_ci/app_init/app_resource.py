#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
资源配置业务处理模块
"""

__author__ = '370418'

from apf_ci.resource.resource_builder import *
#from apf_ci.config.android_plugin import *
from apf_ci.resource.skin import SkinResource
from apf_ci.resource.language import LanguageResource
from apf_ci.resource.cache_service import CacheService


def main(variables_json):
    cache_switch = variables_json['cache_switch']
    is_local = variables_json['is_local']

    workspace_path = variables_json['workspace_path']
    target_path = variables_json['target_path']

    #variables_path = os.path.join(target_path, 'variables.json')
    #variables_data = read_file_content(variables_path)
    #variables_json = json.loads(variables_data)

    app_type = variables_json['build_app_type']


    cache_service = CacheService(app_type)
    skin_resource = SkinResource(target_path, variables_json)
    skin_resources_array = skin_resource.get_skin_resources()
    # true:开启缓存 false:关闭缓存
    if cache_switch:
        resource_type = "skin"
        download_pool_array, copy_pool_array = skin_resource.skin_resource_cache_handle(
            skin_resources_array, download_type=None)
        # 未命中的统一下载
        cache_service.download_new_resource(download_pool_array)
        # 将资源拷贝到工作空间的目录下
        cache_service.copy_cache_into_job(copy_pool_array, resource_type)
    else:
        skin_resource.download_skin(skin_resources_array, download_type=None)
    #skin_resource.unzip_skin()

    language_resource = LanguageResource(target_path, variables_json)
    download_language_array = language_resource.get_language_resources()
    for language_name in download_language_array:
        language_resources_array = download_language_array[language_name]
        if cache_switch:
            resource_type = "language"
            download_pool_array, copy_pool_array = language_resource.language_resource_cache_handle(
                language_resources_array, language_name, download_type=None)
            # 未命中的统一下载
            cache_service.download_new_resource(download_pool_array)
            # 将资源拷贝到工作空间的目录下
            cache_service.copy_cache_into_job(copy_pool_array, resource_type)
        else:
            language_resource.download_language(app_type, language_name, language_resources_array,None,None)

    #android_plugin = AndroidPlugin(target_path)
    #android_plugin_json = android_plugin.android_json()
    #language_resource.unzip_language(android_plugin, android_plugin_json)

    resource_config = ResourceConfig(workspace_path)

    # 处理安卓的英语默认资源下载，解压到/res/values下
    #if app_type.lower() == 'android':
    #    resource_config._android_en_language_resource_handle(app_type, download_language_array, cache_switch,
    #                                                         language_resource, cache_service, android_plugin,
    #                                                         android_plugin_json, variables_json)

    default_language = variables_json['defaultLang']
    target_build_path = os.path.join(target_path, 'app_component_pages', default_language, 'build.json')
    biz_version_map = resource_config.init_bizs_version(target_build_path)

    resource_host = variables_json['fac_resource_manage']
    environment_resource_map, environment_name_map = resource_config.init_environment_resource(resource_host)

    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')
    biz_env_path = os.path.join(app_factory_path, default_language, 'components', 'biz_env.json')
    biz_plugin_path = os.path.join(app_factory_path, default_language, 'components', 'plugin.json')
    env = variables_json['env']
    each_environment_bizs_map, plugin_env_map = resource_config.init_each_environment_bizs(biz_env_path,
                                                                                           biz_plugin_path,
                                                                                           biz_version_map,
                                                                                           environment_resource_map,
                                                                                           env, environment_name_map)

    resource_config.create_service_json(each_environment_bizs_map, resource_host, app_factory_path)
    resource_config.create_datasources_json(app_factory_path, default_language, plugin_env_map, resource_host)

    app_pages_path = os.path.join(target_path, 'app_component_pages', default_language, 'app_pages.json')
    resource_config.create_page_controller_json(app_factory_path, app_pages_path, False)

    if app_type.lower() == 'android':
        resource_config.delete_xml()

    variables_path = os.path.join(target_path, 'variables.json')
    write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
