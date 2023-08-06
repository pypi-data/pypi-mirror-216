#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单元测试 rn_resource_analysis_pages_builder
"""
import os
import unittest

from apf_ci.react_widget_resource.builder.rn_resource_analysis_pages_builder import RnResourceAnalysisPages


class TestRnResourceAnalysisPagesBuilder(unittest.TestCase):
    storage_host = 'http://app-native-storage.web.sdp.101.com/'
    lifecycle_host = 'https://app-factory-lifecycle.sdp.101.com/'
    factory_id = '711cc60d-d38f-4623-a255-a3143221b176'
    component_type = 'react-android'
    load_comp_list = []
    rn_resource_analysis_pages_builder = RnResourceAnalysisPages(storage_host, lifecycle_host, factory_id,
                                                                 component_type, load_comp_list)

    def test_get_page(self):
        dependencies_json = {}
        widgets_arr = []
        workspace_path = os.getcwd()
        node_json_obj = {'__namespace': 'com.nd.sdp.page.appdiarypage', '__open': True, '__page_type': 'default',
                         '__plugin_key': 'com.nd.sdp.plugin.motiondiaryplugin',
                         '__plugin_page': 'plugin://motiondiaryplugin/diary_word_edit',
                         '__plugin_page_name': 'diary_word_edit', '__plugin_param': {}, '__type': 'plugin',
                         '_component': {'name': 'appdiarypage', 'namespace': 'com.nd.sdp.page'},
                         '_page_name': 'diary-page',
                         'component': {'name': 'motiondiaryplugin', 'namespace': 'com.nd.sdp.plugin'},
                         'page_name': '1505284920731/index.html',
                         'plugin_template': 'plugin://com.nd.sdp.plugin.motiondiaryplugin/diary_word_edit',
                         'properties': {'page_display': '默认页', 'widget-list': [{
                             'name': 'react://com.nd.sdp.widget.motiondiarywidget/diary-word-edit?id=c1381062-580a-4099-8849-eb6fc097330b&tag_name=tag_22aaef67-da00-435d-bd19-6261bb8c9060&is_widget=true'}]},
                         'stage': 'release', 'tag_name': 'tag_06b95393-580d-4144-8ed7-36bc6a5d2272',
                         'template': 'react://com.nd.sdp.plugin.motiondiaryplugin/1505284920731/motiondiaryplugin-diary_word_edit'}
        first_language = 'en'
        plugin_key = 'com.nd.sdp.plugin.motiondiaryplugin'
        variables_json = {}
        page_obj = self.rn_resource_analysis_pages_builder.get_page(dependencies_json, widgets_arr, workspace_path,
                                                                    node_json_obj, first_language, plugin_key,
                                                                    variables_json)
        assert page_obj.id == '1505284920731'
        assert page_obj.path == '@app.react.page.sdp.nd/diary-page'
        assert page_obj.pluginKey == 'com.nd.sdp.plugin.motiondiaryplugin'
        assert page_obj.uri == 'plugin://com.nd.sdp.plugin.motiondiaryplugin\\diary-page'

