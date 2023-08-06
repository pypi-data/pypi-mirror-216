#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.parser.abstract_parser import *
from apf_ci.lite_app.lite_enum.component_type_enum import ComponentTypeEnum

class ReactParser(AbstractParser):

    def exact_parse(self, component_json_object):
        version = self.param_map["envtarget"]
        app_type = self.param_map["build_app_type"]
        component_type = ComponentTypeEnum.get_component_type_by_app_type(app_type)

        react_json_object = self.get_lite_app_info(component_json_object, component_type)
        if react_json_object is None:
            return None

        npm = react_json_object.get("npm", "")
        if npm == "":
            return None

        npm_arr = npm.replace("\"", "").replace(" ", "").split(":")
        js_package_name = npm_arr[0]
        js_version = npm_arr[1]

        component_json = component_json_object["component"]
        namespace = component_json["namespace"]
        biz_name = component_json["name"]
        module_name = namespace + "." + biz_name

        npm_dto = NpmDTO()
        npm_dto.npm = npm
        npm_dto.version = version
        npm_dto.js_package_name = js_package_name
        npm_dto.js_version = js_version
        npm_dto.module_name = module_name
        npm_dto.component_type = component_type
        return npm_dto

