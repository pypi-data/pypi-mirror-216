#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re

from apf_ci.h5_grain.h5_page import H5Page
from apf_ci.rn_widget.model.widget import Widget
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class AnalysisPagesBuilder:
    def __init__(self, storage_host, factory_id):
        self.storage_host = storage_host
        self.factory_id = factory_id

    def perform(self, workspace_path, variables_dict):
        languages_array = variables_dict["languages"]
        language_arr = self.get_first_language(workspace_path, languages_array)

        first_language = ""
        for object in language_arr:
            if object:
                first_language = object
                break
        logger.info(" 默认第一个语言firstLanguage： %s" % first_language)

        result_obj = self.__analysis_pages(workspace_path, first_language, language_arr)

        if result_obj == "FAILTURE":
            return False

        variables_dict["resultObj"] = result_obj
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_dict, ensure_ascii=False))
        return True

    def get_first_language(self, workspace_path, languages_array):
        config_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/config.json")
        language_arr = []
        # 如果文件不存在，走API接口获取数据
        if not os.path.exists(config_file_path):
            language_url = self.storage_host + "/v0.8/apps/" + self.factory_id + "/languages"
            language_json = get_data(language_url)

            language_arr = language_json.get("languages")
        else:
            config_json_str = read_file_content(config_file_path)
            if config_json_str:
                config_json_obj = json.loads(config_json_str)
                language_arr = config_json_obj.get("language_enable")
                if not language_arr:
                    language_arr = languages_array
        return language_arr

    def __analysis_pages(self, workspace_path, first_language, language_arr):
        pages_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json")
        pages_file_path = pages_file_path.replace("${TAG_LANGUAGE}", first_language)
        logger.info(" 正在读取pages.json文件： %s" % pages_file_path)

        if not os.path.exists(pages_file_path):
            logger.warning(" pages.json文件不存在：%s" % pages_file_path)
            return "FAILTURE"
        else:
            # 键值对用于替换各语言包中pages.json文件中符合条件的节点值
            replace_node_value_map = {}
            pages = []
            # 所依赖的npm集合
            npm_dependencies = {}
            # 所依赖的颗粒集合
            widgets_arr = []

            pages_json_str = read_file_content(pages_file_path)
            pages_json_obj = json.loads(pages_json_str)

            # 解析page.json文件中满足条件的节点，循环节点
            for pages_json_key in pages_json_obj:
                node_json_obj = pages_json_obj[pages_json_key]
                if node_json_obj:
                    template = node_json_obj.get("template")
                    if template:
                        regex = '^local://com.nd.apf.h5.widget/(.+)/index.html$'
                        if re.match(regex, template):
                            logger.info(" 匹配到满足正则表达式 %s 条件的template值：%s" % (regex, template))
                            page = self.__get_page(npm_dependencies, widgets_arr, workspace_path, template,
                                                   node_json_obj, first_language)
                            pages.append(page.__dict__)
                            # Map数据存储
                            replace_node_value_map[pages_json_key] = page.id
            if len(pages) == 0:
                return "EMPTY"
            logger.debug(" replaceNodeValueMap: %s" % replace_node_value_map)
            # 循环语言包：配置修改符合条件的pages.json文件，以及更新替换build.json文件
            for language in language_arr:
                pages_path = os.path.join(workspace_path,
                                          "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace(
                                              "${TAG_LANGUAGE}", language))
                if not os.path.exists(pages_path):
                    logger.warning(" pages.json文件不存在：%s" % pages_path)
                else:
                    pages_json_content = read_file_content(pages_path)
                    replace_pages_json_obj = json.loads(pages_json_content)

                    for entry_key in replace_node_value_map:
                        value = replace_node_value_map[entry_key]

                        key_json = replace_pages_json_obj.get(entry_key)
                        if key_json:
                            logger.debug(" 正在替换 %s 节点：%s , 变更为: %s" % (pages_path, entry_key, value))
                            replace_pages_json_obj.pop(entry_key)
                            replace_pages_json_obj[value] = key_json
                    write_content_to_file(pages_path, json.dumps(replace_pages_json_obj, ensure_ascii=False))
            result_obj = {
                "widgets": widgets_arr,
                "pages": pages,
                "npmDependencies": npm_dependencies
            }
            return result_obj

    def __get_page(self, dependencies_json, widgets_arr, workspace_path, template, node_json_obj, first_language):
        page = H5Page()

        # 取得pageId的值
        start_index = template.find("local://com.nd.apf.h5.widget/") + 29
        end_index = len(template) - 11
        id = template[start_index:end_index]
        page.id = id

        page_name = node_json_obj.get("_page_name")
        uri = "local://com.nd.apf.h5.widget" + os.sep + page_name
        page.uri = uri

        component = node_json_obj.get("_component", {})
        biz_name = component.get("name")
        name_space = component.get("namespace")
        logger.debug(" 获取相关属性值：【id】= %s、【uri】= %s、【namespace】= %s、【bizname】= %s" % (id, uri, name_space, biz_name))

        npm = self.get_h5_npm_value(workspace_path, name_space, biz_name)
        if npm:
            npm = npm.replace('"', "")
            dependencies_arr = npm.split(":")
            dependencies_json[dependencies_arr[0]] = dependencies_arr[1]
            page.path = dependencies_arr[0]

        # 取properties下的widget
        properties = node_json_obj.get("properties", {})
        if properties:
            for properties_key in properties:
                items_str = properties[properties_key]
                if items_str:
                    items_json_arr = []
                    if isinstance(items_str, list):
                        items_json_arr = items_str
                    else:
                        continue

                    if items_json_arr:
                        widgets = []
                        for items_json in items_json_arr:
                            if not isinstance(items_json, dict):
                                continue
                            for key in items_json:
                                item = items_json[key]
                                h5_pattern = "^h5://(.+)/(.+)$"
                                if not re.match(h5_pattern, item):
                                    continue
                                widget = Widget()
                                widget.uri = item

                                h5_biz_id = item[item.find("h5://") + 5: item.rfind("/")]
                                h5_namespace = h5_biz_id[:h5_biz_id.rfind(".")]
                                h5_biz_name = h5_biz_id[h5_biz_id.rfind(".") + 1:]

                                widget_npm = self.get_h5_npm_value(workspace_path, h5_namespace, h5_biz_name)
                                if widget_npm:
                                    widget_npm = widget_npm.replace('"', "")
                                    dependencies_arr = widget_npm.split(":")
                                    dependencies_json[dependencies_arr[0]] = dependencies_arr[1]
                                    widget.path = dependencies_arr[0]

                                widgets_version = ""
                                build_path = os.path.join(workspace_path,
                                                          "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json")
                                build_path = build_path.replace("${TAG_LANGUAGE}", first_language)
                                if not os.path.exists(build_path):
                                    logger.warning(" build.json文件不存在：%s" % build_path)
                                else:
                                    build_json_content = read_file_content(build_path)
                                    logger.warning(" 向build.json文件获取对应组件的版本：%s" % build_path)

                                    components_json_arr = json.loads(build_json_content)
                                    for components in components_json_arr:
                                        if not isinstance(components, dict):
                                            continue
                                        component_json_obj = components.get("component")
                                        name_space = component_json_obj.get("namespace")
                                        name = component_json_obj.get("name")

                                        if h5_namespace == name == h5_biz_name:
                                            widgets_version = components.get("version")
                                            break
                                # 封装所依赖的颗粒组件信息，并去重
                                flag = False
                                for widget_object in widgets_arr:
                                    if isinstance(widget_object, dict):
                                        old_name_space = widget_object.get("namespace")
                                        old_biz_name = widget_object.get("biz_name")
                                        old_version = widget_object.get("version")
                                        old_npm = widget_object.get("npm")

                                        if old_name_space == h5_namespace and old_biz_name == h5_biz_name and old_version == widgets_version and old_npm == widget_npm:
                                            flag = True
                                            break
                                if not flag:
                                    widgets_json = {
                                        "namespace": h5_namespace,
                                        "biz_name": h5_biz_name,
                                        "version": widgets_version,
                                        "npm": widget_npm
                                    }
                                    widgets_arr.append(widgets_json)
                                widgets.append(widget.__dict__)
                                break
                        page.widgets = widgets
        return page

    def get_h5_npm_value(self, workspace_path, namespace, biz_name):
        npm = ""

        defines_file_path = os.path.join(workspace_path, "target/defines.json")
        if not os.path.exists(defines_file_path):
            error_message = 'defines.json文件不存在：%s' % defines_file_path
            logger.error(LoggerErrorEnum.FILE_NOT_EXIST, error_message)
            raise Exception(error_message)
        else:
            prefix = namespace + ":" + biz_name

            content = read_file_content(defines_file_path)
            defines_json = json.loads(content)

            # 解析defines.json文件中满足条件的节点，循环节点
            for defines_key in defines_json:
                if defines_key.startswith(prefix):
                    logger.warning(" 解析defines.json文件得到满足条件的节点：%s " % defines_key)
                    node_json_obj = defines_json[defines_key]
                    if node_json_obj:
                        types_json_obj = node_json_obj.get("types")
                        if types_json_obj:
                            widget_json_obj = types_json_obj.get("widget")
                            if widget_json_obj:
                                npm = widget_json_obj.get("npm")
        logger.debug("获取到npm值: %s" % npm)
        return npm
