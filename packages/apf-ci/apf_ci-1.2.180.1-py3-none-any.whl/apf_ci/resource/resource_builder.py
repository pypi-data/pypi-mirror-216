#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
资源配置业务处理模块
"""

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *
#from apf_ci.config.android_plugin import *


class ResourceConfig:
    def __init__(self, workspace_path):
        self.workspace_path = workspace_path

    def delete_xml(self):
        xml_path = os.path.join(self.workspace_path, 'app', 'res', 'values', 'strings_ci_not_copy.xml')
        if os.path.exists(xml_path):
            logger.info(' 开始删除/app/res/values/strings_ci_not_copy.xml')
            os.remove(xml_path)
            logger.info(' 删除/app/res/values/strings_ci_not_copy.xml成功')

    def init_bizs_version(self, target_build_path):
        biz_version_map = {}

        build_data = read_file_content(target_build_path)
        build_json_array = json.loads(build_data)
        for build_json in build_json_array:
            component_json = build_json['component']
            namespace = component_json['namespace']
            name = component_json['name']
            biz = '%s:%s' % (namespace, name)
            biz_version_map[biz] = build_json['version']

        return biz_version_map

    def init_environment_resource(self, resource_host):
        environment_resource_map = {}
        environment_name_map = {}

        environment_config_url = '%s/v0.1/resconfig/environment' % resource_host
        environment_config_array = get_data(environment_config_url)

        if environment_config_array.__len__() == 0:
            error_msg = '构建失败，所有资源类型获取失败 url=%s' % environment_config_url
            logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_msg)
            raise Exception()

        for environment_config_json in environment_config_array:
            alias_json = environment_config_json['alias']
            key = alias_json['android']
            environment_resource_map[key] = environment_config_json['id']
            environment_name_map[key] = environment_config_json['name']

        return environment_resource_map, environment_name_map

    def init_each_environment_bizs(self, biz_env_path, plugin_path, biz_version_map, environment_resource_map, env,
                                   environment_name_map):
        each_environment_bizs_map = {}
        plugin_env_map = {}
        plugin_version_map = {}

        if os.path.exists(plugin_path):
            logger.info(' 解析plugin.json文件中动态数据源的插件,获取插件版本')
            plugins_data = read_file_content(plugin_path)
            plugins_json = json.loads(plugins_data)

            for plugin_json in plugins_json.values():
                if 'plugin' in plugin_json:
                    plugin = plugin_json['plugin']
                    version = plugin_json['version']
                    namespace = plugin['namespace']
                    biz_name = plugin['biz_name']
                    plugin_key = '%s:%s' % (namespace, biz_name)
                    plugin_version_map[plugin_key] = version
                    logger.debug('init_each_environment_bizs：' + plugin_key + ' = ' + version)

        if os.path.exists(biz_env_path):
            bizs_env_data = read_file_content(biz_env_path)
            bizs_env_array = json.loads(bizs_env_data)

            for biz_env_json in bizs_env_array:
                component_json = biz_env_json['component']
                namespace = component_json['namespace']
                biz_name = component_json['name']
                version = biz_env_json['env']
                key = '%s:%s' % (namespace, biz_name)

                if version == '':
                    version = env
                if biz_env_json['type'] == 'plugin':
                    plugin_env_map[key] = environment_name_map[version]
                    if key not in plugin_version_map.keys():
                        continue
                    bizOrPluginVersion = plugin_version_map[key]
                else:
                    if key not in biz_version_map.keys():
                        continue
                    bizOrPluginVersion = biz_version_map[key]

                # logger.debug('bizOrPluginVersion：' + bizOrPluginVersion)
                bizs_list = []
                environment_id = environment_resource_map[version]
                if environment_id in each_environment_bizs_map:
                    bizs_list = each_environment_bizs_map[environment_id]

                bizs_list.append(key + ':' + bizOrPluginVersion)
                each_environment_bizs_map[environment_id] = bizs_list
                # logger.debug('pop before：' + key)
                if biz_env_json['type'] == 'plugin':
                    plugin_version_map.pop(key)
                else:
                    biz_version_map.pop(key)
                    # logger.debug('pop after：' + key)

        if biz_version_map.__len__() > 0:
            bizs_list = []
            environment_id = environment_resource_map[env]

            if environment_id in each_environment_bizs_map:
                bizs_list = each_environment_bizs_map[environment_id]

            for bizs in biz_version_map:
                bizs_list.append(bizs + ':' + biz_version_map[bizs])

            each_environment_bizs_map[environment_id] = bizs_list

        if plugin_version_map.__len__() > 0:
            bizs_list = []
            environment_id = environment_resource_map[env]

            if environment_id in each_environment_bizs_map:
                bizs_list = each_environment_bizs_map[environment_id]

            for bizs in plugin_version_map:
                bizs_list.append(bizs + ':' + plugin_version_map[bizs])

            each_environment_bizs_map[environment_id] = bizs_list

        plugin_env_map['default'] = environment_name_map[env]
        logger.debug('init_each_environment_bizs done')
        return each_environment_bizs_map, plugin_env_map


    def create_service_json(self, each_environment_bizs_map, resource_host, app_factory_path):
        app_service_array = []

        for environment_id in each_environment_bizs_map:
            resource_service_url = '%s/v0.1/default/batch/%s' % (resource_host, environment_id)

            params = {}
            bizs_list = each_environment_bizs_map[environment_id]
            params['comps'] = ','.join(bizs_list)

            resource_json_array = post_for_array(resource_service_url, params, False)
            resource_size = resource_json_array.__len__()
            logger.debug('应用组件资源大小为:【 %s 】' % resource_size)

            for resource_json in resource_json_array:
                namespace = resource_json['namespace']
                biz_name = resource_json['biz_name']

                if 'items' in resource_json:
                    items_array = resource_json['items']

                    if items_array.__len__() > 0:
                        item_json = items_array[0]

                        if 'resource_url' in item_json:
                            resource_url = item_json['resource_url']
                            if resource_url:
                                resource_data = read_cs_content(resource_url)
                                resource_json = json.loads(resource_data)

                                comp_json = {}
                                comp_json['namespace'] = namespace
                                comp_json['name'] = biz_name

                                comp_service_json = {}
                                comp_service_json['component'] = comp_json
                                comp_service_json['properties'] = resource_json

                                app_service_array.append(comp_service_json)

        service_path = os.path.join(app_factory_path, 'app', 'service.json')
        write_content_to_file(service_path, json.dumps(app_service_array))
        logger.info(' service.json文件成功：%s' % service_path)

    def create_datasources_json(self, app_factory_path, default_language, plugin_env_map, resource_host):
        datasource_name_array = []

        plugin_path = os.path.join(app_factory_path, default_language, 'components', 'plugin.json')
        if os.path.exists(plugin_path):
            logger.info(' 正在解析plugin.json文件中动态数据源的插件名')

            plugins_data = read_file_content(plugin_path)
            plugins_json = json.loads(plugins_data)

            for plugin_json in plugins_json.values():
                if 'plugin' in plugin_json:
                    plugin = plugin_json['plugin']
                    version = plugin_json['version']
                    namespace = plugin['namespace']
                    biz_name = plugin['biz_name']

                    environment_name = plugin_env_map['default']
                    key = '%s:%s' % (namespace, biz_name)
                    if key in plugin_env_map:
                        if plugin_env_map[key]:
                            environment_name = plugin_env_map[key]

                    datasource_url = '%s/v0.1/custom/env/%s/%s/%s/environment?name=%s' % (
                        resource_host, namespace, biz_name, version, environment_name)
                    datasource_constant_json = self._get_datasource_constant(datasource_url, biz_name)
                    datasource_name_array.append(datasource_constant_json)

        datasources_path = os.path.join(app_factory_path, 'app', 'datasources.json')
        logger.info(' 正在创建datasources.json文件：%s' % datasources_path)
        write_content_to_file(datasources_path, json.dumps(datasource_name_array))

    def create_page_controller_json(self, app_factory_path, app_pages_path, is_sub):
        logger.info(' 正在解析app_pages.json：%s' % app_pages_path)
        app_pages_data = read_file_content(app_pages_path)
        app_pages_array = json.loads(app_pages_data)

        plugins_id_list = []
        plugins_not_id_list = []
        for app_pages_json in app_pages_array:
            if app_pages_json['__type'] == 'plugin':
                plugin_param_json = app_pages_json['__plugin_param']

                plugin_json = {}
                plugin_json['template'] = app_pages_json['template']
                plugin_json['plugin_template'] = app_pages_json['plugin_template']
                plugin_json['plugin_page'] = app_pages_json['__plugin_page']
                plugin_json['plugin_param'] = plugin_param_json
                # plugin_json['plugin_page_path'] = app_pages_json['__plugin_page_path']

                if 'id' in plugin_param_json:
                    plugins_id_list.append(plugin_json)
                else:
                    plugins_not_id_list.append(plugin_json)

        # 优先按plugin_param中有id属性排序，然后按plugin_param参数个数降序排序
        plugins_id_list = sorted(plugins_id_list, key=lambda plugins_json: plugins_json['plugin_param'].__len__(),
                                 reverse=True)
        plugins_not_id_list = sorted(plugins_not_id_list,
                                     key=lambda plugins_json: plugins_json['plugin_param'].__len__(), reverse=True)
        plugins_list = plugins_id_list + plugins_not_id_list

        page_controller_json = {}
        for plugin_json in plugins_list:
            page_json_array = []
            name = plugin_json['plugin_template']
            logger.debug(' plugin name=' + name)
            if '?' in name:
                name = name[0:name.index('?')]
            if name in page_controller_json:
                page_json_array = page_controller_json[name]

            match_json = {}
            plugin_param_json = plugin_json['plugin_param']
            for plugin_param_key in plugin_param_json:
                match_json[plugin_param_key] = plugin_param_json[plugin_param_key]

            page_json = {}
            page_json['match'] = match_json
            page_json['page'] = plugin_json['template']

            page_json_array.append(page_json)
            page_controller_json[name] = page_json_array

        page_controller_path = os.path.join(app_factory_path, 'app', 'page_controller.json')
        logger.info(' 正在创建page_controller.json文件：%s' % page_controller_path)
        write_content_to_file(page_controller_path, json.dumps(page_controller_json, ensure_ascii=False))

    def _get_datasource_constant(self, datasource_url, biz_name):
        datasource_json = get_data(datasource_url)
        logger.debug(' 获取数据源插件常量：%s' % datasource_json)

        constant_json = {}
        items_json_array = datasource_json['items']
        for items_json in items_json_array:
            config_json = items_json['config']
            constant_json = dict(constant_json, **config_json)

        datasource_constant_json = {}
        datasource_constant_json['plugin_id'] = biz_name
        datasource_constant_json['properties'] = constant_json

        return datasource_constant_json


