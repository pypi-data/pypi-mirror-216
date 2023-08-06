#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用配置业务处理模块
"""

__author__ = 'LianGuoQing'

from apf_ci.config.runtime import Runtime
from apf_ci.config.defines import Defines
from apf_ci.config.widget_tree import WidgetTree
from apf_ci.config.properties_transform import *
from apf_ci.config.lite_app import LiteApp
from apf_ci.config.language_service import *
from apf_ci.config.env_service import EnvService
from apf_ci.config.page_attributes import PageAttributes
from apf_ci.util.http_utils import *
from apf_ci.app_init.utils.build_config_utils import *
from apf_ci.config.biz_comp_transform import BizCompJsonTransform
from apf_ci.config.json_property_analysis import JsonPropertyAnalysis
from apf_ci.util.hook_service import HookService

from apf_ci.config.widget_i18n_utils import *
from apf_ci.config.page_i18n_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import BuildConfig
from apf_ci.app_init.utils.appinfo_utils import AppInfo

key_path_dict = {
    'config': 'app',
    'extension': 'app',
    'build': 'components',
    'files': 'components',
    'pages': 'pages',
    'app_pages': 'pages',
    'component_pages': 'pages',
    'widget': 'pages',
    'biz_env': 'components',
    'ios_extension': 'components',
    'plugin': 'components'
}


def main(args):
    is_local = args.isLocal == 'true'
    is_light_app = args.isLightApp == 'true'

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')

    variables_path = os.path.join(target_path, 'variables.json')
    variables_data = read_file_content(variables_path)
    variable_dict = json.loads(variables_data)

    env_jenkins = args.envJenkins
    if env_jenkins is None:
        env_jenkins = variable_dict['envJenkins']

    app_type = variable_dict['build_app_type']

    hook_service = HookService(app_type)
    if is_light_app is False:
        gradle_home = variable_dict['gradleHome']
        hook_service.hook('pre_app_config', gradle_home, is_local)

    storage_host = variable_dict['app_native_storage']
    resource_host = variable_dict['fac_resource_manage']
    widget_host = variable_dict["widget_manage"]
    page_host = variable_dict["page_manage"]

    envtarget = variable_dict['envtarget']
    lite_app_update_time = variable_dict['lite_app_update_time']
    factory_id = variable_dict['factoryId']
    com_test_type = variable_dict['comTestType']

    app_url = "%s/v0.8/apps/%s" % (storage_host, factory_id)
    app_json = get_data(app_url)
    app_info = AppInfo(target_path)
    app_info_json = app_info.get_app_info(storage_host, factory_id)
    i18n_json = app_json['i18n']
    i18n_dict = init_i18n(i18n_json, storage_host)

    build_app_version = app_json['version']
    logger.debug(' 构建应用版本：%s' % build_app_version)
    variable_dict['build_app_version'] = build_app_version

    languages_array = get_languages(storage_host, factory_id)
    variable_dict['languages'] = languages_array
    all_languages_array = get_all_languages(resource_host)
    variable_dict['allLanguages'] = all_languages_array
    language_tree_array = get_language_tree(resource_host)
    default_language = get_default_language(languages_array, language_tree_array)
    variable_dict['defaultLang'] = default_language

    # 获取defines.json内容
    defines_json = Defines(target_path).defines_json()
    biz_comp_transform = BizCompJsonTransform(app_type)
    biz_comp_transform.make_property_map(defines_json)

    logger.debug('【xmlI18nPropertyMap】=%s' % biz_comp_transform.i18n_property_map)
    logger.debug('【xmlImagePropertyMap】=%s' % biz_comp_transform.image_property_map)

    build_config = BuildConfig(target_path)
    build_config_json_encrypt = build_config.get_build_config(variable_dict['envJenkins'],is_local)
    build_config_json = build_config.decrypy_build_config(build_config_json_encrypt)
    environment_dict = get_environment_map(build_config_json)

    ios_keychain_i18n = {}
    ios_keychain_file_type = {}
    ios_keychain_default = {}
    if app_type.lower() == 'ios':
        key_chain_namespace = build_config_json['key_chain_namespace']
        key_chain_bizname = build_config_json['key_chain_bizname']
        init_ios_keychain_biz(key_chain_namespace, key_chain_bizname,
                              variable_dict, target_path, ios_keychain_i18n, ios_keychain_file_type)
        ios_keychain_default = build_config_json['ios_permission_config']

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
            logger.debug(" 下载【%s】" % item_url)
            logger.debug(" 下载【%s】，key【%s】id【%s】" % (language, item_map_key, id))

            item_json = get_data(item_url)
            logger.debug(" 下载【%s】 done" % item_url)
            env_return = download_json_file(item_map_key, language, item_json, i18n_dict, biz_comp_transform,
                                            image_property_map, com_test_type, envtarget, environment_dict,
                                            ios_permitsion_dict, app_name_dict, app_type,
                                            ios_keychain_i18n, ios_keychain_file_type, languages_array,
                                            ios_keychain_default, default_language, widget_host, page_host)
            if item_map_key == 'config' and env_return != '':
                env = env_return

        do_generate_pages_json(target_path, app_factory_path, language)

        app_language_path = os.path.join(app_factory_path, language)
        new_files_map = do_replace_image_file(target_path, app_language_path, app_type, image_property_map)
        if is_light_app is False:
            download_image_file(target_path, app_type, new_files_map)

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

    variable_dict['lite_app_server'] = lite_app_host
    variable_dict['liteAppAwsJson'] = lite_app_aws_json

    if is_light_app is False:
        download_xml_proguard(storage_host, factory_id, target_path)

        page_attributes = PageAttributes(env_jenkins, is_local, target_path)
        page_attributes.handle_page_attributes(app_factory_path)

    env_service = EnvService(variable_dict, env_jenkins)
    env_service.append_data_to_config(app_factory_path, environment_dict, build_config_json, app_json, app_info_json)

    write_content_to_file(variables_path, json.dumps(variable_dict))

    runtime = Runtime(target_path)
    runtime.handle_build_json_file(languages_array, app_factory_path)

    if is_light_app is False:
        hook_service.hook('post_app_config', gradle_home, is_local)


def init_ios_keychain_biz(key_chain_namespace, key_chain_bizname,
                          variable_dict, target_path, ios_keychain_i18n, ios_keychain_file_type):
    biz_comp_mng_host = variable_dict['biz_component_mng']
    biz_defines_dict = get_biz_define(biz_comp_mng_host, key_chain_namespace, key_chain_bizname)

    biz_ios_keychain_define_path = os.path.join(target_path, 'biz_ios_keychain_define.json')
    write_content_to_file(biz_ios_keychain_define_path, json.dumps(biz_defines_dict))
    logger.debug(' 创建文件: %s' % biz_ios_keychain_define_path)

    properties_json = biz_defines_dict['properties']

    get_i18n_map_and_file_type(properties_json, ios_keychain_i18n, ios_keychain_file_type)

    keychain_i18n_path = os.path.join(target_path, 'keychain_i18n.json')
    write_content_to_file(keychain_i18n_path, json.dumps(ios_keychain_i18n))
    logger.info(' 创建文件: %s' % keychain_i18n_path)

    keychain_file_type_path = os.path.join(target_path, 'keychain_file_type.json')
    write_content_to_file(keychain_file_type_path, json.dumps(ios_keychain_file_type))
    logger.info(' 创建文件: %s' % keychain_file_type_path)


def get_i18n_map_and_file_type(properties_json, ios_keychain_i18n, ios_keychain_file_type):
    """
    得到是否国际化的Map和file name entitlements OR info
    :param properties_json:
    :param properties_key:
    :param ios_keychain_i18n:
    :param ios_keychain_file_type:
    :return:
    """
    for properties_key in properties_json:
        ios_privacy = properties_json[properties_key]

        if isinstance(ios_privacy, dict):
            if '_i18n' in ios_privacy.keys() and ios_privacy['_i18n'].lower() == 'true':
                ios_keychain_i18n[properties_key] = True
            else:
                ios_keychain_i18n[properties_key] = False

            ios_keychain_file_type[properties_key] = 'info'
            if 'entitlements' in ios_privacy.keys():
                ios_keychain_file_type[properties_key] = 'entitlements'


def get_biz_define(biz_comp_mng_host, namespace, biz_name):
    """
    获取业务组件定义
    :param biz_comp_mng_host:
    :param namespace:
    :param biz_name:
    :return:
    """
    biz_comp_mng_url = "%s/v1.0/%s/%s/release/define" % (biz_comp_mng_host, namespace, biz_name)
    return get_data(biz_comp_mng_url)


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


def replace_module(target_path, app_factory_path, language):
    """
    删除widgets.json中的module内容，备份widgets.json、pages.json、build.json文件
    :param target_path:
    :param app_factory_path:
    :param language:
    :return:
    """
    app_widgets_path = os.path.join(app_factory_path, language, 'pages', 'widgets.json')
    app_widgets_data = read_file_content(app_widgets_path)

    widgetTree = WidgetTree()
    app_widgets_content = widgetTree.remove_module(json.loads(app_widgets_data))
    write_content_to_file(app_widgets_path, json.dumps(app_widgets_content))

    target_widgets_path = os.path.join(target_path, 'app_component_pages', language, 'widgets.json')
    write_content_to_file(target_widgets_path, json.dumps(app_widgets_content))

    app_pages_path = os.path.join(app_factory_path, language, 'pages', 'pages.json')
    if os.path.exists(app_pages_path):
        app_pages_data = read_file_content(app_pages_path)
        replacement = widgetTree.get_replacement()

        for replacement_key in replacement:
            app_pages_data = app_pages_data.replace(replacement_key, replacement[replacement_key])

        # app_pages_data.replace('\"\\s*module://.*\"', '\"\"')
        target_pages_path = os.path.join(target_path, 'app_component_pages', language, 'pages.json')
        write_content_to_file(target_pages_path, app_pages_data)

        write_content_to_file(app_pages_path, app_pages_data)

    app_build_path = os.path.join(app_factory_path, language, 'components', 'build.json')
    if os.path.exists(app_build_path):
        app_build_data = read_file_content(app_build_path)
        target_build_path = os.path.join(target_path, 'app_component_pages', language, 'build.json')
        write_content_to_file(target_build_path, app_build_data)


def do_replace_image_file(target_path, app_language_path, app_type, image_property_map):
    """
    替换widgets.json、pages.json、build.json文件中的图片
    :param target_path:
    :param app_language_path:
    :param app_type:
    :param image_property_map:
    :return:
    """
    for image_property_key in image_property_map:
        logger.debug('entry : key:%s --%s' % (image_property_key, image_property_map[image_property_key]))

    new_files_map = {}

    #读取设备iamge size mode配置
    build_config = BuildConfig(os.path.join(os.getcwd(), 'target'))
    build_config_json = build_config.read_build_config()
    device_image_size_mode = build_config_json['device_image_size_mode']
    logger.debug('device_image_size_mode：%s' % device_image_size_mode)

    app_pages_path = os.path.join(app_language_path, 'pages', 'pages.json')
    logger.info('替换page.json开始：%s' % app_pages_path)
    app_pages_data = read_file_content(app_pages_path)

    page_transform = PageWidgetTransform(target_path, device_image_size_mode)
    page_transform.set_content(app_pages_data)
    page_transform.set_app_type(app_type)
    for image_property_key in image_property_map:
        if image_property_map[image_property_key]:
            page_transform.set_adapter_key(image_property_key)
            page_transform.search_property(image_property_map[image_property_key])
            new_files_map = dict(new_files_map, **page_transform.repalce_map)

    write_content_to_file(app_pages_path, page_transform.content)
    logger.info('替换page.json结束')

    app_widgets_path = os.path.join(app_language_path, 'pages', 'widgets.json')
    if os.path.exists(app_widgets_path):
        logger.info('替换widgets.json开始：%s' % app_widgets_path)
        app_widgets_data = read_file_content(app_widgets_path)

        if app_widgets_data and app_widgets_data != '{}':
            widgets_transform = PageWidgetTransform(target_path, device_image_size_mode)
            widgets_transform.set_content(app_widgets_data)
            widgets_transform.set_app_type(app_type)

            for image_property_key in image_property_map:
                if image_property_map[image_property_key]:
                    widgets_transform.set_adapter_key(image_property_key)
                    widgets_transform.search_property(image_property_map[image_property_key])
                    new_files_map = dict(new_files_map, **widgets_transform.repalce_map)

            write_content_to_file(app_widgets_path, widgets_transform.content)
            logger.info('替换widgets.json结束')

    app_build_path = os.path.join(app_language_path, 'components', 'build.json')
    logger.info('替换build.json开始：%s' % app_build_path)
    app_build_data = read_file_content(app_build_path)

    build_transform = BuildTransform(target_path, device_image_size_mode)
    build_transform.set_content(app_build_data)
    build_transform.set_app_type(app_type)

    for image_property_key in image_property_map:
        if image_property_map[image_property_key]:
            build_transform.set_adapter_key(image_property_key)
            build_transform.search_property(image_property_map[image_property_key])
            new_files_map = dict(new_files_map, **build_transform.repalce_map)
    write_content_to_file(app_build_path, build_transform.content)
    logger.info('替换build.json结束')

    return new_files_map


def download_image_file(target_path, app_type, new_files_map):
    """
    下载图片文件
    :param target_path:
    :param app_type:
    :param new_files_map:
    :return:
    """
    logger.info('下载newFile文件开始')
    base_path = os.path.dirname(target_path)
    if app_type.lower() == 'android':
        absolute = os.path.join(base_path, 'app', 'res', 'drawable-hdpi')
    elif app_type.lower() == 'ios':
        absolute = os.path.join(base_path, 'ComponentAppBase', 'Resources', 'skin',
                                'com.nd.smartcan.appfactory.main_component_skin.bundle')

    url_path_array = []
    for file_name in new_files_map:
        logger.debug('【判断文件】%s' % file_name)
        file_path_value = new_files_map[file_name]

        if file_name.endswith('.zip'):
            # 上传ZIP包图片，支持多分辨率
            handle_zip_file(file_name, target_path, absolute, app_type)
        else:
            if isinstance(file_path_value, str):
                # 正常图片下载
                if file_path_value:
                    file_path_value = file_path_value.replace('\"', '')
                    save_path = os.path.join(absolute, file_name)
                    logger.debug('下载文件【%s】保存在【%s】' % (file_path_value, save_path))

                    url_path_json = {}
                    url_path_json[file_path_value] = save_path
                    url_path_array.append(url_path_json)
            elif isinstance(file_path_value, dict):
                # 图片适配
                url = file_path_value['_value']
                if url:
                    try:
                        resizes = file_path_value['_resize']
                    except KeyError:
                        resizes = ''

                    if app_type.lower() == 'android':
                        file_name = file_name[file_name.find('@') + 1:]

                    if resizes:
                        # 按规定尺寸输出
                        for resize in resizes.split(','):
                            resize = resize.replace(' ', '')
                            if resize.find('@') > -1:
                                size = resize[0:resize.find('@')]
                            else:
                                size = resize

                            save_relative_path = absolute
                            if app_type.lower() == 'android':
                                hdpi_name = ''

                                if resize.find('@') > -1 and resize[resize.find('@') + 1:]:
                                    hdpi_name = '%s%s' % ('drawable-', resize[resize.find('@') + 1:])
                                else:
                                    model = file_path_value['_model']
                                    if model == 'hdpi' or model == 'xhdpi' or model == 'xxhdpi' or model == 'xxxhdpi':
                                        hdpi_name = '%s%s' % ('drawable-', model)

                                if hdpi_name:
                                    save_relative_path = os.path.join(os.path.dirname(absolute), hdpi_name)

                            save_file_path = os.path.join(save_relative_path, file_name)
                            download_cs_file(url, save_file_path, 3)
                            logger.debug('下载文件【%s】保存在【%s】' % (url, save_file_path))

                            if size:
                                if size.find('*') > -1:
                                    output_width = int(size[0:size.find('*')])
                                    output_height = int(size[size.find('*') + 1:])
                                else:
                                    output_width = int(size)
                                    output_height = int(size)

                                resize_image(save_file_path, save_file_path, output_width, output_height)
                    else:
                        save_relative_path = absolute

                        if app_type.lower() == 'android':
                            hdpi_name = ''
                            model = file_path_value['_model']
                            if model == 'hdpi' or model == 'xhdpi' or model == 'xxhdpi' or model == 'xxxhdpi':
                                hdpi_name = '%s%s' % ('drawable-', model)

                            if hdpi_name:
                                save_relative_path = os.path.join(os.path.dirname(absolute), hdpi_name)

                        # 按原始尺寸输出app-factory-dependency-service
                        save_path = os.path.join(save_relative_path, file_name)
                        logger.debug('下载文件【%s】保存在【%s】' % (url, save_path))
                        url_path_json = {}
                        url_path_json[url] = save_path
                        url_path_array.append(url_path_json)

    if url_path_array.__len__() > 0:
        multi_download_pool(url_path_array)
    logger.info('下载newFile文件结束')


def handle_zip_file(file_name, target_path, absolute, app_type):
    """
    将zip包中的文件通过规则进行拷贝
    :param file_name:
    :param target_path:
    :param absolute:
    :param app_type:
    :return:
    """
    # 取文件名索引
    index = file_name.rfind('/')
    if index == -1:
        # 不带路径的文件索引
        index = 0
    else:
        # 带路径的文件索引
        index += 1

    # 取不带格式的文件名
    folder_name = file_name[index:file_name.rfind('.zip')]
    # 放置zip解压文件的临时路径
    zip_temp_path = os.path.join(target_path, 'zipTemp', folder_name)

    for root, dirs, files in os.walk(zip_temp_path):
        for src_file_name in files:
            format_index = src_file_name.rfind('.')
            suffix_format = src_file_name[format_index:]
            xx_suffix_format = '%s%s' % ('@2x', suffix_format)
            xxx_suffix_format = '%s%s' % ('@3x', suffix_format)

            if app_type.lower() == 'android':
                base_path = os.path.dirname(absolute)

                if src_file_name.endswith(xx_suffix_format):
                    png_path = 'drawable-xhdpi'
                elif src_file_name.endswith(xxx_suffix_format):
                    png_path = 'drawable-xxxhdpi'
                else:
                    png_path = 'drawable-mdpi'

                dest_file_path = os.path.join(base_path, png_path, folder_name, suffix_format)

            elif app_type.lower() == 'ios':
                if src_file_name.endswith(xx_suffix_format):
                    suffix_format = '%s%s' % ('@2x', suffix_format)
                elif src_file_name.endswith(xxx_suffix_format):
                    suffix_format = '%s%s' % ('@3x', suffix_format)

                dest_file_path = os.path.join(absolute, folder_name, suffix_format)

            src_file_path = os.path.join(root, src_file_name)
            copy_file(src_file_path, dest_file_path)


def do_generate_pages_json(target_path, app_factory_path, language):
    """
    合并app_pages.json和component_pages.json文件内容到pages.json文件中
    :param target_path:
    :param app_factory_path:
    :param language:
    :return:
    """
    pages_json = {}

    target_language_path = os.path.join(target_path, 'app_component_pages', language)
    if not os.path.exists(target_language_path):
        os.makedirs(target_language_path)

    # backup and delete app_pages.json file
    app_pages_key_path = key_path_dict['app_pages']
    app_pages_path = os.path.join(app_factory_path, language, app_pages_key_path, 'app_pages.json')
    app_pages_data = read_file_content(app_pages_path)
    app_pages_array = json.loads(app_pages_data)

    write_content_to_file(os.path.join(target_language_path, 'app_pages.json'), json.dumps(app_pages_array))

    for app_pages_json in app_pages_array:
        template = app_pages_json['template']

        page_id = template[template.find('=') + 1:]
        if '__type' in app_pages_json.keys():
            if app_pages_json['__type'] == 'plugin':
                page_name = app_pages_json['page_name']
                page_id = page_name[0:page_name.find('/')]

        pages_json[page_id] = app_pages_json

    os.remove(app_pages_path)

    # backup and delete component_pages.json file
    component_pages_key_path = key_path_dict['component_pages']
    component_pages_path = os.path.join(app_factory_path, language, component_pages_key_path, 'component_pages.json')
    component_pages_data = read_file_content(component_pages_path)
    component_pages_array = json.loads(component_pages_data)

    write_content_to_file(os.path.join(target_language_path, 'component_pages.json'), json.dumps(component_pages_array))

    for component_pages_json in component_pages_array:
        template = component_pages_json['template']
        pages_json[template] = component_pages_json

    os.remove(component_pages_path)

    # create pages.json file
    pages_key_path = key_path_dict['pages']
    pages_path = os.path.join(app_factory_path, language, pages_key_path, 'pages.json')
    write_content_to_file(pages_path, json.dumps(pages_json))
    logger.info(' create pages.json file: %s ' % pages_path)


def replace_i18n(key, content, i18n_dict, language, i18n_property_map={}, image_property_map={}):
    """
    替换i18n内容
    :param key:
    :param content:
    :param i18n_dict:
    :param language:
    :param i18n_property_map:
    :param image_property_map:
    :return:
    """
    replace_content = content
    language_i18n_json = i18n_dict[language]
    zhcn_i18n_json = i18n_dict['zh-CN']

    for zhcn_i18n_key in zhcn_i18n_json:
        i18n_value = zhcn_i18n_json[zhcn_i18n_key]

        if zhcn_i18n_key in i18n_property_map.keys():
            if zhcn_i18n_key in language_i18n_json.keys():
                i18n_value = language_i18n_json[zhcn_i18n_key]

        if key.lower() == 'config' or key.lower() == 'ios_extension':
            if zhcn_i18n_key in language_i18n_json.keys():
                i18n_value = language_i18n_json[zhcn_i18n_key]

        if i18n_value is None:
            i18n_value = ''

        if zhcn_i18n_key in image_property_map.keys():
            if i18n_value:
                i18n_image_dict = {}
                if isinstance(i18n_value, dict):
                    i18n_image_dict = i18n_value
                else:
                    i18n_image_dict['default'] = i18n_value

                image_property = image_property_map[zhcn_i18n_key]
                if isinstance(image_property, list):
                    _image_property = []

                    for image_property_json in image_property:
                        _image_property_json = {}

                        model = 'default'
                        for image_property_key in image_property_json:
                            _image_property_json[image_property_key] = image_property_json[image_property_key]

                            if image_property_key == '_model':
                                model = image_property_json['_model']

                        image_value = ''
                        if model in i18n_image_dict.keys():
                            image_value = i18n_image_dict[model]

                        _image_property_json['_value'] = image_value
                        _image_property.append(_image_property_json)

                    image_property_map[json.dumps(i18n_value)] = _image_property
                    del image_property_map[zhcn_i18n_key]
                else:
                    image_property_map[zhcn_i18n_key] = i18n_value
            else:
                image_property_map[zhcn_i18n_key] = i18n_value

        if isinstance(i18n_value, str):
            # 如果有双引号需要加上这样的转义，否则在json.load会解析失败
            i18n_value = i18n_value.replace("\\", "\\\\")
            i18n_value = i18n_value.replace("\"", "\\\"")
            replace_content = replace_content.replace(zhcn_i18n_key, i18n_value)
        elif isinstance(i18n_value, dict):
            old = '"%s"' % zhcn_i18n_key
            new = json.dumps(i18n_value)

            if key.lower() == 'config' or key.lower() == 'widget':
                if 'default' in i18n_value.keys():
                    new = '"%s"' % i18n_value['default']

                replace_content = replace_content.replace(old, new)
            elif key.lower() == 'app_pages':
                replace_content = replace_widget_image(replace_content, old, i18n_value)
            else:
                replace_content = replace_content.replace(old, new)
        else:
            old = '%s%s%s' % ('"', zhcn_i18n_key, '"')
            replace_content = replace_content.replace(old, json.dumps(i18n_value))

    return replace_content


def replace_widget_image(content, old, i18n_value):
    """
    将widget中的图片格式default去除
    :param content:
    :param old:
    :param i18n_value:
    :return:
    """
    pattern = '^react://com.nd.apf.react.native.widget/(.+)$'
    new_content_array = []

    content_array = json.loads(content)
    for content_json in content_array:
        template = content_json['template']
        if template:
            replace_content = json.dumps(i18n_value)

            if re.match(pattern, template) is not None:
                if 'default' in i18n_value.keys():
                    replace_content = '"%s"' % i18n_value['default']

            node_json = json.dumps(content_json).replace(old, replace_content)
            new_content_array.append(json.loads(node_json))

    return json.dumps(new_content_array)


def download_json_file(key, language, item_json, i18n_dict, biz_comp_transform,
                       image_property_map, com_test_type, envtarget, environment_dict,
                       ios_permitsion_dict, app_name_dict, app_type,
                       ios_keychain_i18n, ios_keychain_file_type, languages_array, ios_keychain_default,
                       default_language, widget_host, page_host):
    """
    下载json文件
    :param key:
    :param language:
    :param item_json:
    :param i18n_dict:
    :param biz_comp_transform:
    :param image_property_map:
    :param com_test_type:
    :param envtarget:
    :param environment_dict:
    :param ios_permitsion_dict:
    :param app_name_dict:
    :return:
    """
    path = ''
    try:
        path = key_path_dict[key]
    except KeyError:
        pass

    if path == '':
        return ''

    app_factory_path = os.path.join(os.getcwd(), 'app', 'assets', 'app_factory')
    if key == 'config' or key == 'extension':
        path_dir = os.path.join(app_factory_path, path)
    else:
        path_dir = os.path.join(app_factory_path, language, path)

    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    file_name = item_json['fileName']
    if file_name == '':
        return ''

    content = item_json['content']
    if key == 'pages' or key == 'files':
        return ''
    elif key == 'biz_env':
        if com_test_type.upper() != 'APP_FACTORY_FUNCTION' \
            and com_test_type.upper() != 'CUSTOM_ENV_APP_FACTORY_FUNCTION' \
            and com_test_type.upper() != 'APP_FACTORY_INTEGRATE' \
            and com_test_type.upper() != 'CUSTOM_ENV_APP_FACTORY_INTEGRATE':
            return ''
    elif key == 'config':
        content = replace_i18n(key, content, i18n_dict, language)
        content_json = json.loads(content)

        env = '5'
        if 'env' in content_json.keys() and content_json['env']:
            env = content_json['env']

        if envtarget == 'development' and env == '8':
            env = '5'

        env_json = environment_dict[envtarget]
        if envtarget != 'development' and envtarget != 'test' and envtarget != 'preproduction':
            env = env_json['env']

        content_json['env'] = env

        logger.debug(" env【%s】envtarget【%s】" % (env, envtarget))

        # if 'iOSUsageDescription' in content_json.keys():
        #     ios_usage_description_arr = content_json['iOSUsageDescription']
        #     if ios_usage_description_arr.__len__() > 0:
        #         ios_permitsion_dict[language] = ios_usage_description_arr[0]

        app_name_dict[language] = content_json['label']
        if language != 'zh-CN':
            return env

        content = json.dumps(content_json)

    elif key == 'ios_extension':
        # ios权限从新的地方拿了
        content_privacy_temp_handle = item_json['content']
        content_privacy_temp_handle = replace_i18n(key, content_privacy_temp_handle, i18n_dict, language)
        content_privacy_temp_handle_json = json.loads(content_privacy_temp_handle)
        if content_privacy_temp_handle_json is not None:
            app_json = content_privacy_temp_handle_json['app']
            if app_json is not None:
                app_scenes_json = app_json['scenes']
                # 为了兼容ios 权限，写入info.plist
                if app_scenes_json is not None:
                    ios_permitsion_dict_obj = {}
                    for app_scenes_key in app_scenes_json:
                        if app_scenes_key.endswith('Description'):
                            ios_permitsion_dict_obj[app_scenes_key] = app_scenes_json[app_scenes_key]
                    ios_permitsion_dict[language] = ios_permitsion_dict_obj

        if app_type.lower() == 'ios' and language == 'zh-CN':
            content_temp = item_json['content']
            ios_keychain_uuid = read_ios_keychain_uuid(content_temp)
            logger.debug(" ios_extension替换前：" + content_temp)

            content_temp = replace_i18n(key, content_temp, i18n_dict, language)
            logger.debug(" ios_extension替换后：" + content_temp)

            content_json = json.loads(content_temp)

            move_privacy_to_i18n(content_json, ios_keychain_uuid,
                                 ios_keychain_i18n, ios_keychain_file_type, languages_array, i18n_dict, language,
                                 ios_keychain_default, default_language)

            ios_extension_path = os.path.join(os.getcwd(), 'target', 'ios_extension.json')
            write_content_to_file(ios_extension_path, json.dumps(content_json))
            logger.info(' 创建文件: %s' % ios_extension_path)

        content = replace_i18n(key, content, i18n_dict, language)
        file_name = 'ios_extension.json'

    elif key == 'build' or key == 'component_pages':
        if key == 'build':
            target_path = os.path.join(os.getcwd(), 'target')
            runtime = Runtime(target_path)
            content = runtime.handle_runtime_properties(content, app_type)

        i18n_property_map = {}
        json_property_analysis = JsonPropertyAnalysis(biz_comp_transform)
        json_property_analysis.make_uuid_map(content, key, i18n_property_map, image_property_map)

        content = replace_i18n(key, content, i18n_dict, language, i18n_property_map, image_property_map)
    elif key == 'app_pages':
        i18n_property_map = {}
        #筛选图片、属性
        json_property_analysis = JsonPropertyAnalysis(biz_comp_transform)
        json_property_analysis.make_uuid_map(content, key, i18n_property_map, image_property_map)

        template_data = json.loads(content, encoding="utf-8")
        #筛选国际化属性
        i18n_property_map2 = filter_page_uuid(template_data, page_host + "v0.1/pages/defines")

        i18n_property_map3 = {}
        i18n_property_map3.update(i18n_property_map)
        i18n_property_map3.update(i18n_property_map2)

        content = replace_i18n(key, content, i18n_dict, language, i18n_property_map3, image_property_map)
    elif key == 'widget':
        json_property_analysis = JsonPropertyAnalysis(biz_comp_transform)
        template_dict = json_property_analysis.make_widget_uuid_map(content, {}, {})

        i18n_property_map = filter_widget_uuid(template_dict, widget_host + "v0.1/widgets/defines")

        for page_id in template_dict:
            page = template_dict[page_id]
            template_data = json.dumps(page)
            value = replace_i18n(key, template_data, i18n_dict, language, i18n_property_map, {})
            template_dict[page_id] = json.loads(value)

        content = json.dumps(template_dict)
        file_name = 'widgets.json'

    file_path = os.path.join(path_dir, file_name)
    write_content_to_file(file_path, content)

    logger.debug('create file %s success: %s ' % (file_name, file_path))
    return ''


def handle_scenes(parent_json, pre_key, ios_keychain_uuid, ios_keychain_i18n,
                  ios_keychain_file_type, languages_array, i18n_dict, language, ios_keychain_default, default_language):
    i18n_default_language_json = i18n_dict[language]

    if 'scenes' in parent_json.keys():
        pop_scenes_arr = []

        scenes_json = parent_json['scenes']
        for scenes_key in scenes_json:
            each_scene = scenes_json[scenes_key]
            try:
                file_type = ios_keychain_file_type[scenes_key]
            except KeyError:
                file_type = 'info'

            if scenes_key in ios_keychain_i18n.keys() and ios_keychain_i18n[scenes_key]:
                if 'i18n' not in parent_json.keys():
                    parent_json['i18n'] = {}

                i18n_json = parent_json['i18n']
                for lang in languages_array:
                    ios_keychain_default_each_language_json = {}
                    if lang in ios_keychain_default:
                        ios_keychain_default_each_language_json = ios_keychain_default[lang]
                    else:
                        ios_keychain_default_each_language_json = ios_keychain_default[default_language]

                    i18n_lang_json = i18n_dict[lang]

                    if lang not in i18n_json.keys():
                        i18n_json[lang] = {}

                    lang_json = i18n_json[lang]
                    if 'scenes' not in lang_json.keys():
                        lang_json['scenes'] = {}

                    category_info_json = lang_json['scenes']
                    type_translation_json = {}

                    if isinstance(each_scene, list):
                        string_arr_flag = False
                        for arr in each_scene:
                            if isinstance(arr, str):
                                string_arr_flag = True
                                break

                        if string_arr_flag:
                            uuid_key = '%s%s' % (pre_key, scenes_key)
                            uuid = ios_keychain_uuid[uuid_key]
                            each_scene = i18n_lang_json[uuid]

                            if each_scene is '' and scenes_key in ios_keychain_default_each_language_json:
                                each_scene = ios_keychain_default_each_language_json[scenes_key]
                        else:
                            for i, each_scene_json in enumerate(each_scene):
                                for each_scene_key in each_scene_json:
                                    uuid_key = '%s%s_%s_%s' % (pre_key, scenes_key, i, each_scene_key)
                                    uuid = ios_keychain_uuid[uuid_key]

                                    if uuid in i18n_lang_json.keys():
                                        value_object = i18n_lang_json[uuid]
                                    else:
                                        value_object = i18n_default_language_json[uuid]

                                    if value_object is '' and each_scene_key in ios_keychain_default_each_language_json:
                                        value_object = ios_keychain_default_each_language_json[each_scene_key]

                                    each_scene_json[each_scene_key] = value_object

                        type_translation_json[file_type] = each_scene

                    else:
                        uuid_key = '%s%s' % (pre_key, scenes_key)
                        uuid = ios_keychain_uuid[uuid_key]
                        if uuid in i18n_lang_json.keys():
                            value_object = i18n_lang_json[uuid]
                        else:
                            value_object = i18n_default_language_json[uuid]
                        if value_object is '' and scenes_key in ios_keychain_default_each_language_json:
                            value_object = ios_keychain_default_each_language_json[scenes_key]
                        type_translation_json[file_type] = value_object

                    category_info_json[scenes_key] = type_translation_json

                pop_scenes_arr.append(scenes_key)

            else:
                ios_keychain_default_each_language_json = {}
                if language in ios_keychain_default:
                    ios_keychain_default_each_language_json = ios_keychain_default[language]
                else:
                    ios_keychain_default_each_language_json = ios_keychain_default[default_language]
                type_translation_json = {}

                if isinstance(each_scene, list):
                    string_arr_flag = False
                    for arr in each_scene:
                        if isinstance(arr, str):
                            string_arr_flag = True
                            break

                    if string_arr_flag:
                        uuid_key = '%s%s' % (pre_key, scenes_key)
                        uuid = ios_keychain_uuid[uuid_key]
                        each_scene = i18n_default_language_json[uuid]

                        if each_scene is '' and scenes_key in ios_keychain_default_each_language_json:
                            each_scene = ios_keychain_default_each_language_json[scenes_key]
                    else:
                        for i, each_scene_json in enumerate(each_scene):
                            for each_scene_key in each_scene_json:
                                uuid_key = '%s%s_%s_%s' % (pre_key, scenes_key, i, each_scene_key)
                                uuid = ios_keychain_uuid[uuid_key]

                                if uuid in i18n_default_language_json.keys():
                                    value_object = i18n_default_language_json[uuid]
                                else:
                                    value_object = ''

                                if value_object is '' and each_scene_key in ios_keychain_default_each_language_json:
                                    value_object = ios_keychain_default_each_language_json[each_scene_key]

                                each_scene_json[each_scene_key] = value_object

                    type_translation_json[file_type] = each_scene

                else:
                    uuid_key = '%s%s' % (pre_key, scenes_key)
                    uuid = ios_keychain_uuid[uuid_key]

                    if uuid in i18n_default_language_json.keys():
                        value_object = i18n_default_language_json[uuid]
                    else:
                        value_object = ''
                    if value_object is '' and scenes_key in ios_keychain_default_each_language_json:
                        value_object = ios_keychain_default_each_language_json[scenes_key]
                    type_translation_json[file_type] = value_object

                scenes_json[scenes_key] = type_translation_json

        for scenes_key in pop_scenes_arr:
            scenes_json.pop(scenes_key)


def move_privacy_to_i18n(content_json, ios_keychain_uuid, ios_keychain_i18n,
                         ios_keychain_file_type, languages_array, i18n_dict, language, ios_keychain_default,
                         default_language):
    """
    把国际化的权限移到i18n/{lang}
    :param content_json:
    :param ios_keychain_uuid:
    :param ios_keychain_i18n:
    :param ios_keychain_file_type:
    :param languages_array:
    :param i18n_dict:
    :param language:
    :return:
    """
    for key in content_json:
        value_json = content_json[key]

        if 'app' == key.lower():
            handle_scenes(value_json, 'app_', ios_keychain_uuid, ios_keychain_i18n,
                          ios_keychain_file_type, languages_array, i18n_dict, language, ios_keychain_default,
                          default_language)
        else:
            for share_key in value_json:
                share_json = value_json[share_key]
                handle_scenes(share_json, 'extension_', ios_keychain_uuid, ios_keychain_i18n,
                              ios_keychain_file_type, languages_array, i18n_dict, language, ios_keychain_default,
                              default_language)


def read_ios_keychain_uuid(content):
    ios_keychain_uuid = {}
    content_json = json.loads(content)

    for key in content_json:
        value_json = content_json[key]

        if 'app' == key.lower():
            get_uuid_map(value_json, ios_keychain_uuid, 'app')
        else:
            for share_key in value_json:
                share_json = value_json[share_key]
                get_uuid_map(share_json, ios_keychain_uuid, 'extension')

    return ios_keychain_uuid


def get_uuid_map(value_json, ios_keychain_uuid, uuid_type):
    if 'scenes' in value_json.keys():
        scenes_json = value_json['scenes']
        for scenes_key in scenes_json:
            scenes_value = scenes_json[scenes_key]
            if isinstance(scenes_value, list):
                for i, scenes_value_json in enumerate(scenes_value):
                    for scenes_value_key in scenes_value_json:
                        uuid_key = '%s_%s_%s_%s' % (uuid_type, scenes_key, i, scenes_value_key)
                        ios_keychain_uuid[uuid_key] = scenes_value_json[scenes_value_key]
            else:
                uuid_key = '%s_%s' % (uuid_type, scenes_key)
                ios_keychain_uuid[uuid_key] = scenes_value


def init_i18n(i18n_json, storage_host):
    """
    按语言初始化i18n内容
    :param i18n_json:
    :param storage_host:
    :return:
    """
    i18n_dict = {}
    for language_key in i18n_json:
        logger.debug(' init i18n language: %s ' % language_key)
        language_value = i18n_json[language_key]

        items_url = "%s/v0.8/items/%s/content" % (storage_host, language_value)
        items_json = get_data(items_url)
        i18n_dict[language_key] = items_json

    return i18n_dict


def download_xml_proguard(storage_host, factory_id, target_path):
    """
    下载xmls_old.xml和proguards.txt文件
    :param storage_host:
    :param factory_id:
    :param target_path:
    :return:
    """
    components_url = "%s/v0.8/apps/%s/components/xml" % (storage_host, factory_id)
    components_json = get_data(components_url)

    error_data = components_json['error']
    if error_data:
        error_message = 'get components xml failure: %s' % error_data
        logger.error(LoggerErrorEnum.INVALID_SERVER_RESPONSE, error_message)
        raise Exception(error_message)

    xml_data = components_json['xml']
    write_content_to_file(os.path.join(target_path, 'xmls_old.xml'), xml_data)

    proguard_data = components_json['proguard']
    write_content_to_file(os.path.join(target_path, 'proguards.txt'), proguard_data)


if __name__ == "__main__":
    target_path = os.path.join(os.getcwd(), 'target')
    app_build_path = os.path.join(target_path, 'defines.json')

    defines_json = Defines(target_path).defines_json()
    biz_comp_transform = BizCompJsonTransform('android')
    biz_comp_transform.make_property_map(defines_json)

    logger.debug('【xmlI18nPropertyMap】=%s' % biz_comp_transform.i18n_property_map)
    logger.debug('【xmlImagePropertyMap】=%s' % biz_comp_transform.image_property_map)

    app_pages_path = os.path.join(target_path, 'app_pages.json')
    content = read_file_content(app_pages_path)

    image_property_map = {}
    i18n_property_map = {}
    json_property_analysis = JsonPropertyAnalysis(biz_comp_transform)
    json_property_analysis.make_uuid_map(content, "app_pages", i18n_property_map, image_property_map)

    storage_host = 'http://app-native-storage.debug.web.nd'
    app_url = "%s/v0.8/apps/%s" % (storage_host, 'a411276d-a5a2-4977-a62f-b5d6d07a7627')

    app_json = get_data(app_url)
    i18n_json = app_json['i18n']
    i18n_dict = init_i18n(i18n_json, storage_host)

    content = replace_i18n("app_pages", content, i18n_dict, 'zh-CN', i18n_property_map, image_property_map)
    logger.debug(image_property_map)