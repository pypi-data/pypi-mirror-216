#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger


class CleanConfigFileBuilder:
    def __init__(self):
        pass

    def perform(self, variables_dict):
        languages_json = variables_dict["languages"]
        workspace_path = os.getcwd()
        for language in languages_json:
            # 删除ios_extension.json文件
            ios_extension_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/components/ios_extension.json".replace("${TAG_LANGUAGE}", language))
            if os.path.exists(ios_extension_file_path):
                os.remove(ios_extension_file_path)
                logger.debug(" delete %s" % ios_extension_file_path)

            # 删除plugin.json文件
            plugin_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/components/plugin.json".replace("${TAG_LANGUAGE}", language))
            if os.path.exists(plugin_file_path):
                os.remove(plugin_file_path)
                logger.debug(" delete  %s" % plugin_file_path)

            # 去除build.json中versionNumber属性
            build_json_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace("${TAG_LANGUAGE}", language))
            build_json_content = read_file_content(build_json_file_path)
            build_json = json.loads(build_json_content)

            self.build_remove_attribute(build_json_file_path, build_json)

            # 去除pages.json中第一层级带_的属性
            pages_json_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace("${TAG_LANGUAGE}", language))
            pages_json_content = read_file_content(pages_json_file_path)
            pages_json = json.loads(pages_json_content)

            self.pages_remove_attribute(pages_json_file_path, pages_json)

            # 简化widgets.json内容格式
            widget_json_file_path = os.path.join(workspace_path, "app/assets/app_factory/${TAG_LANGUAGE}/pages/widgets.json".replace("${TAG_LANGUAGE}", language))
            widget_json_content = read_file_content(widget_json_file_path)
            widget_json = json.loads(widget_json_content)

            self.widget_remove_attribute(widget_json_file_path, widget_json)

    def build_remove_attribute(self, build_json_file_path, build_json):
        """
        去除version和versionNumber属性
        :param build_json:
        :return:
        """
        for build_object in build_json:
            if "versionNumber" in build_object.keys():
                build_object.pop("versionNumber")
        write_content_to_file(build_json_file_path, json.dumps(build_json, ensure_ascii=False))

    def pages_remove_attribute(self, pages_json_file_path, pages_json):
        """
        去除pages.json第一层级下所有带_的属性
        :param pages_json_file_path:
        :param pages_json:
        :return:
        """
        for page_key in pages_json:
            page_json_object = {}

            page_value = pages_json[page_key]
            for attribute_key in page_value:
                # 过滤掉"_"开头的属性，添加到新的object中
                if not attribute_key.startswith("_") and attribute_key != "stage":
                    page_json_object[attribute_key] = page_value[attribute_key]

            # 将原来的key对应的值，用pgae_json_object覆盖掉
            pages_json[page_key] = page_json_object
        write_content_to_file(pages_json_file_path, json.dumps(pages_json, ensure_ascii=False))

    def widget_remove_attribute(self, widget_json_file_path, widget_json):
        """
        保留properties和event属性，并将__parent和__top属性值以key分别为_parent和_top加入到properties中
        :param widget_json_file_path:
        :param widget_json:
        :return:
        """
        new_content_json_object = {}
        for key in widget_json:
            value_json_object = {}

            widget_json_object = widget_json[key]
            properties_json_object = widget_json_object["properties"]
            if "properties" in widget_json_object.keys():
                parent = widget_json_object.get("__parent", "")
                top = widget_json_object.get("__top", "")

                properties_json_object["_parent"] = parent
                properties_json_object["_top"] = top

                implement = widget_json_object.get("implement", "")
                if implement:
                    properties_json_object["implement"] = implement

                value_json_object["properties"] = properties_json_object

            event_json_object = widget_json_object.get("event", {})
            if event_json_object:
                value_json_object["event"] = event_json_object

            module_plugin_json_object = widget_json_object.get("module_plugin", {})
            if module_plugin_json_object:
                value_json_object["module_plugin"] = module_plugin_json_object

            widget_name = widget_json_object.get("widget_name", "")
            if widget_name:
                value_json_object["widget_name"] = widget_name

            # 只保留了：properties / event / module_plugin / widget_name
            new_content_json_object[key] = value_json_object
        write_content_to_file(widget_json_file_path, json.dumps(new_content_json_object, ensure_ascii=False))
