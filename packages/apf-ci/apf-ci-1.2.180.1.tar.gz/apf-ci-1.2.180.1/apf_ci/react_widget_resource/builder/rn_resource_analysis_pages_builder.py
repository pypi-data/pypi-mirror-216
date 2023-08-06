#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
继承rn_widget的AnalysisPagesBuilder。部分方法复用
"""

import re

from apf_ci.rn_widget.builder.analysis_pages_builder import AnalysisPagesBuilder
from apf_ci.rn_widget.model.page import Page
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *


class RnResourceAnalysisPages(AnalysisPagesBuilder):

    def __init__(self, storage_host, lifecycle_host, factory_id, component_type, load_comp_list):
        super(RnResourceAnalysisPages, self).__init__(storage_host, lifecycle_host, factory_id, component_type,
                                                      load_comp_list)
        self.storage_host = storage_host
        self.lifecycle_host = lifecycle_host
        self.factory_id = factory_id
        self.component_type = component_type
        self.load_comp_list = load_comp_list

    def perform(self, variables_json):
        language_array = variables_json["languages"]

        workspace_path = os.getcwd()

        language_arr = self._get_language(workspace_path, language_array, variables_json)
        first_language = ""
        if language_arr is not None and language_arr != []:
            first_language = str(language_arr[0])
        logger.info(" 默认第一个语言 firstLanguage: %s" % first_language)
        result = self.analysis_pages(workspace_path, first_language, language_arr, self.load_comp_list, variables_json)

        if result == "FAILTURE":
            return False

        # 所依赖的颗粒放入全局变量中，值可能会为EMPTY，需排除
        variables_json["pagesResult"] = result
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
        return True

    def analysis_pages(self, workspace_path, first_language, language_arr, load_comp_list, variables_json):
        """
        解析pages.json 返回package.json内容 （str）
        :param workspace_path:
        :param first_language:
        :param language_arr:
        :param load_comp_list:
        :param variables_json:
        :return:
        """
        pages_file_path = os.path.join(workspace_path, "target/app_component_pages/${TAG_LANGUAGE}/pages.json")
        pages_file_path = pages_file_path.replace("${TAG_LANGUAGE}", first_language)
        logger.info(" 正在读取pages.json文件: %s" % pages_file_path)

        return_json = {}
        if not os.path.exists(pages_file_path):
            logger.info(" pages.json文件不存在: %s" % pages_file_path)
            return "FAILTURE"

        pages_json_str = read_file_content(pages_file_path)
        pages_json_obj = json.loads(pages_json_str)

        # 解析page.json文件中满足条件的节点，循环节点
        for pages_json_key in pages_json_obj:
            node_json_obj = pages_json_obj[pages_json_key]

            template = node_json_obj.get("template")
            plugin_key = node_json_obj.get("__plugin_key", "")
            if template is not None:
                regex = "^react://%s/(.*)$" % plugin_key
                matcher = re.findall(regex, template)
                if len(matcher) > 0:
                    logger.debug(" 匹配到满足正则表达式 %s 条件的template值: %s" % (regex, template))
                    last_dot = plugin_key.rfind(".")
                    plugin_ns = plugin_key[:last_dot]
                    plugin_name = plugin_key[last_dot + 1:]
                    plugin_component_id = plugin_ns + ":" + plugin_name

                    pages = []
                    # 页面id 所以来的npm集合
                    id_npm_dependencies_map = {}
                    dependencies_json = {}
                    # 所依赖的颗粒集合
                    widgets_arr = []
                    page = self.get_page(dependencies_json, widgets_arr, workspace_path, node_json_obj,
                                          first_language, plugin_key, variables_json)

                    if load_comp_list != []:
                        flag = False
                        for earch_load_comp in load_comp_list:
                            if earch_load_comp.startswith(plugin_component_id + ":"):
                                flag = True
                                break
                        if not flag:
                            continue
                    each_plugin_json = return_json.get(plugin_key, {})
                    if each_plugin_json == {}:
                        return_json[plugin_key] = each_plugin_json
                    each_of_pages = each_plugin_json.get("pages", [])
                    if each_of_pages == []:
                        each_plugin_json["pages"] = each_of_pages
                    each_of_pages.append(page.__dict__)

                    each_of_widgets = each_plugin_json.get("widgets", [])
                    if each_of_widgets == []:
                        each_plugin_json["widgets"] = each_of_widgets
                    each_of_widgets.extend(widgets_arr)

                    id_npm_dependencies_map[page.id] = dependencies_json
                    each_of_npm_dependencies = each_plugin_json.get("npmDependencies", {})
                    if each_of_npm_dependencies == {}:
                        each_plugin_json["npmDependencies"] = each_of_npm_dependencies
                    each_of_npm_dependencies[page.id] = dependencies_json
        if len(return_json) == 0:
            return "EMPTY"
        pages_info_file_path = os.path.join(workspace_path, "target/react_widget/package.json")
        logger.info(" 正在创建package.json %s" % pages_info_file_path)
        return_json_str = json.dumps(return_json)
        write_content_to_file(pages_info_file_path, return_json_str)
        return return_json_str

    def get_page(self, dependencies_json, widgets_arr, workspace_path, node_json_obj, first_language, plugin_key,
                  variables_json):
        page = Page()
        page_name = node_json_obj.get("page_name")
        if page_name is None:
            id = ""
        else:
            id = page_name[:page_name.find("/index.html")]
        page.id = id

        _page_name = node_json_obj.get("_page_name", "")
        uri = "plugin://" + plugin_key + os.sep + _page_name
        page.uri = uri
        page.pluginKey = plugin_key

        component = node_json_obj.get("_component", {})
        biz_name = component.get("name", "")
        name_space = component.get("namespace", "")

        tag_name = node_json_obj.get("tag_name", "")
        stage = node_json_obj.get("stage", "")
        logger.debug(" 获取相关属性值:【id】= %s 、【uri】= %s 、【namepsace】= %s 、【bizName】= %s 、【tagName】= %s 、【stage】= %s" % (
            id, uri, name_space, biz_name, tag_name, stage))

        param_map = {
            "nodeType": "pages",
            "namespace": name_space,
            "bizname": biz_name,
            "widgetName": _page_name,
            "tagName": tag_name,
            "stage": stage
        }
        npm = self._get_react_npm_value(param_map, variables_json)
        if npm != "":
            npm = npm.replace("\"", "")
            dependencies_arr = npm.split(":")
            dependencies_json[dependencies_arr[0]] = dependencies_arr[1]
            page.path = dependencies_arr[0]

        # 解析properties节点下符合react://打头的值的属性
        properties_json_obj = node_json_obj.get("properties")
        if properties_json_obj is not None:
            widgets = []
            for properties_key in properties_json_obj:
                properties_item = properties_json_obj[properties_key]
                if isinstance(properties_item, list):
                    properties_item_json_array = properties_item

                    for items_json in properties_item_json_array:
                        if isinstance(items_json, dict):
                            for key in items_json:
                                obj = items_json[key]
                                if isinstance(obj, str):
                                    item = str(obj)
                                    react_matcher = re.findall("^react://(.+)/(.+)$", item)
                                    if len(react_matcher) > 0:
                                        map_data = self._analysis_widgets(dependencies_json, widgets_arr, widgets, item,
                                                                          workspace_path, first_language,
                                                                          variables_json)
                                        self._handle_data(map_data, dependencies_json, widgets_arr, widgets, item,
                                                          variables_json)
                                        page.widgets = widgets
        return page

    def _analysis_widgets(self, dependencies_json, widgets_arr, widgets, parent_id, workspace_path, first_language,
                          variables_json):
        map_dict = {}
        widgets_file_path = os.path.join(workspace_path, "target/app_component_pages/${TAG_LANGUAGE}/widgets.json")
        widgets_file_path = widgets_file_path.replace("${TAG_LANGUAGE}", first_language)

        if os.path.exists(widgets_file_path):
            widgets_content = read_file_content(widgets_file_path)
            if widgets_content != "":
                widget_content_json_obj = json.loads(widgets_content)
                for widgets_content_key in widget_content_json_obj:
                    widget_json_obj = widget_content_json_obj[widgets_content_key]
                    parent = widget_json_obj.get("__parent")
                    template = widget_json_obj.get("template", "")

                    # 获取js插件信息
                    properties_json_object = widget_json_obj.get("properties")
                    if properties_json_object:
                        module_properties_json = properties_json_object.get("_module_properties")
                        if module_properties_json:
                            js_plugins_arr = module_properties_json.get("js_plugins")
                            if js_plugins_arr:
                                for js_plugin_json in js_plugins_arr:
                                    js_plugins = dependencies_json.get("js_plugins")
                                    if not js_plugins:
                                        js_plugins = {}
                                    js_plugins_name = js_plugin_json.get("name")
                                    js_plugins_version = js_plugin_json.get("version")
                                    js_plugins[js_plugins_name] = js_plugins_version
                                    dependencies_json["js_plugins"] = js_plugins

                    if parent is not None and parent == parent_id:
                        logger.debug(" 查找到__parentId= %s 在widgets.json文件中对应的子颗粒" % parent_id)
                        logger.debug(" 对应template= %s" % template)
                        if template != "":
                            map_data = self._analysis_widgets(dependencies_json, widgets_arr, widgets, template,
                                                              workspace_path, first_language, variables_json)
                            self._handle_data(map_data, dependencies_json, widgets_arr, widgets, template,
                                              variables_json)

                    # 找到pages.json中properties节点下widget-list的name对应在widgets.json中的template值
                    if parent_id == template:
                        tag_name = widget_json_obj.get("tag_name", "")
                        stage = widget_json_obj.get("stage", "")
                        widget_name = widget_json_obj.get("widget_name", "")

                        map_dict["tag_name"] = tag_name
                        map_dict["stage"] = stage
                        map_dict["widget_name"] = widget_name
        return map_dict
