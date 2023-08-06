#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.model.cache_bo import *


class NpmDTO:
    def __init__(self):
        self.biz_name = ""
        self.namespace = ""
        self.npm = ""
        self.version = ""
        self.js_package_name = ""
        self.js_version = ""
        self.module_name = ""
        self.js_publish_time = ""
        self.component_type = ""
        self.component_info = ""
        self.cacheBO = CacheBO()
        self.param_map = {}

    def tostring_format(self):
        return "NpmDTO {bizName=%s, namespace=%s, componentType=%s, moduleName=%s, npm=%s, version=%s, " \
               "jsPackageName=%s, jsVersion=%s, jsPublishTime=%s, paramMap=%s, componentInfo=%s, cacheBO=%s}" % (
                   self.biz_name, self.namespace, self.component_type, self.module_name, self.npm, self.version,
                   self.js_package_name, self.js_version, self.js_publish_time, self.param_map, self.component_info,
                   self.cacheBO)
