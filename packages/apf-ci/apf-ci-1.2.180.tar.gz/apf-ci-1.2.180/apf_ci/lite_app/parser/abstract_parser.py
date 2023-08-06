#!/usr/bin/python3
# -*- coding:utf-8 -*-

from apf_ci.lite_app.model.npm_dto import *
from apf_ci.lite_app.model.cache_bo import *
from apf_ci.lite_app.parser.iparser import *
from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *
from abc import ABCMeta, abstractmethod


class AbstractParser(IParser, metaclass=ABCMeta):
    def __init__(self):
        self.param_map = {}

    @abstractmethod
    def exact_parse(self, component_json_object):
        pass

    def get_lite_app_info(self, component_json, lite_app_type):
        type_json_array = component_json["type"]
        for type_object in type_json_array:
            if isinstance(type_object, str):
                type = type_object
                if lite_app_type == type:
                    return component_json.get(lite_app_type)
        return None

    def get_js_publish_Time(self, js_package_name, js_version, npm_registry):
        # 非正式：开发测试版,需要去取publish_time,因为非正式版本可以重发覆盖
        url_bufld = npm_registry + "/" + js_package_name
        logger.debug(" 获取js publish_time: %s, js_version: %s" % (url_bufld, js_version))
        response_body_json = get_data(url_bufld)

        publish_time = None
        versions = response_body_json.get("versions", {})
        dist_tags = response_body_json.get("dist-tags", {})
        tag_ver = dist_tags.get(js_version, "")
        if tag_ver != "":
            ver = versions.get(tag_ver)
        else:
            ver = versions.get(js_version)
        if ver is not None:
            publish_time = ver.get("publish_time")
        if publish_time is None:
            logger.debug(" jsVersion= %s, 不存在" % js_version)
            raise Exception("依赖: %s 的版本或tag: %s 不存在" % (js_package_name, js_version))

        return publish_time

    def read_components(self):
        app_components_json_file = "app/assets/app_factory/app/components.json"
        components_content_path = os.path.join(os.getcwd(), app_components_json_file)
        components_content = read_file_content(components_content_path)
        components_content_json = json.loads(components_content)
        return components_content_json

    def add_filter(self, filters):
        filter_json_array = []
        if filters != "":
            filter_arr = filters.split(",")
            for filter in filter_arr:
                if filter != "":
                    last_index = filter.rfind(":")
                    sub_str = filter[0:last_index]
                    filter_json_array.append(sub_str)
        return filter_json_array

    def addParameter(self, param_map):
        self.param_map = param_map

    def parse(self, filter_json_array, components_json_array, variables_json):
        npm_registry = variables_json["npm_registry"]
        npm_DTO_list = []
        for components_object in components_json_array:
            if isinstance(components_object, dict):
                component_json = components_object["component"]
                namespace = component_json["namespace"]
                biz_name = component_json["name"]
                key = namespace + ":" + biz_name

                # 过滤
                if filter_json_array == [] or filter_json_array is None or key in filter_json_array:
                    npmDTO = self.exact_parse(components_object)
                    if npmDTO is not None:
                        publish_time = self.get_js_publish_Time(npmDTO.js_package_name, npmDTO.js_version, npm_registry)
                        npmDTO.biz_name = biz_name
                        npmDTO.namespace = namespace
                        npmDTO.js_publish_time = publish_time
                        npmDTO.param_map = self.param_map
                        npmDTO.component_info = json.dumps(components_object)
                        npm_DTO_list.append(npmDTO)
        return npm_DTO_list
