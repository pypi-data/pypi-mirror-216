#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import json
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.rn_widget.model.page import *
from apf_ci.rn_widget.model.widget import *


class AnalysisPagesBuilder:
    def __init__(self, storage_host, lifecycle_host, factory_id, component_type, load_comp_list):
        self.storage_host = storage_host
        self.lifecycle_host = lifecycle_host
        self.factory_id = factory_id
        self.component_type = component_type
        self.load_comp_list = load_comp_list

    def perform(self, variables_json):
        language_array = variables_json["languages"]
        app_language_jsonarray = variables_json["app_language_array"]

        workspace_path = os.getcwd()
        # 生成appLanguageInfo.json文件
        app_language_info_file_path = os.path.join(workspace_path, "target/react_widget/config/appLanguageInfo.json")
        write_content_to_file(app_language_info_file_path, json.dumps(app_language_jsonarray))

        language_arr = self._get_language(workspace_path, language_array, variables_json)
        first_language = ""
        if language_arr is not None and language_arr != []:
            first_language = str(language_arr[0])
        logger.info(" 默认第一个语言 firstLanguage: %s" % first_language)
        result = self._analysis_pages(workspace_path, first_language, language_arr, self.load_comp_list, variables_json)

        if result == "FAILTURE":
            return False

        # 所依赖的颗粒放入全局变量中，值可能会为EMPTY，需排除
        variables_json["pagesResult"] = result
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
        return True

    def _get_language(self, workspace_path, language_array, variables_json):
        language_arr = {}
        config_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/config.json")
        logger.info("正在读取config.json文件: %s" % config_file_path)
        if os.path.exists(config_file_path):
            language_url = self.storage_host + "/v0.8/apps/" + self.factory_id + "/languages"
            language_json = get_data(language_url)

            language_arr = language_json.get("languages", [])
        else:
            config_json_str = read_file_content(config_file_path)
            if config_json_str is not None and config_json_str != "":
                config_json_obj = json.loads(config_json_str)
                if "language_enable" in config_json_obj.keys():
                    language_arr = config_json_obj["language_enable"]
                    if len(language_arr) <= 0:
                        language_arr = language_array
        return language_arr

    def _analysis_pages(self, workspace_path, first_language, language_arr, load_comp_list, variables_json):
        pages_file_path = os.path.join(workspace_path, "target/app_component_pages/${TAG_LANGUAGE}/pages.json")
        pages_file_path = pages_file_path.replace("${TAG_LANGUAGE}", first_language)
        logger.info(" 正在读取pages.json文件: %s" % pages_file_path)

        return_json = {}
        if not os.path.exists(pages_file_path):
            logger.warning(" pages.json文件不存在: %s" % pages_file_path)
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
                    page = self._get_page(dependencies_json, widgets_arr, workspace_path, node_json_obj,
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
        pages_info_file_path = os.path.join(workspace_path, "target/react_widget/config/pagesInfo.json")
        return_json_str = json.dumps(return_json)
        write_content_to_file(pages_info_file_path, return_json_str)
        return return_json_str

    def _get_page(self, dependencies_json, widgets_arr, workspace_path, node_json_obj, first_language, plugin_key,
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

    def _get_react_npm_value(self, param_map, variables_json):
        npm = ""
        node_type = param_map["nodeType"]
        name_space = param_map["namespace"]
        biz_name = param_map["bizname"]
        widget_name = param_map["widgetName"]
        tag_name = param_map["tagName"]
        stage = param_map["stage"]

        request_jsonarr = []
        request_body = {
            "namespace": name_space,
            "name": biz_name,
            "tag_name": tag_name,
            "stage": stage
        }

        service_name = ""
        if node_type == "widgets":
            service_name = "widget"
            request_body["widget_name"] = widget_name
        elif node_type == "pages":
            service_name = "page"
            request_body["page_name"] = widget_name
        uri = self.lifecycle_host + "/v0.1/lifecycle/services/" + service_name + "/actions/defines"
        request_jsonarr.append(request_body)
        response_body = post_for_array(uri, request_jsonarr, False)

        prefix = name_space + ":" + biz_name + ":" + widget_name + ":"
        for response_body_key in response_body:
            if response_body_key.startswith(prefix):
                node_json_object = response_body[response_body_key]
                if node_type in node_json_object.keys():
                    widget_json_object = node_json_object[node_type]
                    if widget_name in widget_json_object.keys():
                        widget_json = widget_json_object[widget_name]
                        if "_type" in widget_json.keys():
                            _type = widget_json.get("_type", "")
                            if _type == "react":
                                if self.component_type == "react-android":
                                    react_json_object = widget_json.get("react-android", {})
                                elif self.component_type == "react-ios":
                                    react_json_object = widget_json.get("react-ios", {})

                                if react_json_object != {}:
                                    npm = react_json_object.get("npm", "")
        logger.debug(" npm: %s" % npm)
        return npm

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
                    if parent is not None and parent == parent_id:
                        self._get_js_plugins(widget_json_obj, dependencies_json)
                        logger.debug(" 查找到__parentId= %s 在widgets.json文件中对应的子颗粒" % parent_id)
                        logger.debug(" 对应template= %s" % template)
                        if template != "":
                            map_data = self._analysis_widgets(dependencies_json, widgets_arr, widgets, template,
                                                              workspace_path, first_language, variables_json)
                            self._handle_data(map_data, dependencies_json, widgets_arr, widgets, template,
                                              variables_json)

                    # 找到pages.json中properties节点下widget-list的name对应在widgets.json中的template值
                    if parent_id == template:
                        self._get_js_plugins(widget_json_obj, dependencies_json)

                        tag_name = widget_json_obj.get("tag_name", "")
                        stage = widget_json_obj.get("stage", "")
                        widget_name = widget_json_obj.get("widget_name", "")

                        map_dict["tag_name"] = tag_name
                        map_dict["stage"] = stage
                        map_dict["widget_name"] = widget_name
        return map_dict

    def _get_js_plugins(self, widget_json_object, dependencies_json):
        # 获取js插件信息
        properties_json_object = widget_json_object.get("properties")
        if properties_json_object is not None:
            module_properties_json_object = properties_json_object.get("_module_properties")
            if module_properties_json_object is not None:
                module_name = module_properties_json_object.get("name", "")
                if module_name != "":
                    datasource_interface_json = module_properties_json_object.get("datasource_interface")
                    if datasource_interface_json is not None:
                        npm_name = datasource_interface_json.get("name", "")
                        npm_version = datasource_interface_json.get("version", "")
                        if npm_name != "" and npm_version != "":
                            js_plugin = {}
                            js_plugin[npm_name] = npm_version

                            js_plugins_json = dependencies_json.get("js_plugins")
                            if js_plugins_json is None:
                                js_plugins = {}
                                js_plugins[module_name] = js_plugin
                                dependencies_json["js_plugins"] = js_plugins
                            else:
                                js_plugins_json[module_name] = js_plugin

    def _handle_data(self, map_data, dependencies_json, widgets_arr, widgets, template, variables_json):
        widget = Widget()
        widget.uri = template

        react_biz_id = template[template.find("react://") + 8:template.rfind("/")]
        react_name_space = react_biz_id[:react_biz_id.rfind(".")]
        react_biz_name = react_biz_id[react_biz_id.rfind(".") + 1:]

        widget_name = map_data.get("widget_name", "")
        tag_name = map_data.get("tag_name", "")
        stage = map_data.get("stage", "")
        logger.debug(" reactNameSpace= %s ,reactBizName= %s ,tagName= %s ,stage= %s" % (
            react_name_space, react_biz_name, tag_name, stage))

        param_map = {
            "nodeType": "widgets",
            "namespace": react_name_space,
            "bizname": react_biz_name,
            "widgetName": widget_name,
            "tagName": tag_name,
            "stage": stage
        }
        widget_npm = self._get_react_npm_value(param_map, variables_json)
        if widget_npm != "":
            widget_npm = widget_npm.replace("\"", "")
            dependencies_arr = widget_npm.split(":")
            dependencies_json[dependencies_arr[0]] = dependencies_arr[1]
            widget.path = dependencies_arr[0]

        # 封装所依赖的颗粒组件信息，并去重
        flag = False
        for widgets_object in widgets_arr:
            if isinstance(widgets_object, dict):
                old_namespace = widgets_object.get("namespace", "")
                old_biz_name = widgets_object.get("biz_name", "")
                old_version = widgets_object.get("version", "")
                old_npm = widgets_object.get("npm", "")

                if old_namespace == react_name_space and old_biz_name == react_biz_name and old_version == stage and old_npm == widget_npm:
                    flag = True
                    break
                    
        # pages节点下的widget对象，转为json格式。
        # 此时widget只有 {path:"",uri:""}
        page_widget_json = widget.__dict__
        if not flag:
            widgets_json = {
                "namespace": react_name_space,
                "biz_name": react_biz_name,
                "version": stage,
                "npm": widget_npm,
                # 这里需要记录本次构建的widget_name。给多语言资源解析的时候用multi_language_resource
                "widget_name": widget_name
            }
            widgets_arr.append(widgets_json)
            # 将 widgets_json merge进 page_widget_json cmk需求：希望将pages下的widget节点信息整合在一起。
            page_widget_json.update(widgets_json)
        widgets.append(page_widget_json)
