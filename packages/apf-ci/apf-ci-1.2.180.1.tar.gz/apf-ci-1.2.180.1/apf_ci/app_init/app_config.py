#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用配置业务处理模块
"""

__author__ = '370418'

import os

from apf_ci.config.biz_comp_transform import BizCompJsonTransform
from apf_ci.app_init.utils import *
from apf_ci.app_init.utils.image_utils import *
from apf_ci.app_init.utils.js_third_app_utils import *
from apf_ci.config.lite_app import *
from apf_ci.config.page_attributes import PageAttributes
from apf_ci.config.env_service import EnvService
from apf_ci.init.git_template_service import *
from apf_ci.app_init.utils.appinfo_utils import AppInfo

def main(variable_dict):
    is_light_app = variable_dict['is_light_app']

    workspace_path = variable_dict['workspace_path']
    target_path = variable_dict['target_path']
    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')
    env_jenkins = variable_dict['envJenkins']

    app_type = variable_dict['build_app_type']
    is_local = variable_dict['is_local']

    storage_host = variable_dict['app_native_storage']
    resource_host = variable_dict['fac_resource_manage']
    widget_host = variable_dict["widget_manage"]
    page_host = variable_dict["page_manage"]
    envtarget = variable_dict['envtarget']
    lite_app_update_time = variable_dict['lite_app_update_time']
    factory_id = variable_dict['factoryId']
    com_test_type = variable_dict['comTestType']
    #----  target/defines.json
    defines = Defines(target_path)
    defines.download_define(variable_dict, storage_host, factory_id)

    #---- target/snapshot_template.json
    snapshot_templates = get_snapshot_templates_info(storage_host, factory_id)
    if snapshot_templates and snapshot_templates is not None:
        write_content_to_file(os.path.join(target_path, 'snapshot_template.json'), snapshot_templates)

    build_config = BuildConfig(target_path)
    build_config_json = build_config.read_build_config()

    ios_keychain_i18n = {}
    ios_keychain_file_type = {}
    ios_keychain_default = {}
    if app_type.lower() == 'ios':
        key_chain_namespace = build_config_json['key_chain_namespace']
        key_chain_bizname = build_config_json['key_chain_bizname']
        init_ios_keychain_biz(key_chain_namespace, key_chain_bizname,
                              variable_dict, target_path, ios_keychain_i18n, ios_keychain_file_type)
        ios_keychain_default = build_config_json['ios_permission_config']

    # -------------------------------
    apps = Apps(target_path)
    app_json = apps.read_app_info()
    app_info = AppInfo(target_path)
    app_info_json = app_info.get_app_info(storage_host, factory_id)
    #app_url = "%s/v0.8/apps/%s" % (storage_host, factory_id)
    #app_json = get_data(app_url)
    i18n_json = app_json['i18n']
    i18n_dict = init_i18n(i18n_json, storage_host)
    build_app_version = app_json['version']
    logger.debug(' 构建应用版本：%s' % build_app_version)
    variable_dict['build_app_version'] = build_app_version

    # 获取应用的语言，全部支持语言，默认语言
    languages_array = get_languages(storage_host, factory_id)
    variable_dict['languages'] = languages_array
    all_languages_array = get_all_languages(resource_host)
    variable_dict['allLanguages'] = all_languages_array
    default_language = get_default_language(resource_host, languages_array,app_json)
    variable_dict['defaultLang'] = default_language

    # 获取defines.json内容
    defines_json = Defines(target_path).defines_json()
    biz_comp_transform = BizCompJsonTransform(app_type)
    biz_comp_transform.make_property_map(defines_json)
    # 写入 target/i18nProperty.txt、imageProperty.txt
    logger.debug('【xmlI18nPropertyMap】=%s' % biz_comp_transform.i18n_property_map)
    logger.debug('【xmlImagePropertyMap】=%s' % biz_comp_transform.image_property_map)
    write_content_to_file(os.path.join(target_path, 'i18nProperty.txt'),
                          json.dumps(biz_comp_transform.i18n_property_map))
    write_content_to_file(os.path.join(target_path, 'imageProperty.txt'),
                          json.dumps(biz_comp_transform.image_property_map))

    environment_dict = get_environment_map(build_config_json)
    image_property_map = {}
    ios_permitsion_dict = {}
    app_name_dict = {}

    lite_app_map = None
    lite_app_host = ''
    lite_app_aws_json = ''
    env = ''
    dependency_array = []

    for language in languages_array:
        item_map_json = app_json['item_map']
        for item_map_key, id in item_map_json.items():
            item_url = "%s/v0.8/items/%s" % (storage_host, id)
            logger.debug("下载【%s】" % item_url)
            logger.debug("下载【%s】，key【%s】id【%s】" % (language, item_map_key, id))

            item_json = get_data(item_url)
            logger.debug("下载【%s】 done" % item_url)
            env_return = download_json_file(item_map_key, language, item_json, i18n_dict, biz_comp_transform,
                                            image_property_map, com_test_type, envtarget, environment_dict,
                                            ios_permitsion_dict, app_name_dict, app_type, defines_json,
                                            ios_keychain_i18n, ios_keychain_file_type, languages_array,
                                            ios_keychain_default, default_language, widget_host, page_host)
            if item_map_key == 'config' and env_return != '':
                env = env_return

        do_generate_pages_json(target_path, app_factory_path, language)



        app_language_path = os.path.join(app_factory_path, language)
        new_files_map = do_replace_image_file(target_path, app_language_path, app_type, image_property_map)
        if is_light_app is False:
            download_image_file(target_path, app_type, new_files_map)
        # 2021.08.09 新增 更新 components/build.json 里的versionNumber 参数为最新，解决编辑器不重新保存，版本信息不会更新的问题
        update_component_version(app_factory_path, language,variable_dict['biz_component_mng'])
        replace_module(target_path, app_factory_path, language)

        lite_app = LiteApp(app_factory_path)
        lite_app_host_map = lite_app.get_lite_app_host(target_path, env, lite_app_host, lite_app_aws_json)
        if lite_app_host_map is not None:
            lite_app_host = lite_app_host_map['liteAppHost']
            lite_app_aws_json = lite_app_host_map['liteAppAwsJson']

        if lite_app_map is None:
            lite_app_map = {}
            lite_app.get_host_map(lite_app_host, language, lite_app_map)

        defines = Defines(target_path)
        defines.parse(lite_app_map, app_factory_path, app_type, lite_app_update_time)

        if is_light_app is False:
            build_data = read_file_content(os.path.join(app_factory_path, language, 'components', 'build.json'))
            build_array = json.loads(build_data)
            dependency_array += build_array

            create_app_name_file(target_path, app_name_dict)
            create_ios_permision_file(target_path, ios_permitsion_dict)
            create_dependency_final(target_path, dependency_array)

    append_apf_ci_config(app_factory_path, variable_dict)
    variable_dict['lite_app_server'] = lite_app_host
    variable_dict['liteAppAwsJson'] = lite_app_aws_json

    if is_light_app is False:
        download_xml_proguard(storage_host, factory_id, target_path)
        page_attributes = PageAttributes(env_jenkins, is_local, target_path)
        page_attributes.handle_page_attributes(app_factory_path)

    env_service = EnvService(variable_dict, env_jenkins)
    env_service.append_data_to_config(app_factory_path, environment_dict, build_config_json, app_json, app_info_json)

     # 下载js_third_app.json 并存到app目录下,必须env_service.append_data_to_config 步骤后执行
    js_third_app = JsThirdApp(workspace_path)
    js_third_app.write_content(js_third_app.get_content())

    variable = Variable(target_path)
    variable.write_variable_json(variable_dict)
    #write_content_to_file(variables_path, json.dumps(variable_dict))

    runtime = Runtime(target_path)
    runtime.handle_build_json_file(languages_array, app_factory_path)


def append_apf_ci_config(app_factory_path, variable_dict):
    """
        将build.json 中 apf-ci 脚本工具定义的 variables_ 开头属性，保存到 target/variables.json
        """
    build_data = read_file_content(os.path.join(app_factory_path, 'zh-CN', 'components', 'build.json'))
    build_array = json.loads(build_data)
    for component_json in build_array:
        component_name_json = component_json['component']
        if component_name_json['name'] == 'apf-ci':
            properties_json = component_json['properties']
            for proper_key in properties_json:
                #  variables_ 开头属性
                if proper_key.startswith('variables_'):
                    if properties_json[proper_key] != '':
                        variable_key = proper_key.replace('variables_', '')
                        variable_dict[variable_key] = properties_json[proper_key]


def create_app_name_file(target_path, app_name_dict):
    """
    创建appNameJson.json文件
    :param target_path: 文件根路径
    :param app_name_dict: 文件内容
    :return:
    """
    app_name_json_path = os.path.join(target_path, 'appNameJson.json')
    write_content_to_file(app_name_json_path, json.dumps(app_name_dict))


def create_ios_permision_file(target_path, ios_permitsion_dict):
    """
    创建each_language_ios_permision.json文件
    :param target_path: 文件根路径
    :param ios_permitsion_dict: 文件内容
    :return:
    """
    ios_permision_path = os.path.join(target_path, 'each_language_ios_permision.json')
    write_content_to_file(ios_permision_path, json.dumps(ios_permitsion_dict))


def create_dependency_final(target_path, dependency_array):
    """
    解析依赖数组中的数据，去重后保存数据到dependencyFinal.txt文件中
    :param target_path:
    :param dependency_array:
    :return:
    """
    key_list = []
    dependency_final_array = []

    for dependency_json in dependency_array:
        component_json = dependency_json['component']
        key = '%s_%s' % (component_json['name'], component_json['namespace'])
        if key not in key_list:
            key_list.append(key)
            dependency_final_array.append(dependency_json)

    logger.debug('dependencyFinal: 存放在/target/dependencyFinal.txt中')
    dependency_final_path = os.path.join(target_path, 'dependencyFinal.txt')
    write_content_to_file(dependency_final_path, json.dumps(dependency_final_array))
