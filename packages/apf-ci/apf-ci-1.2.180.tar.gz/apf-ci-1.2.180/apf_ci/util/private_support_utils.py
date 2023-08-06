#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from apf_ci.app_init.utils.build_config_utils import BuildConfig, parse_private_host, get_app_factory_deploy_host
from apf_ci.util.log_utils import logger
from apf_ci.util.file_utils import read_file_content, write_content_to_file


def support_private_host(build_config_json, app_json):
    # 部分私有化环境的包，部分host,转换成私有化环境
    # 获取支持的环境
    need_private_env_keyset = build_config_json["need_private_env_keyset"]
    if 'env_client' in app_json:
        if app_json['env_client'] in need_private_env_keyset:
            workspace_path = os.getcwd()
            parse_app_json_private_host(build_config_json, app_json)
            parse_assets_private_host(build_config_json, app_json, workspace_path)
        else:
            logger.debug("%s 环境不需要私有化处理" % app_json['env_client'])


def parse_app_json_private_host(build_config_json, app_json):
    logger.debug("部分私有化环境的包，部分host,转换成私有化环境")
    app_json_private_keyset = build_config_json["app_json_private_keyset"]
    deploy_host_json = get_app_factory_deploy_host(build_config_json)
    for private_key in app_json_private_keyset:
        if private_key in app_json:
            parse_private_host(deploy_host_json, app_json, app_json['env_client'], private_key)
            logger.debug(" app_json[%s]:%s" % (private_key, app_json[private_key]))


def parse_assets_private_host(build_config_json, app_json, workspace_path):
    # 将assets目录下 announce.json 和 components.json 里的 轻应用相关host  转换成私有化环境
    logger.debug("components.json里的轻应用相关host转换成私有化环境")
    env_client = app_json['env_client']
    deploy_host_json = get_app_factory_deploy_host(build_config_json)
    if 'private_light_cs_host' not in deploy_host_json:
        return
    private_light_cs_host = deploy_host_json['private_light_cs_host']
    # 注意这里是 https://cs.101.com/v0.1/static/release_package_repository  ，后期如果存入的有变动，这里可能要调整
    default_cs_prefix = get_cs_prefix(private_light_cs_host, 'default')
    private_cs_prefix = get_cs_prefix(private_light_cs_host, env_client)
    if private_cs_prefix == '':
        logger.warning("private_light_cs_host 不存在对应私有化环境配置,请配置！！！")
        return

    components_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/components.json")
    components_content = read_file_content(components_file_path)
    components_content = replace_cs_prefix(components_content, default_cs_prefix, private_cs_prefix)
    write_content_to_file(components_file_path, components_content)

    announce_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/announce.json")
    announce_content = read_file_content(announce_file_path)
    announce_content = replace_cs_prefix(announce_content, default_cs_prefix, private_cs_prefix)
    write_content_to_file(announce_file_path, announce_content)


def get_cs_prefix(private_light_cs_host, env):
    # 返回对应环境的，轻应用cs地址前缀,如 https://cs.101.com/v0.1/static/release_package_repository
    if env not in private_light_cs_host:
        return ''
    return private_light_cs_host[env]['host'] + '/static/' + private_light_cs_host[env]['server_name']


def replace_cs_prefix(content, default_cs_prefix, private_cs_prefix):
    # 支持生产环境不同情况的
    content = content.replace(default_cs_prefix, private_cs_prefix)
    if 'https://cs.101.com' in default_cs_prefix:
        return content.replace(default_cs_prefix.replace('https://cs.101.com', 'http://cs.101.com'), private_cs_prefix) \
            .replace(default_cs_prefix.replace('https://cs.101.com', 'http://gcdncs.101.com'), private_cs_prefix) \
            .replace(default_cs_prefix.replace('https://cs.101.com', 'https://gcdncs.101.com'), private_cs_prefix) \
            .replace(default_cs_prefix.replace('https://cs.101.com', 'http://cdncs.101.com'), private_cs_prefix) \
            .replace(default_cs_prefix.replace('https://cs.101.com', 'https://cdncs.101.com'), private_cs_prefix)
    return content