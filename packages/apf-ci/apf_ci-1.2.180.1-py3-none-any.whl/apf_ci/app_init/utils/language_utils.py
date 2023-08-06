#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用语言相关配置
"""
from apf_ci.config.runtime import Runtime
from apf_ci.config.json_property_analysis import JsonPropertyAnalysis
from apf_ci.config.page_i18n_utils import *
from apf_ci.config.widget_i18n_utils import *
from apf_ci.config.h5_widget_i18n_utils import filter_h5_widget_uuid
from apf_ci.config.properties_transform import *
from apf_ci.config.widget_tree import WidgetTree
from apf_ci.config.defines import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import BuildConfig

__author__ = '370418'

MAPPING_APPS = "/v0.8/apps"
MAPPING_ITEMS = "/v0.8/items"
MAPPING_DEFINE = "/v0.8/define"
APP_FACTORY_PATH = "/app/assets/app_factory"
NAMESPACE_BIZNAME = "com.nd.apf.h5:widget"

APP_FACTORY_MAIN_NAMESPACE = "com.nd.smartcan.appfactory"
APP_FACTORY_MAIN_NAME = "main_component"

# key_path_dict 子应用和轻应用有区别，这里都统一输出，后续放到key_path_dict_target中
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
    'plugin': 'components',
    'android_config_data': 'components'
}
# 后续应用初始化步骤中，都不过度处理相关文件，放置到target目录下，替换多语言后就交由各端自己处理
# 注意 支持多语言的 需要配置到 key_path_dict_need_i18n ！！！,否则只替换成中文
key_path_dict_target = {
    'permission_config_data': 'components',
    'custom_permission_config_data': 'components',
    'android_permission_use_record': 'app',
    'local_h5_config': 'app'
}
# 有需要全文件做国际化处理的文件需要这里加入这里，否则只做有声明国际化部分中文替换
key_path_dict_need_i18n = [
    'config',
    'ios_extension',
    'custom_permission_config_data',
    'permission_config_data'
]


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


def get_languages(storage_host, factory_id):
    """
    调用存储服务API获取应用的语言
    :param storage_host:
    :param factory_id:
    :return: 返回语言数组
    """
    languages_url = "%s/v0.8/apps/%s/languages" % (storage_host, factory_id)
    return get_data(languages_url)['languages']


def get_all_languages(resource_host):
    """
    调用资源服务API获取所有语言的信息
    :param resource_host:
    :return:
    """
    all_languages_url = "%s/v0.1/resconfig/language" % resource_host
    return get_data(all_languages_url)


def get_default_language(resource_host, languages_json, app_json):
    i18n_default = ''
    if 'i18n_default' in app_json:
        i18n_default = app_json['i18n_default']
    logger.debug(' i18n_default: %s' % i18n_default)
    # 配置的默认语言必须在可用语言内，才能使用
    if i18n_default != '' and 'i18n_default' != 'null' and i18n_default in languages_json:
        return i18n_default

    lang_tree_url = resource_host + "/v0.1/resconfig/language/tree"
    lang_tree_body = get_data(lang_tree_url)
    lang_tree_data = {}
    for item in lang_tree_body:
        if not item['hidden']:
            lang_tree_data[item['name']] = item['weight']

    weight = -1
    default_lang = ''
    for item in languages_json:
        if weight == -1 or lang_tree_data[item] < weight:
            weight = lang_tree_data[item]
            default_lang = item

    logger.debug(' default_lang: %s' % default_lang)
    return default_lang


def download_app_json_define(storage_host, factory_id):
    define_url = storage_host + MAPPING_DEFINE + "/" + factory_id
    defnie_body = get_data(define_url)
    define_data = defnie_body['data']
    return define_data


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


def parse_app_json_define(define_data, target_path):
    # 解析/target/defines.json文件中应用框架的git模板，并保存到/target/git_templates.json中
    prefix = APP_FACTORY_MAIN_NAMESPACE + ":" + APP_FACTORY_MAIN_NAME
    templates = ''
    for key in define_data:
        if key.startswith(prefix):
            item = define_data[key]
            if item:
                extensions = item['extensions']
                if extensions:
                    templates = extensions['templates']
            break
    if templates and templates != '':
        write_content_to_file(os.path.join(target_path, 'git_templates.json'), json.dumps(templates))
        logger.debug(' 保存到/target/git_templates.json文件中')


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

        #if key.lower() == 'config' or key.lower() == 'ios_extension'or key.lower() == 'permission_config_data':
        # 只有 key_path_dict_need_i18n 里的才做国际化处理，其他只替换为中文
        if key in key_path_dict_need_i18n:
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


def download_json_file(key, language, item_json, i18n_dict, biz_comp_transform,
                       image_property_map, com_test_type, envtarget, environment_dict,
                       ios_permitsion_dict, app_name_dict, app_type, defines_json,
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
    if key in key_path_dict:
        path = key_path_dict[key]
    elif key in key_path_dict_target:
        path = key_path_dict_target[key]

    if path == '':
        return ''

    app_factory_path = os.path.join(os.getcwd(), 'app', 'assets', 'app_factory')
    target_app_factory_path = os.path.join(os.getcwd(), 'target', 'app_factory')
    if path == 'app':
        path_dir = os.path.join(app_factory_path, path)
        target_path_dir = os.path.join(target_app_factory_path, path)
    else:
        path_dir = os.path.join(app_factory_path, language, path)
        target_path_dir = os.path.join(target_app_factory_path, language, path)

    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
        os.makedirs(target_path_dir)

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

        logger.debug(' env【%s】envtarget【%s】' % (env, envtarget))

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
            logger.debug(' ios_extension替换前：' + content_temp)

            content_temp = replace_i18n(key, content_temp, i18n_dict, language)
            logger.debug(' ios_extension替换后：' + content_temp)

            content_json = json.loads(content_temp)

            move_privacy_to_i18n(content_json, ios_keychain_uuid,
                                 ios_keychain_i18n, ios_keychain_file_type, languages_array, i18n_dict, language,
                                 ios_keychain_default, default_language)

            ios_extension_path = os.path.join(os.getcwd(), 'target', 'ios_extension.json')
            write_content_to_file(ios_extension_path, json.dumps(content_json))
            logger.debug('创建文件: %s' % ios_extension_path)

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
        # 补充h5颗粒国际化资源的获取
        i18n_property_map_h5 = filter_h5_widget_uuid(template_dict, defines_json, biz_comp_transform)
        i18n_property_map.update(i18n_property_map_h5)
        for page_id in template_dict:
            page = template_dict[page_id]
            template_data = json.dumps(page)
            value = replace_i18n(key, template_data, i18n_dict, language, i18n_property_map, {})
            template_dict[page_id] = json.loads(value)

        content = json.dumps(template_dict)
        file_name = 'widgets.json'
    else:
        content = replace_i18n(key, content, i18n_dict, language)

    file_path = os.path.join(path_dir, file_name)
    target_file_path = os.path.join(target_path_dir, file_name)
    # 只有旧的文件，是直接在这里写入，并存入app目录，后续新增文件只会在target目录下
    if key in key_path_dict:
        write_content_to_file(file_path, content)
        logger.debug(' create file %s success: %s ' % (file_name, file_path))
    write_content_to_file(target_file_path, content)
    logger.debug(' create file %s success: %s ' % (file_name, target_file_path))
    return ''


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
                    elif default_language in ios_keychain_default:
                        ios_keychain_default_each_language_json = ios_keychain_default[default_language]
                    else:
                        ios_keychain_default_each_language_json = ios_keychain_default["zh-CN"]
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
            detail_key = scenes_key + "_detail"
            if detail_key in scenes_json:
                scenes_json.pop(detail_key)


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
    try:
        app_pages_array = json.loads(app_pages_data)
    except Exception:
        error_msg = '%s 转换成json  异常，请用json校验工具排查具体错误位置和原因' % app_pages_path
        logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_msg)

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
    logger.debug(' create pages.json file: %s ' % pages_path)


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

    app_pages_path = os.path.join(app_language_path, 'pages', 'pages.json')
    logger.info('替换page.json开始：%s' % app_pages_path)
    app_pages_data = read_file_content(app_pages_path)
    #读取设备iamge size mode配置
    build_config = BuildConfig(os.path.join(os.getcwd(), 'target'))
    build_config_json = build_config.read_build_config()
    device_image_size_mode = build_config_json['device_image_size_mode']
    logger.debug('device_image_size_mode：%s' % device_image_size_mode)

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


def update_component_version(app_factory_path, language, biz_component_mng):
    """
    更新 components/build.json 里的versionNumber 参数为最新，解决编辑器不重新保存，版本信息不会更新的问题
    """
    app_build_path = os.path.join(app_factory_path, language, 'components', 'build.json')
    if os.path.exists(app_build_path):
        app_build_data = read_file_content(app_build_path)
        app_build_json = json.loads(app_build_data)
        # 拼接查询的组件参数
        coms = ""
        for data in app_build_json:
            component_tag = "%s:%s:%s" % (data["component"]["namespace"], data["component"]["name"], data["version"])
            coms = coms + component_tag + ","

        # 获取组件对应的信息
        get_components_url = biz_component_mng + 'v1.0/bizs/versions?isGetTagName=true'
        post_body = {}
        post_body['comps'] = coms
        resp = post_for_array(get_components_url, post_body)
        resp_map = {}
        for resp_item in resp:
            component_key = resp_item['namespace'] + '.' + resp_item['biz_name']
            resp_map[component_key] = resp_item

        # 更新版本信息
        for data in app_build_json:
            component_tag = "%s.%s" % (data["component"]["namespace"], data["component"]["name"])
            if component_tag in resp_map.keys():
                try:
                    data["versionNumber"] = resp_map[component_tag]["lifecycle"]["versionNumber"]
                except:
                    pass
        write_content_to_file(app_build_path, json.dumps(app_build_json))