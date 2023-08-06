#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import re

from apf_ci.constant.path_constant import PathConstant
from apf_ci.h5_grain.builder.analysis_pages_builder import AnalysisPagesBuilder
from apf_ci.h5_grain.h5_page import H5Page
from apf_ci.h5_grain.package_model import PackageModel
from apf_ci.rn_widget.model.widget import Widget
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger


class CreatePackageBuilder:

    def __init__(self, storage_host, factory_id):
        self.storage_host = storage_host
        self.factory_id = factory_id
        self.analysis_builder = AnalysisPagesBuilder(storage_host, factory_id)

    def perform(self, variables_json):

        # 获取应用语言，只需要第一个即可
        first_language = self.get_first_language(variables_json)

        # 创建package.json
        result = self.create_package(first_language)

        if result == "EMPTY":
            return False
        elif result == "FAILTURE":
            return False

        variables_json["resultObj"] = result
        variables_path = os.path.join(os.getcwd(), "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))

        return True


    def get_first_language(self, variables_json):
        """
        获取第一个语言
        :param variables_json:
        :return:
        """
        languages_array = variables_json["languages"]
        workspace_path = os.getcwd()

        language_arr = self.analysis_builder.get_first_language(workspace_path, languages_array)
        first_language = ""
        if language_arr is not None and language_arr != []:
            first_language = str(language_arr[0])
        logger.info(" 默认第一个语言 firstLanguage: %s" % first_language)
        return first_language

    def create_package(self, first_language):
        """
        解析pages.json创建package.json
        :param first_language:
        :return:
        """
        workspace_path = os.getcwd()

        pages_file_path = os.path.join(workspace_path, PathConstant.TARGET_PAGES_FILE_PATH)
        pages_file_path = pages_file_path.replace("${TAG_LANGUAGE}", first_language)
        logger.info(" 正在读取pages.json文件: %s" % pages_file_path)

        if not os.path.exists(pages_file_path):
            logger.info(" pages.json文件不存在: %s" % pages_file_path)
            return "FAILTURE"

        pages_json_str = read_file_content(pages_file_path)
        pages_json_obj = json.loads(pages_json_str)

        # 封装package.json内容
        package_model = PackageModel()
        pages = []
        dependencies = ""
        # 所依赖的npm集合
        dependencies_json = {}
        # 解析page.json文件中满足条件的节点，循环节点
        for pages_json_key in pages_json_obj:
            node_json_object = pages_json_obj[pages_json_key]
            if node_json_object:
                template = node_json_object.get("template")
                if template:
                    regex = 'local://com.nd.apf.h5.widget/(.+)/index.html$'
                    if re.match(regex, template):
                        logger.debug(" 匹配到满足正则表达式 %s 条件的template值：%s" % (regex, template))
                        page = self.get_page(dependencies_json, template, node_json_object)
                        pages.append(page.__dict__)
                        dependencies = json.dumps(dependencies_json, ensure_ascii=False)
                    else:
                        logger.debug(" 未匹配到结果 %s" % template)

        if len(pages) == 0:
            return "EMPTY"
        template_file_path = os.path.join(workspace_path, "target/h5_grain/packageTemplate.json")
        build_config_json = read_file_content(template_file_path)
        logger.info(" 正在读取packageTemplate.json文件内容...path: %s" % template_file_path)

        package_model.other = build_config_json
        package_model.pages = json.dumps(pages, ensure_ascii=False)
        package_model.dependencies = dependencies

        package_file_path = os.path.join(workspace_path, "target/h5_grain/package.json")
        logger.info(" 正在向package.json文件中写入内容...path: %s" % package_file_path)
        write_content_to_file(package_file_path, package_model.tostring_format())

        result_obj = {
            "pages": pages,
            "npmDependencies": dependencies
        }
        return result_obj

    def get_page(self, dependencies_json, template, node_json_obj):
        """
        获取符合正则表达式的page内容
        :param defines_file_path:
        :param template:
        :param node_json_obj:
        :return:
        """
        workspace_path = os.getcwd()
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

        npm = self.analysis_builder.get_h5_npm_value(workspace_path, name_space, biz_name)
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

                                widget_npm = self.analysis_builder.get_h5_npm_value(workspace_path, h5_namespace,
                                                                                    h5_biz_name)
                                if widget_npm:
                                    widget_npm = widget_npm.replace('"', "")
                                    dependencies_arr = widget_npm.split(":")
                                    dependencies_json[dependencies_arr[0]] = dependencies_arr[1]
                                    widget.path = dependencies_arr[0]

                                widgets.append(widget.__dict__)
                                break
                        page.widgets = widgets
        logger.debug(" 解析后的page为：id:%s, path:%s, uri:%s, widgets:%s" % (page.id, page.path, page.uri, page.widgets))
        return page
