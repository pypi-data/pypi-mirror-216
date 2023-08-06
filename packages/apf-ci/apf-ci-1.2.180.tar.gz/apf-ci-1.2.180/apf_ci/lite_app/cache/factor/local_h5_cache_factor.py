#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from apf_ci.lite_app.model.cache_factor_bo import *
from apf_ci.lite_app.cache.factor.abstract_cache_factor import *
from apf_ci.util.log_utils import logger

class LocalH5CacheFactor(AbstractCacheFactor):

    def get_cache_factor(self, npm_dto):
        param_map = npm_dto.param_map
        languages_array = param_map.get("app_language_array")

        app_type = param_map.get("build_app_type")
        sub_app = param_map.get("isSubApp")

        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        module_name = npm_dto.module_name
        component_info = npm_dto.component_info

        # 取得各文件md5的值，保存到cache对象中
        cache_factor = self.__get_cache_factor_json(languages_array, module_name, app_type, namespace, biz_name, sub_app, component_info)
        cache_factor["js_package_name"] = npm_dto.js_package_name
        cache_factor["js_version"] = npm_dto.js_version
        cache_factor["js_publish_time"] = npm_dto.js_publish_time

        if "dev" not in cache_factor.keys():
            cache_factor["dev"] = ""
        if "js_template_commitid" not in cache_factor.keys():
            cache_factor["js_template_commitid"] = ""
        if "js_build_tool" not in cache_factor.keys():
            cache_factor["js_build_tool"] = ""
        if "app_type" not in cache_factor.keys():
            cache_factor["app_type"] = ""
        if "pages_file_md5" not in cache_factor.keys():
            cache_factor["pages_file_md5"] = ""
        # 将cache_factor字典，转成cache_factor_bo对象
        cache_factor_bo = CacheFactorBO()
        cache_factor_bo.__dict__ = cache_factor
        logger.debug(cache_factor_bo.tostring_format())
        return cache_factor_bo

    def __get_cache_factor_json(self, languages_json_array, module_name, app_type, namespace, biz_name, sub_app, component_info):
        workspace_path = os.getcwd()
        languages_temp_path = os.path.join(workspace_path, "target/languageTemp/h5")
        module_path = os.path.join(workspace_path, "target/local_h5/{TAG_MODULE}".replace("{TAG_MODULE}", module_name))

        language_file_md5_buffer = ""
        build_file_md5_buffer = ""
        pages_file_md5_buffer = ""

        for languages_object in languages_json_array:
            if not isinstance(languages_object, dict):
                continue
            language_name = languages_object.get("name")
            alias_json = languages_object.get("build_alias")
            language_alias = alias_json.get(app_type.lower())
            language_file_md5 = self.get_language_file_md5(languages_temp_path, namespace, biz_name, language_alias)
            if language_file_md5:
                language_file_md5_buffer += language_file_md5

            config_file_path = os.path.join(module_path, "i18n", language_name)

            # 取build.json文件中对应的组件内容，放到新建的build.json文件中，并返回其文件MD5值
            build_file_md5 = self.get_build_file_md5(workspace_path, config_file_path, language_name, namespace, biz_name)
            build_file_md5_buffer += build_file_md5

            # 取pages.json文件中对应的组件内容，放到新建的pages.json文件中，并返回其文件MD5值
            pages_file_md5 = self.get_pages_file_md5(workspace_path, config_file_path, language_name, namespace, biz_name)
            pages_file_md5_buffer += pages_file_md5

        skin_temp_path = os.path.join(workspace_path, "target/skinTemp/h5")
        skin_file_md5 = self.get_skin_file_md5(skin_temp_path, namespace, biz_name)

        cache_factor_json = {
            "skin_file_md5": skin_file_md5,
            "i18n_file_md5": get_md5(language_file_md5_buffer),
            "build_file_md5": get_md5(build_file_md5_buffer),
            "service_file_md5": get_md5(pages_file_md5_buffer)
        }

        # 这里sub_app没有转成bool值，直接用str类型
        if sub_app == "true":
            module_app_path = os.path.join(module_path, "app")
            cache_factor_json["components_file_md5"] = self.get_components_file_md5(module_app_path, component_info)
            cache_factor_json["service_file_md5"] = self.get_service_file_md5(workspace_path, module_app_path, namespace, biz_name)
        else:
            cache_factor_json["components_file_md5"] = ""
            cache_factor_json["service_file_md5"] = ""
        cache_factor_json["sub_app"] = sub_app

        return cache_factor_json

