#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
测试多语言颗粒资源下载
multi_language_resource_builder
"""

import os
import unittest

from apf_ci.rn_widget.builder.multi_language_resource_builder import MultiLanguageResourceBuilder
from apf_ci.util.content_service_config import ContentServiceConfig


class TestMultiLanguageResource(unittest.TestCase):
    multi_language_resource_builder = MultiLanguageResourceBuilder()


    def test_init_test_directory(self):
        """
        初始化测试空间，自动创建widget.json的文件目录，但widget.json需要去jenkins上拷贝一份下来测
        :return:
        """
        workspace_path = os.getcwd()
        app_factory_path = os.path.join(workspace_path, "app", "assets", "app_factory")
        widget_en_json_path = os.path.join(app_factory_path, "en", "pages")
        widget_zhcn_json_path = os.path.join(app_factory_path, "zh-CN", "pages")
        if not os.path.exists(widget_en_json_path):
            os.makedirs(widget_en_json_path)
        if not os.path.exists(widget_zhcn_json_path):
            os.makedirs(widget_zhcn_json_path)

    # test打头的方法会被识别为测试方法
    def test_get_widget_module_id_json(self):
        app_language_list = []
        language_element_en = {
            "id": "577e347ea310d2b92220d220", # 取部分字段
            "name": "en",
            "type": "language"
        }
        language_element_zh_cn = {
            "id": "577e347ea310d2b92220d222", # 取部分字段
            "name": "zh-CN",
            "type": "language"
        }
        app_language_list.append(language_element_en)
        app_language_list.append(language_element_zh_cn)

        result_json = self.multi_language_resource_builder.get_widget_module_id_json(app_language_list)
        # 校验 语言是否为result_json的key 是否正确
        assert "en" in result_json.keys()
        assert "zh-CN" in result_json.keys()
        # 校验 widget对应的 moduleId值是否正确
        en_widget_first_widget_module_josn = result_json.get("en")
        # 取 module id 判断widgetname是否有在其中
        en_widget_list = en_widget_first_widget_module_josn.get("0596db05-71f3-477c-9b20-b41d975e722e")
        assert "diary-weather" in en_widget_list
        assert "diary-share" in en_widget_list

    def test_get_widget_npm_json(self):
        widgets_json_arr = []
        widget1 = {
            "namespace": "com.nd.sdp.widget",
            "biz_name": "appcommonwidget",
            "version": "rekease",
            "npm": "@app.react.widget.sdp.nd/image-left-item:0.0.35"
        }
        widget2 = {
            "namespace": "com.nd.sdp.widget",
            "biz_name": "appcommonwidget",
            "version": "rekease",
            "npm": "@app.react.widget.sdp.nd/limit-list-view:0.0.36"
        }
        widgets_json_arr.append(widget1)
        widgets_json_arr.append(widget2)

        result_json = self.multi_language_resource_builder.get_widget_npm_json(widgets_json_arr)

        # 校验 “image-left-item”为key的 npm版本号为 0.0.35
        assert result_json.get("image-left-item") == "0.0.35"
        # 校验 “limit-list-view”为key的 npm版本号为 0.0.36
        assert result_json.get("limit-list-view") == "0.0.36"

    def test_component_service_to_query_language_version(self):
        widgets_npm_json = {
            'image-left-item': '0.0.35',
            'limit-list-view': '0.0.36'
        }

        result_json = self.multi_language_resource_builder.component_service_to_query_language_version(widgets_npm_json)

    def test_query_widget_language_app_resource(self):
        languages_array = []
        language_element_en = {
            "id": "577e347ea310d2b92220d220", # 取部分字段
            "name": "en",
            "type": "language"
        }
        language_element_zh_cn = {
            "id": "577e347ea310d2b92220d222", # 取部分字段
            "name": "zh-CN",
            "type": "language"
        }
        languages_array.append(language_element_en)
        languages_array.append(language_element_zh_cn)

        factory_id = "5b7fd074-521f-4112-a62b-a889a68526e0"
        widget_module_json = {
            "en": {
                '0596db05-71f3-477c-9b20-b41d975e722e': ['diary-weather', 'diary-share', 'diary-calendar',
                                                         'diary-voice',
                                                         'diary-bottom', 'diary-word', 'diary-widget', 'diary-picture',
                                                         'diary-weibo'],
                '8c539efc-caa6-4336-a9cf-d1572b74797b': ['image-left-item', 'list-view'],
                'a320d696-b5bb-48f3-82ab-9361bdc40257': ['diary-word-view'],
                '82a65081-94bd-4c07-8521-98393cd231db': ['image-left-item', 'limit-list-view'],
                'ccc0dd48-ebb1-4791-98b0-03163e7f62bd': ['hello-news-detail'],
                'cf6c812d-b442-4b88-8535-7e1107ed1486': ['diary-word-edit']
            }
        }
        widgets_language_version_json = {
            "image-left-item": 1,
            "limit-list-view": 2
        }
        cs_model = ContentServiceConfig()
        cs_model.host = 'http://betacs.101.com/v0.1'
        cs_model.server_name = 'qa_content_biz_comp_mng'
        cs_model.session_id = 'bb932030--4467-95ab-19898db09f8f'
        cs_model.user_id = '100000101'

        variables_json = {}
        variables_json["widget_i18n_store"] = "http://widget-i18n-store.debug.web.nd/"
        result_json = self.multi_language_resource_builder.query_widget_language_app_resource(languages_array,
                                                                                              factory_id,
                                                                                              widget_module_json,
                                                                                              widgets_language_version_json,
                                                                                              cs_model, variables_json)

    def test_download_widget_language(self):
        language_result_arr = [{
                                   "zh-CN": {
                                       "image-left-item": "https://cs.101.com/v0.1/static/cs_fac_resource_manage/development/com.nd.sdp/uc_component/android/skin_1542869555950.zip"
                                   },
                                   "en": {
                                       "image-left-item": "https://cs.101.com/v0.1/static/cs_fac_resource_manage/development/com.nd.sdp/uc_component/android/skin_1542869555950.zip"
                                   }
                               }]
        result_json = self.multi_language_resource_builder.download_widget_language(language_result_arr)
