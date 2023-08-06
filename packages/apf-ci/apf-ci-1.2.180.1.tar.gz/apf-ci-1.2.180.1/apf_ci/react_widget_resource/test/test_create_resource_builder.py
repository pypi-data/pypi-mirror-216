#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单元测试 create resource builder
"""
import os
import unittest

from apf_ci.react_widget_resource.builder.create_resource_builder import CreateResourceBuilder
from apf_ci.util.content_service_config import ContentServiceConfig


class TestCreateResourceBuilder(unittest.TestCase):
    page_id_list = ['1505284920731']
    env_target = 'preproduction'
    factory_id = '711cc60d-d38f-4623-a255-a3143221b176'
    storage_host = 'http://app-native-storage.web.sdp.101.com/'
    widget_host = 'https://widget-manage-server.sdp.101.com/'
    plugin_id_dir = 'com.nd.sdp.plugin.motiondiaryplugin'
    cs_config = ContentServiceConfig()
    cs_config.user_id = '100000101'
    cs_config.session_id = '0231aad9-d1ac-4146-83bf-2de1fb9211e2'
    cs_config.server_name = 'cs_app_native_storage'
    cs_config.host = 'http://cs.101.com/v0.1'
    create_resource = CreateResourceBuilder(page_id_list, env_target, factory_id, storage_host, widget_host,
                                            plugin_id_dir, cs_config)

    def setUp(self):
        print("do something before test.Prepare environment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_get_app_language_array(self):
        all_languages_json_arr = [{'id': '577e347ea310d2b92220d220', 'parent': 'language', 'name': 'en',
                                   'build_alias': {'android': 'en', 'ios': 'en'},
                                   'alias': {'android': 'en', 'ios': 'en'}, 'type': 'language',
                                   'policy_url': '$[policyUrl]', 'description': '英语', 'weight': 1, 'hidden': False,
                                   'display': 'English', 'create_time': 1474627677847},
                                  {'id': '577e347ea310d2b92220d222', 'parent': 'chs', 'name': 'zh-CN',
                                   'build_alias': {'android': 'zh', 'ios': 'zh-Hans'},
                                   'alias': {'android': 'zh-CN', 'ios': 'zh-Hans'}, 'type': 'language',
                                   'policy_url': '$[policyUrl]', 'description': '简体中文', 'weight': 2, 'hidden': False,
                                   'display': '简体中文', 'create_time': 1553853423143},
                                  ]
        languages_json_arr = ['en', 'zh-CN']
        language_arr = self.create_resource.get_app_language_array(languages_json_arr, all_languages_json_arr)
        assert language_arr[0]["id"] == '577e347ea310d2b92220d220'
        assert language_arr[1]["id"] == '577e347ea310d2b92220d222'

    def test_get_skin_resource_id(self):
        resource_host = 'http://fac-resouce-manage.oth.web.sdp.101.com/'
        skin_id = self.create_resource.get_skin_resource_id(resource_host)
        assert skin_id == '577e347ea310d2b92220d21e'
