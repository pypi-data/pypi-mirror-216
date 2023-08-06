#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.parser.abstract_parser import *


class LocalH5Parser(AbstractParser):
    def exact_parse(self, component_json_object):
        local_h5_json_object = self.get_lite_app_info(component_json_object, "local-h5")
        if local_h5_json_object is None:
            return None
        npm = local_h5_json_object.get("npm", "")
        if npm == "":
            return None

        version = local_h5_json_object["version"]

        npm_arr = npm.replace("\"", "").replace(" ", "").split(":")
        js_package_name = npm_arr[0]
        js_version = npm_arr[1]
        module_name = js_package_name[js_package_name.find("/") + 1:]

        npm_dto = NpmDTO()
        npm_dto.npm = npm
        npm_dto.version = version
        npm_dto.js_package_name = js_package_name
        npm_dto.js_version = js_version
        npm_dto.module_name = module_name
        npm_dto.component_type = "local-h5"
        return npm_dto
