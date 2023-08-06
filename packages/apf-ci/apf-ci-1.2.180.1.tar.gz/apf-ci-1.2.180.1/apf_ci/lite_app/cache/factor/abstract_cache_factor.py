#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from abc import ABCMeta
from apf_ci.lite_app.cache.factor.icache_factor import *
from apf_ci.util.file_utils import *
from apf_ci.util.md5_utils import *


class AbstractCacheFactor(ICacheFactor, metaclass=ABCMeta):

    def get_file_md5(self, file_path):
        """
        通过文件路径获取文件MD5值，若文件不存在，则对空值进行MD5加密
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_content = f.read()
            return get_md5(file_content)
        else:
            return get_md5("")

    def parse_file(self, file_path, namespace, biz_name):
        """
        解析出对应组件的数据
        :param file_path:
        :param namespace:
        :param biz_name:
        :return:
        """
        new_content_json_array = []

        if os.path.exists(file_path):
            content = read_file_content(file_path)
            if content != "":
                content_json_array = json.loads(content)
                for object in content_json_array:
                    if not isinstance(object, dict):
                        continue

                    component_json = object["component"]
                    component_biz_name = component_json["name"]
                    name_space = component_json["namespace"]

                    if component_biz_name == biz_name and name_space == namespace:
                        new_content_json_array.append(object)
        return new_content_json_array

    def get_build_file_md5(self, workspace_path, config_file_path, language_name, namespace, biz_name):
        """
        获取build.json文件MD5值
        :param workspace_path:
        :param config_file_path:
        :param language_name:
        :param namespace:
        :param biz_name:
        :return:
        """
        app_i18n_build_json_file = "app/assets/app_factory/{TAG_I18N}/components/build.json"
        build_file_path = os.path.join(workspace_path, app_i18n_build_json_file.replace("{TAG_I18N}", language_name))
        new_build_json_array = self.parse_file(build_file_path, namespace, biz_name)

        new_build_file_path = os.path.join(config_file_path, "build.json")
        write_content_to_file(new_build_file_path, json.dumps(new_build_json_array))

        return self.get_file_md5(new_build_file_path)

    def get_pages_file_md5(self, workspace_path, config_file_path, language_name, namespace, biz_name):
        """
        获取pages.json文件MD5值
        :param workspace_path:
        :param config_file_path:
        :param language_name:
        :param namespace:
        :param biz_name:
        :return:
        """
        new_pages_json_obj = {}
        app_i18n_build_json_file = "app/assets/app_factory/{TAG_I18N}/pages/pages.json"
        pages_file_path = os.path.join(workspace_path, app_i18n_build_json_file.replace("{TAG_I18N}", language_name))

        if os.path.exists(pages_file_path):
            pages_json_str = read_file_content(pages_file_path)

            if pages_json_str != "":
                pages_json_obj = json.loads(pages_json_str)
                pages_json_set = pages_json_obj.keys()

                # 解析page.json文件中满足条件的节点，循环节点
                for pages_json_key, node_json_obj in pages_json_obj.items():
                    if "component" in node_json_obj.keys():
                        component = node_json_obj["component"]
                        component_biz_name = component.get("name")
                        if not component_biz_name:
                            component_biz_name = component.get("biz_name")
                        name_space = component["namespace"]
                        if component_biz_name == biz_name and name_space == namespace:
                            new_pages_json_obj[pages_json_key] = node_json_obj

        new_pages_file_path = os.path.join(config_file_path, "pages.json")
        write_content_to_file(new_pages_file_path, json.dumps(new_pages_json_obj))
        return self.get_file_md5(new_pages_file_path)

    def get_components_file_md5(self, workspace_path, module_app_path, namespace, biz_name):
        """
        获取components.json文件MD5值
        :param workspace_path:
        :param module_app_path:
        :param namespace:
        :param biz_name:
        :return:
        """
        component_file_path = os.path.join(workspace_path, "/app/assets/app_factory/app/components.json")
        new_components_jsonarray = self.parse_file(component_file_path, namespace, biz_name)

        new_components_file_path = os.path.join(module_app_path, "components.json")
        write_content_to_file(new_components_file_path, new_components_jsonarray)

        return self.get_file_md5(new_components_file_path)

    def get_components_file_md5(self, module_app_path, data):
        """
        获取components.json文件MD5值
        :param module_app_path:
        :param data:
        :return:
        """
        new_components_jsonarray = []
        data_json_obejct = json.loads(data)
        new_components_jsonarray.append(data_json_obejct)

        new_components_file_path = os.path.join(module_app_path, "components.json")
        write_content_to_file(new_components_file_path, json.dumps(new_components_jsonarray))
        return self.get_file_md5(new_components_file_path)

    def get_service_file_md5(self, workspace_path, module_app_path, namespace, biz_name):
        """
        获取service.json文件MD5值
        :param workspace_path:
        :param module_app_path:
        :param namespace:
        :param biz_name:
        :return:
        """
        service_file_path = os.path.join(workspace_path, "/app/assets/app_factory/app/service.json")
        new_service_jsonarray = self.parse_file(service_file_path, namespace, biz_name)

        new_service_file_path = os.path.join(module_app_path, "service.json")
        write_content_to_file(new_service_file_path, json.dumps(new_service_jsonarray))
        return self.get_file_md5(new_service_file_path)

    def get_skin_file_md5(self, skin_temp_path, namespace, biz_name):
        """
        获取皮肤资源ZIP文件MD5值
        :param skin_temp_path:
        :param namespace:
        :param biz_name:
        :return:
        """
        skin_zip_file_name = namespace + "###" + biz_name + ".zip"
        skin_zip_file_path = os.path.join(skin_temp_path, skin_zip_file_name)
        return self.get_file_md5(skin_zip_file_path)

    def get_language_file_md5(self, language_temp_path, namespace, biz_name, language_alias):
        """
        获取语言ZIP文件MD5值
        :param language_temp_path:
        :param namespace:
        :param biz_name:
        :param language_alias:
        :return:
        """
        language_zip_file_name = namespace + "###" + biz_name + "###" + language_alias + ".zip"
        language_zip_file_path = os.path.join(language_temp_path, language_zip_file_name)
        return self.get_file_md5(language_zip_file_path)
