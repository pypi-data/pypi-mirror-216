#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单元测试 npm builder
"""
import json
import os
import unittest

from apf_ci.react_widget_resource.builder.npm_builder import NpmBuilder
from apf_ci.util.file_utils import read_file_content
from apf_ci.rn_widget.model.page import Page


class TestNpmBuilder(unittest.TestCase):
    npm_dependencies = {'@app.react.page.sdp.nd/diary-page': '0.0.4',
                        '@app.react.widget.sdp.nd/diary-word-edit': '0.0.21'}
    page = Page()
    page.id = '1505284920731'
    page.path = '@app.react.page.sdp.nd/diary-page'
    page.pluginKey = 'com.nd.sdp.plugin.motiondiaryplugin'
    page.uri = 'plugin://com.nd.sdp.plugin.motiondiaryplugin\\diary-page'
    page.widgets = [{'path': '@app.react.widget.sdp.nd/diary-word-edit',
                     'uri': 'react://com.nd.sdp.widget.motiondiarywidget/diary-word-edit?id=c1381062-580a-4099-8849-eb6fc097330b&tag_name=tag_22aaef67-da00-435d-bd19-6261bb8c9060&is_widget=true'}]
    plugin_id_dir = 'com.nd.sdp.plugin.motiondiaryplugin'
    npm_builder = NpmBuilder(page, npm_dependencies, plugin_id_dir)

    def setUp(self):
        print("do something before test.Prepare environment.")
        page_plugin_path = os.path.join(os.getcwd(), "target/react_widget", self.plugin_id_dir, self.page.id)
        if not os.path.exists(page_plugin_path):
            os.makedirs(page_plugin_path)

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_update_package_file(self):
        workspace_path = os.getcwd()
        module_str = '1505284920731'
        self.npm_builder.update_package_file(workspace_path, self.plugin_id_dir, module_str)

        page_plugin_path = os.path.join(os.getcwd(), "target/react_widget", self.plugin_id_dir, self.page.id, "package.json")
        assert os.path.exists(page_plugin_path)
        package_content_json = json.loads(read_file_content(page_plugin_path))
        dependencies_json = package_content_json["dependencies"]
        assert dependencies_json["@sdp.nd/NavigatorManager"] == "^0.1.22"
        page_json = package_content_json["pages"]
        assert page_json[0]["id"] == "1505284920731"
        assert page_json[0]["path"] == "@app.react.page.sdp.nd/diary-page"
        assert page_json[0]["uri"] == "plugin://com.nd.sdp.plugin.motiondiaryplugin\diary-page"
        assert page_json[0]["pluginKey"] == "com.nd.sdp.plugin.motiondiaryplugin"
        widgets_arr = page_json[0]["widgets"]
        assert widgets_arr[0]["path"] == "@app.react.widget.sdp.nd/diary-word-edit"
        assert widgets_arr[0]["uri"] == "react://com.nd.sdp.widget.motiondiarywidget/diary-word-edit?id=c1381062-580a-4099-8849-eb6fc097330b&tag_name=tag_22aaef67-da00-435d-bd19-6261bb8c9060&is_widget=true"

    def test_create_page_file(self):
        workspace_path = os.getcwd()
        module_str = '1505284920731'
        self.npm_builder.create_page_file(workspace_path, self.plugin_id_dir, module_str)

        pages_json_file_path = os.path.join(workspace_path, "target/react_widget", self.plugin_id_dir, module_str, "page.json")
        assert os.path.exists(pages_json_file_path)
        pages_json_file_content_json = json.loads(read_file_content(pages_json_file_path))
        assert pages_json_file_content_json["id"] == "1505284920731"
        assert pages_json_file_content_json["path"] == "@app.react.page.sdp.nd/diary-page"
        assert pages_json_file_content_json["uri"] == "plugin://com.nd.sdp.plugin.motiondiaryplugin\\diary-page"
        assert pages_json_file_content_json["pluginKey"] == "com.nd.sdp.plugin.motiondiaryplugin"

