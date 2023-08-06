#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *

class AndroidInjectionsBuilder:
    def __init__(self, app_type):
        self.app_type = app_type

    def perform(self, variables_dict):
        if self.app_type.lower() != "android":
            return True

        logger.info("安卓react页面注入实例初始化开始！！！")
        widget_manager_url = variables_dict["widget_manage"]
        page_manager_url = variables_dict["page_manage"]
        workspace = os.getcwd()

        pages_file_path = os.path.join(workspace, "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace("${TAG_LANGUAGE}", "zh-CN"))
        pages_content_str = read_file_content(pages_file_path)

        widgets_file_path = os.path.join(workspace, "app/assets/app_factory/${TAG_LANGUAGE}/pages/widgets.json".replace("${TAG_LANGUAGE}", "zh-CN"))
        widgets_content_str = read_file_content(widgets_file_path)

        pages = self._android_injections(pages_content_str, widgets_content_str, page_manager_url, widget_manager_url)
        write_content_to_file(pages_file_path, json.dumps(pages))

        logger.info("安卓react页面注入实例初始化完成！！！")
        return True

    def _android_injections(self, page_content_str, widgets_content_str, page_manager_url, widget_manager_url):
        widget_template_map = {}
        widget_parent_map = {}
        if widgets_content_str:
            widget_json_dict = json.loads(widgets_content_str)
            for key in widget_json_dict:
                widget_obj = widget_json_dict[key]
                template = widget_obj.get("template", "")
                parent = widget_obj.get("__parent", "")
                widget_template_map[template] = widget_obj
                arr = widget_parent_map.get(parent)
                if not arr:
                    arr = []
                arr.append(widget_obj)
                widget_parent_map[parent] = arr

        pages_json = json.loads(page_content_str)

        # react页面验证规则
        reg_ex = "react://(.+)/(.+)$"

        template = ""
        for key in pages_json:
            page = pages_json[key]
            template = page.get("template", "")
            if template.startswith("react://com.nd.apf.react.native.widget"):
                class_duplicate_map = {}
                parr = self._get_page_android_injects(page, page_manager_url, class_duplicate_map)
                logger.debug("page injections: %s" % parr)

                react_widget_arr = self._find_all_widgets(page, widget_template_map, widget_parent_map, reg_ex)
                logger.debug("page's reactWidgetArr: %s" % react_widget_arr)
                warr = self.get_widget_android_injects(page, widget_manager_url, react_widget_arr, class_duplicate_map)
                logger.debug("widget injections: %s" % warr)

                parr.extend(warr)
                if len(parr) != 0:
                    native_injections = {
                        "native-injection": parr
                    }
                    page["native-injections"] = native_injections
        return pages_json

    def _get_page_android_injects(self, page_json, page_manage_url, class_duplicate_map):
        native_injection_list = []
        component = page_json.get("_component", "")
        react_page_arr = []
        react_page = {
            "namespace": component.get("namespace", ""),
            "name": component.get("name", ""),
            "tag_name": page_json.get("tag_name", ""),
            "page_name": page_json.get("_page_name", "")
        }
        react_page_arr.append(react_page)

        url = page_manage_url + "/v0.1/pages/defines"
        logger.debug("获取page:%s 获取注入声明：%s" % (page_json.get("_name_name", {}), url))
        logger.debug("POST: body=%s" % react_page_arr)

        return_obj = post_for_array(url, react_page_arr, False)
        if not return_obj:
            return native_injection_list
        for key in return_obj.keys():
            each_page = return_obj.get(key)
            pages_obj = each_page.get("pages")
            if not pages_obj:
                return native_injection_list
            page_json_object = pages_obj.get(page_json.get("_page_name", ""))
            if not page_json_object:
                return native_injection_list
            nis = page_json_object.get("native-injections")
            if not nis:
                return native_injection_list
            ni = nis.get("native-injection")
            if not ni:
                return native_injection_list
            if isinstance(ni, dict):
                self._injection_class_dumplicate(class_duplicate_map, ni, native_injection_list)
            elif isinstance(ni, list):
                for temp in ni:
                    self._injection_class_dumplicate(class_duplicate_map, temp, native_injection_list)
        return native_injection_list


    def _injection_class_dumplicate(self, class_duplicate_map, native_injection_obj, native_injection_list):
        if class_duplicate_map.get(native_injection_obj.get("_class", "") + "###" + native_injection_obj.get("_type", "")) is None:
            real = {
                "class": native_injection_obj.get("_class", ""),
                "type": native_injection_obj.get("_type", ""),
                "desc": native_injection_obj.get("_desc", ""),
            }
            native_injection_list.append(real)
            class_duplicate_map[native_injection_obj.get("_class", "") + "###" + native_injection_obj.get("_type", "")] = "1"

    def _find_all_widgets(self, page, widget_template_map, widget_parent_map, reg_ex):
        properties = page.get("properties", {})
        react_widget_arr = []
        for key in properties:
            property = properties[key]
            self._find_all_react_widgets(property, widget_template_map, widget_parent_map, react_widget_arr, reg_ex)
        return react_widget_arr

    def _find_all_react_widgets(self, obj, widget_template_map, widget_parent_map, react_widget_arr, reg_ex):
        if isinstance(obj, str):
            str_value = obj
            if re.findall(reg_ex, str_value):
                # 是react页面
                self._find_each_react_widget(str_value, widget_template_map, widget_parent_map, react_widget_arr)
        elif isinstance(obj, dict):
            # 递归遍历属性，判断是否react页面
            for key in obj:
                value = obj[key]
                self._find_all_react_widgets(value, widget_template_map, widget_parent_map, react_widget_arr, reg_ex)
        elif isinstance(obj, list):
            # 递归遍历属性，判断是否react页面
            for value in obj:
                self._find_all_react_widgets(value, widget_template_map, widget_parent_map, react_widget_arr, reg_ex)


    def _find_each_react_widget(self, str_value, widget_template_map, widget_parent_map, react_widget_arr):
        widget = widget_template_map.get(str_value, {})
        if widget:
            component = widget.get("component", {})
            react_page = {
                "namespace": component.get("namespace", ""),
                "name": component.get("name", ""),
                "tag_name": widget.get("tag_name", ""),
                "widget_name": widget.get("widget_name", "")
            }
            react_widget_arr.append(react_page)
        widget_parent_jsonarr = widget_parent_map.get("value", [])
        if widget_parent_jsonarr:
            # 包含子widget
            for object in widget_parent_jsonarr:
                self._find_each_react_widget(object.get("template", "'"), widget_template_map, widget_parent_map, react_widget_arr)

    def get_widget_android_injects(self, page, widget_manager_url, react_widget_arr, class_duplicate_map):
        native_injection_list = []
        url = widget_manager_url + "/v0.1/widgets/defines"
        logger.debug("获取page: %s 的widget获取注入声明：%s" % (page.get("_page_name"), url))
        logger.debug("POST: body=%s" % react_widget_arr)
        if not react_widget_arr:
            return native_injection_list
        return_obj = post_for_array(url, react_widget_arr, False)
        if not return_obj:
            return native_injection_list

        for key in return_obj.keys():
            each_page = return_obj[key]
            pages_obj = each_page.get("widgets", {})
            if not pages_obj:
                return native_injection_list

            for page_key in pages_obj.keys():
                page_json_object = pages_obj[page_key]
                if not page_json_object:
                    continue
                nis = page_json_object.get("native-injections", {})
                if not nis:
                    continue
                ni = nis.get("native-injection", {})
                if not ni:
                    continue
                if isinstance(ni, dict):
                    self._injection_class_dumplicate(class_duplicate_map, ni, native_injection_list)
                elif isinstance(ni, list):
                    for temp in ni:
                        self._injection_class_dumplicate(class_duplicate_map, temp, native_injection_list)
        return native_injection_list
