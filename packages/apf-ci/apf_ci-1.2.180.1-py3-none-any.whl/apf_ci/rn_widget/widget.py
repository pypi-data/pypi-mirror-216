#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
React native widget module.
"""

__author__ = 'LianGuoQing'

import os
import sys
import json
import re
import subprocess
import platform

from apf_ci.util.file_utils import read_file_content, write_content_to_file
from apf_ci.util.http_utils import post_for_array
from apf_ci.util.log_utils import logger

class ReactWidgetLocalBuilder:
    """The apf_ci build for react native widget"""

    __component_type_dict = {
        'ios': 'react-ios',
        'android': 'react-android'
    }

    def __init__(self, app_factory_path, target_path, app_type, default_language, lifecycle_host):
        self.app_factory_path = app_factory_path
        self.target_path = target_path
        self.app_type = app_type
        self.default_language = default_language
        self.lifecycle_host = lifecycle_host

    def handle_data(self, map, dependencies_dict, widgets_array, widgets_list, template):
        """
        组装widgets数据和pages下widgets节点数据，以及npm依赖信息
        :param map: 键值对集合，包含widget_name、stage、tag_name值
        :param dependencies_dict: npm依赖信息键值对集合，其中健为npm名称、值为npm版本
        :param widgets_array: 颗粒所依赖的组件信息集合（biz_name、namespace、npm、version）
        :param widgets_list: 颗粒所依赖的path、uri信息集合
        :param template: 对应的template值
        :return: 返回颗粒所依赖的组件信息数组
        """
        widget_dict = {}
        widget_dict['uri'] = template

        biz_id = template[template.find('react://') + 8:template.rfind('/')]
        namespace = biz_id[0:biz_id.rfind('.')]
        biz_name = biz_id[biz_id.rfind('.') + 1:]

        widget_name = map['widget_name']
        stage = map['stage']

        request_body_json = {}
        request_body_json['namespace'] = namespace
        request_body_json['name'] = biz_name
        request_body_json['tag_name'] = map['tag_name']
        request_body_json['stage'] = stage

        npm = self.get_npm(request_body_json, 'widgets', widget_name)
        if npm:
            dependencies_array = npm.split(':')
            dependencies_dict[dependencies_array[0]] = dependencies_array[1]
            widget_dict['path'] = dependencies_array[0]

        flag = False
        for widgets_json in widgets_array:
            old_namespace = widgets_json['namespace']
            old_biz_name = widgets_json['biz_name']
            old_version = widgets_json['version']
            old_npm = widgets_json['npm']

            if namespace == old_namespace and biz_name == old_biz_name and stage == old_version and npm == old_npm:
                flag = True
                break

        if flag is False:
            widgets_json = {}
            widgets_json['namespace'] = namespace
            widgets_json['biz_name'] = biz_name
            widgets_json['version'] = stage
            widgets_json['npm'] = npm
            widgets_array.append(widgets_json)

        widgets_list.append(widget_dict)

    def analysis_widgets(self, dependencies_dict, widgets_array, widgets_list, parent_id):
        """
        解析widgets.json文件，查找对应子颗粒信息
        :param dependencies_dict: npm依赖信息键值对集合，包括js_plugins
        :param widgets_array: 颗粒所依赖的组件信息集合（biz_name、namespace、npm、version）
        :param widgets_list: 颗粒所依赖的path、uri信息集合
        :param parent_id: 应的template值
        :return: 返回键值对集合，包含widget_name、stage、tag_name值
        """
        map = {}

        widgets_path = os.path.join(self.app_factory_path, self.default_language, 'pages', 'widgets.json')
        widgets_data = read_file_content(widgets_path)
        widgets_json = json.loads(widgets_data)

        for widgets_key in widgets_json:
            widget_json = widgets_json[widgets_key]
            # properties_json = widget_json['properties']
            #
            # if '_module_properties' in properties_json.keys():
            #     module_properties_json = properties_json['_module_properties']
            #     module_name = module_properties_json['name']
            #     if module_name:
            #         if 'datasource_interface' in module_properties_json.keys():
            #             datasource_interface_json = module_properties_json['datasource_interface']
            #             if datasource_interface_json.__len__() > 0:
            #                 npm_name = datasource_interface_json['name']
            #                 npm_version = datasource_interface_json['version']
            #                 if npm_name and npm_version:
            #                     js_plugin = {}
            #                     js_plugin[npm_name] = npm_version
            #
            #                     if 'js_plugins' in dependencies_dict:
            #                         js_plugins = dependencies_dict['js_plugins']
            #                         js_plugins[module_name] = js_plugin
            #                         dependencies_dict['js_plugins'] = js_plugins
            #                     else:
            #                         js_plugins = {}
            #                         js_plugins[module_name] = js_plugin
            #                         dependencies_dict['js_plugins'] = js_plugins
            #


            parent = widget_json['__parent']
            template = widget_json['template']

            if parent and parent == parent_id:

                logger.info('[INFO] 查找到__parentId=%s在widgets.json文件中对应的子颗粒' % parent_id)
                logger.info('对应template=%s' % template)
                self.get_js_plugin(widget_json, dependencies_dict)
                if template:
                    map_data = self.analysis_widgets(dependencies_dict, widgets_array, widgets_list, template)
                    self.handle_data(map_data, dependencies_dict, widgets_array, widgets_list, template)

            if template == parent_id:
                self.get_js_plugin(widget_json, dependencies_dict)
                map['tag_name'] = widget_json['tag_name']
                map['stage'] = widget_json['stage']
                map['widget_name'] = widget_json['widget_name']

        return map

    def get_js_plugin(self, widget_json, dependencies_dict):
        properties_json = widget_json['properties']
        if '_module_properties' in properties_json.keys():
            module_properties_json = properties_json['_module_properties']
            module_name = module_properties_json['name']
            if module_name:
                if 'datasource_interface' in module_properties_json.keys():
                    datasource_interface_json = module_properties_json['datasource_interface']
                    if datasource_interface_json.__len__() > 0:
                        npm_name = datasource_interface_json['name']
                        npm_version = datasource_interface_json['version']
                        if npm_name and npm_version:
                            js_plugin = {}
                            js_plugin[npm_name] = npm_version

                            if 'js_plugins' in dependencies_dict:
                                js_plugins = dependencies_dict['js_plugins']
                                js_plugins[module_name] = js_plugin
                                dependencies_dict['js_plugins'] = js_plugins
                            else:
                                js_plugins = {}
                                js_plugins[module_name] = js_plugin
                                dependencies_dict['js_plugins'] = js_plugins

    def get_page(self, id_npm_dependencies_dict, widgets_array, page_json, plugin_key):
        """
        封装pages节点信息，包括id、path、uri、widgets信息
        :param id_npm_dependencies_dict: npmDependencies节点信息，即健为页面id、值为npm依赖信息集合
        :param widgets_array: 颗粒所依赖的组件信息集合（biz_name、namespace、npm、version）
        :param page_json: 页面信息
        :param plugin_key: 插件key,ns:name
        :return: 返回pages节点信息
        """
        page_dict = {}
        dependencies_dict = {}

        page_name = page_json['page_name']
        id = page_name[0: page_name.find('/index.html')]
        page_dict['id'] = id

        _page_name = page_json['_page_name']
        #uri = 'react://com.nd.apf.react.native.widget/%s' % _page_name
        uri = 'plugin://'+plugin_key+'/%s' % _page_name
        page_dict['uri'] = uri
        page_dict['pluginKey']=plugin_key

        request_body_json = {}
        component_json = page_json['_component']
        request_body_json['namespace'] = component_json['namespace']
        request_body_json['name'] = component_json['name']
        request_body_json['tag_name'] = page_json['tag_name']
        request_body_json['stage'] = page_json['stage']

        npm = self.get_npm(request_body_json, 'pages', _page_name)
        if npm:
            dependencies_array = npm.split(':')
            dependencies_dict[dependencies_array[0]] = dependencies_array[1]
            page_dict['path'] = dependencies_array[0]

        widgets_list = []
        pattern = '^react://(.+)/(.+)$'
        properties_json = page_json['properties']
        for properties_key in properties_json:
            properties_item = properties_json[properties_key]
            if isinstance(properties_item, list):
                for item_json in properties_item:
                    for item_key in item_json:
                        item = item_json[item_key]
                        if isinstance(item, str):
                            if re.match(pattern, item) is not None:
                                map_data = self.analysis_widgets(dependencies_dict, widgets_array, widgets_list, item)
                                self.handle_data(map_data, dependencies_dict, widgets_array, widgets_list, item)
                                page_dict['widgets'] = widgets_list

        id_npm_dependencies_dict[id] = dependencies_dict
        return page_dict

    def get_npm(self, request_body_json, node_type, widget_name):
        """通过调用生命周期服务API获取npm信息"""
        npm = ''
        component_type = self.__component_type_dict[self.app_type]
        namespace = request_body_json['namespace']
        biz_name = request_body_json['name']
        prefix = '%s:%s:%s:' % (namespace, biz_name, widget_name)

        if node_type == 'widgets':
            service_name = 'widget'
            request_body_json['widget_name'] = widget_name
        elif node_type == 'pages':
            service_name = 'page'
            request_body_json['page_name'] = widget_name

        lifecycle_url = '%s/v0.1/lifecycle/services/%s/actions/defines' % (self.lifecycle_host, service_name)
        request_body_array = []
        request_body_array.append(request_body_json)
        response_body_json = post_for_array(lifecycle_url, request_body_array, False)

        for response_body_key in response_body_json:
            if response_body_key.startswith(prefix):
                node_json = response_body_json[response_body_key]
                widgets_json = node_json[node_type]
                widget_json = widgets_json[widget_name]
                _type = widget_json['_type']
                if _type == 'react':
                    if component_type in widget_json.keys():
                        react_json = widget_json[component_type]
                        npm = react_json['npm']

        logger.debug(' npm: %s' % npm)
        return npm

    def analysis_pages(self):
        """解析pages.json文件内容，找到符合RN颗粒的节点"""
        pages_path = os.path.join(self.app_factory_path, self.default_language, 'pages', 'pages.json')
        pages_data = read_file_content(pages_path)
        pages_json = json.loads(pages_data)

        #pattern = '^react://com.nd.apf.react.native.widget/(.+)$'
        pages_list = []
        pages_info_json = {}
        for pages_key in pages_json:
            id_npm_dependencies_dict = {}
            widgets_array = []

            page_json = pages_json[pages_key]
            template = page_json['template']
            plugin_key = page_json.get('__plugin_key','')
            pattern = '^react://'+plugin_key+'(.+)$'
            if re.match(pattern, template) is not None:
                logger.debug(' 匹配到满足正则表达式条件的template值：%s' % template)
                page_dict = self.get_page(id_npm_dependencies_dict, widgets_array, page_json, plugin_key)

                each_plugin_json = pages_info_json.get(plugin_key)
                if each_plugin_json is None:
                    each_plugin_json = {}
                each_of_pages = each_plugin_json.get('pages', [])
                each_of_pages.append(page_dict)
                each_plugin_json['pages'] = each_of_pages

                each_of_widgets = each_plugin_json.get('widgets', [])
                each_of_widgets = each_of_widgets + widgets_array
                each_plugin_json['widgets'] = each_of_widgets

                each_of_npmDependencies = each_plugin_json.get('npmDependencies', {})
                each_of_npmDependencies.update(id_npm_dependencies_dict)
                each_plugin_json['npmDependencies'] = each_of_npmDependencies

                pages_info_json[plugin_key] = each_plugin_json
            #pages_list.append(page_dict)

        if pages_info_json.__len__() > 0:
            pages_info_path = os.path.join(self.target_path, 'react_widget', 'config', 'pagesInfo.json')
            write_content_to_file(pages_info_path, json.dumps(pages_info_json, ensure_ascii=False))
            return True

        return False

    def execute_build(self, build_tool, git_repository, commit_id, is_dev, reset_cache, each_plugin_info):
        """
        Install build tools, and execute the build script.
        :param build_tool:
        :param git_repository:
        :param commit_id:
        :param is_dev:
        :param reset_cache:
        :return:
        """
        logger.info(' npm config set registry="http://registry.npm.sdp.nd/"')

        platform_name = platform.system()
        if platform_name == 'Windows':
            subprocess.call(['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"'], shell=True)

            if self.app_type == 'android':
                logger.info(' npm config set unsafe-perm true')
                subprocess.call(['npm', 'config', 'set', 'unsafe-perm', 'true'], shell=True)

            logger.info(" npm install %s" % build_tool)
            subprocess.call(['npm', 'install', build_tool], shell=True)
        else:
            self.execute_command(['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"'])

            if self.app_type == 'android':
                logger.info(' npm config set unsafe-perm true')
                self.execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'])

            logger.info(" npm install %s" % build_tool)
            self.execute_command(['npm', 'install', build_tool])

        # logger.info(" yarn add %s" % build_tool)
        # subprocess.call(['yarn', 'add', build_tool], shell=True)

        each_plugin_path = os.path.join(self.target_path, 'react_widget', each_plugin_info)
        if not os.path.exists(each_plugin_path):
            os.makedirs(each_plugin_path)
        os.chdir(each_plugin_path)

        js_name = './../node_modules/@sdp.nd/react-native-widget-builder/index.js'
        logger.info(" node %s --gitRepository %s --commitId %s --platform %s --dev %s --reset-cache %s --pluginDir %s"
              % (js_name, git_repository, commit_id, self.app_type, is_dev, reset_cache, each_plugin_info))

        self.execute_command(['node', js_name,
                         '--gitRepository', git_repository,
                         '--commitId', commit_id,
                         '--platform', self.app_type,
                         '--dev', is_dev,
                         '--reset-cache', reset_cache,
                         '--pluginDir', each_plugin_info])

    def execute_command(self, popenargs):
        popen = subprocess.Popen(popenargs, stdout=subprocess.PIPE, universal_newlines=True ,encoding='UTF-8')
        while True:
            next_line = popen.stdout.readline()
            if next_line == '' and popen.poll() != None:
                break
            sys.__stdout__.write(next_line)
            sys.__stdout__.flush()
