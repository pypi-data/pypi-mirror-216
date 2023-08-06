#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IOS keychain 初始化
target/keychain_i18n.json 、target/keychain_file_type.json两文件
"""

__author__ = '370418'

import os
import json
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *

def init_ios_keychain_biz(key_chain_namespace, key_chain_bizname,
                          variable_dict, target_path, ios_keychain_i18n, ios_keychain_file_type):
    biz_comp_mng_host = variable_dict['biz_component_mng']
    biz_defines_dict = get_biz_define(biz_comp_mng_host, key_chain_namespace, key_chain_bizname)

    biz_ios_keychain_define_path = os.path.join(target_path, 'biz_ios_keychain_define.json')
    write_content_to_file(biz_ios_keychain_define_path, json.dumps(biz_defines_dict))
    logger.debug('[INFO] 创建文件: %s' % biz_ios_keychain_define_path)

    properties_json = biz_defines_dict['properties']


    get_i18n_map_and_file_type(properties_json, ios_keychain_i18n, ios_keychain_file_type)

    keychain_i18n_path = os.path.join(target_path, 'keychain_i18n.json')
    write_content_to_file(keychain_i18n_path, json.dumps(ios_keychain_i18n))
    logger.debug('[INFO] 创建文件: %s' % keychain_i18n_path)

    keychain_file_type_path = os.path.join(target_path, 'keychain_file_type.json')
    write_content_to_file(keychain_file_type_path, json.dumps(ios_keychain_file_type))
    logger.debug('[INFO] 创建文件: %s' % keychain_file_type_path)

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