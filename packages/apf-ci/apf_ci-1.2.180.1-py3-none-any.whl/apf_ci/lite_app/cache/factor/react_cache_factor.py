#!/usr/bin/python3
#! -*- coding:utf-8 -*-

from apf_ci.lite_app.cache.factor.abstract_cache_factor import *
from apf_ci.lite_app.model.cache_factor_bo import *

class ReactCacheFactor(AbstractCacheFactor):

    def get_cache_factor(self, npm_dto):
        param_map = npm_dto.param_map

        languages_array = param_map["app_language_array"]
        languages_json_array = languages_array

        app_type = param_map["build_app_type"]
        sub_app = param_map["isSubApp"]

        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        module_name = npm_dto.module_name
        component_info = npm_dto.component_info

        cache_factor = self._get_cache_factor_json(languages_json_array, module_name, app_type, namespace, biz_name, sub_app, component_info)

        cache_factor["js_package_name"] = npm_dto.js_package_name
        cache_factor["js_version"] = npm_dto.js_version
        cache_factor["js_publish_time"] = npm_dto.js_publish_time

        if "templateBO" in param_map.keys():
            template = param_map["templateBO"]
            if template is not None:
                cache_factor["js_template_commitid"] = template.commit_id
                cache_factor["js_build_tool"] = template.build_tool
                cache_factor["dev"] = template.dev
                cache_factor["app_type"] = app_type

        # 将cache_factor字典，转成cache_factor_bo对象
        cache_factor_bo = CacheFactorBO()
        cache_factor_bo.__dict__ = cache_factor
        logger.debug(" %s" % cache_factor_bo.tostring_format())
        return cache_factor_bo

    def _get_cache_factor_json(self, languages_json_array, module_name, app_type, namespace, biz_name, sub_app, component_info):
        workspace_path = os.getcwd()

        #生成appLanguageInfo.json文件
        self._create_app_language_info_file(workspace_path, json.dumps(languages_json_array))

        #遍历语言，获取build.json、pages.json文件
        language_file_md5_buffer = ""
        build_file_md5_buffer = ""
        pages_file_md5_buffer = ""

        language_temp_path = os.path.join(workspace_path, "target/languageTemp/react")
        module_config_path = os.path.join(workspace_path, "target/react/config/{TAG_MODULE}".replace("{TAG_MODULE}", module_name))

        for language_object in languages_json_array:
            if not isinstance(language_object, dict):
                continue

            language_json_object = language_object
            language_name = language_json_object["name"]

            alias_json = language_json_object["build_alias"]
            language_alias = alias_json[app_type.lower()]
            language_file_md5 = self.get_language_file_md5(language_temp_path, namespace, biz_name, language_alias)
            if language_file_md5 != "":
                language_file_md5_buffer += language_file_md5

            config_file_path = os.path.join(module_config_path, "config", language_name)

            # 取build.json文件中对应的组件内容，放到新建的build.json文件中，并返回其文件MD5值
            build_file_md5 = self.get_build_file_md5(workspace_path, config_file_path, language_name, namespace, biz_name)
            build_file_md5_buffer += build_file_md5

            # 取pages.json文件中对应的组件内容，放到新建的pages.json文件中，并返回其文件MD5值
            pages_file_md5 = self.get_pages_file_md5(workspace_path, config_file_path, language_name, namespace, biz_name)
            pages_file_md5_buffer += pages_file_md5

        skin_temp_path = os.path.join(workspace_path, "target/skinTemp/react")
        skin_file_md5 = self.get_skin_file_md5(skin_temp_path, namespace, biz_name)

        cache_factor_json = {}
        cache_factor_json["skin_file_md5"] = skin_file_md5
        cache_factor_json["i18n_file_md5"] = get_md5(language_file_md5_buffer)
        cache_factor_json["build_file_md5"] = get_md5(build_file_md5_buffer)
        cache_factor_json["pages_file_md5"] = get_md5(pages_file_md5_buffer)

        # 这里sub_app没有转成bool值，直接用str类型
        if sub_app == "true":
            module_app_path = os.path.join(module_config_path, "app")
            cache_factor_json["components_file_md5"] = self.get_components_file_md5(module_app_path, component_info)
            cache_factor_json["service_file_md5"] = self.get_service_file_md5(workspace_path, module_app_path, namespace, biz_name)
        else:
            # 不是子应用的话，也需要把cache_factor的属性填满，以便将dict转成对象的形式
            cache_factor_json["components_file_md5"] = ""
            cache_factor_json["service_file_md5"] = ""
        cache_factor_json["sub_app"] = sub_app

        return cache_factor_json


    def _create_app_language_info_file(self, workspace_path, data):
        app_language_info_file_path = os.path.join(workspace_path, "target/react/config/appLanguageInfo.json")
        write_content_to_file(app_language_info_file_path, data)
