#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import get_data
from apf_ci.util.log_utils import logger

def get_languages(storage_host, factory_id):
    """
    调用存储服务API获取应用的语言
    :param storage_host:
    :param factory_id:
    :return: 返回语言数组
    """
    languages_url = "%s/v0.8/apps/%s/languages" % (storage_host, factory_id)
    return get_data(languages_url)['languages']

def get_language_tree(resource_host):
    language_tree_url = "%s/v0.1/resconfig/language/tree" % resource_host
    return get_data(language_tree_url)

def get_all_languages(resource_host):
    """
    调用资源服务API获取所有语言的信息
    :param resource_host:
    :return:
    """
    all_languages_url = "%s/v0.1/resconfig/language" % resource_host
    return get_data(all_languages_url)

def get_default_language(languages_array, language_tree_array):
    language_weight_dict = {}

    for language_tree_json in language_tree_array:
        if language_tree_json['hidden'] is False:
            language_weight_dict[language_tree_json['name']] = int(language_tree_json['weight'])

    weight = -1
    default_language = ''
    for languages in languages_array:
        if weight == -1 or language_weight_dict[languages] < weight:
            weight = language_weight_dict[languages]
            default_language = languages

    return default_language

def language_i18n(languages_array, all_languages_array):
    lang_display_name_map = {}
    lang_alias_name_map = {}

    for language_json in all_languages_array:
        name = language_json['name']
        lang_display_name_map[name] = language_json['display']
        lang_alias_name_map[name] = language_json['alias']

    lang_array = []
    i18n_json = {}
    for language_name in languages_array:
        display_name = lang_display_name_map[language_name]
        i18n_json[language_name] = display_name

        lang_json = {}
        lang_json['name'] = language_name
        lang_json['display'] = display_name
        lang_json['alias'] = lang_alias_name_map[language_name]
        lang_array.append(lang_json)

    return lang_array, i18n_json

def language_weight_parent_list(language_tree_array):
    language_weight_map = {}
    language_parent_map = {}
    language_list = []

    for language_tree_json in language_tree_array:
        name = language_tree_json['name']

        language_weight_map[name] = int(language_tree_json['weight'])
        language_parent_map[name] = language_tree_json['parent']

        alias_json = language_tree_json['alias']
        if alias_json['android']:
            language = {}
            language['display'] = language_tree_json['display']
            language['name'] = name
            language['alias'] = alias_json
            language_list.append(language)

    return language_weight_map, language_parent_map, language_list

def language_enable_parent(languages_array, language_weight_map, language_parent_map):
    language_enable_map = {}
    language_enable_parent_map = {}

    for language_enable in languages_array:
        language_enable_map[language_enable] = language_weight_map[language_enable]

        parent = language_parent_map[language_enable]
        if parent != 'language':
            # 当父节点不是language，即还不是根节点
            language_enable_parent_map[parent] = 1

    return language_enable_map, language_enable_parent_map

def language_groups(language_enable_parent_map, language_parent_map, language_weight_map):
    language_groups_list = []

    for language_enable_parent in language_enable_parent_map:
        language_group = {}

        for language_parent in language_parent_map:
            if language_parent_map[language_parent] == language_enable_parent:
                language_group[language_parent] = language_weight_map[language_parent]

        language_groups_list.append(sort_by_value(language_group))

    return language_groups_list

def get_language_default_json(sort_language_enables, language_parent_map,app_json):
    language_default_json = {}
    language_default_json['default'] = sort_language_enables[0]
    i18n_default = ''
    if 'i18n_default' in app_json:
        i18n_default = app_json['i18n_default']
        logger.debug(' i18n_default: %s' % i18n_default)
    if i18n_default != '' and 'i18n_default' != 'null' and i18n_default in sort_language_enables:
            language_default_json['default'] = i18n_default
    for sort_language_enable in sort_language_enables:
        traverse_default_language(language_parent_map, sort_language_enable, sort_language_enable, language_default_json)

    return language_default_json

def traverse_default_language(language_parent_map, sort_language_enable, language_enable, language_default_json):
    language_enable_parent = language_parent_map[sort_language_enable]

    if language_enable_parent == '':
        logger.debug('【语言新规】%s parent is blank!' % sort_language_enable)
        return

    if language_enable_parent == 'language':
        logger.debug('【语言新规】%s parent is language!' % sort_language_enable)
        return

    language_default_json[language_enable_parent] = language_enable
    traverse_default_language(language_parent_map, language_enable_parent, language_enable, language_default_json)

def sort_by_value(map):
    items = map.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]







