#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单元测试 ensure_template_builder
"""
import json
import os
import unittest

from apf_ci.react_widget_resource.builder.ensure_template_builder import EnsureTemplateBuilder
from apf_ci.util.file_utils import read_file_content


class TestEnsureTemplateBuilder(unittest.TestCase):

    storage_host = 'http://app-native-storage.web.sdp.101.com/'
    tool = ''
    commit_id = ''
    url = ''
    ensure_template_builder = EnsureTemplateBuilder(storage_host, tool, commit_id, url)

    def setUp(self):
        print("do something before test.Prepare environment.")
        target_path = os.path.join(os.getcwd(), "target")
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_perform(self):
        variables_json = {
            "build_app_type":'android',
            "npm_registry":'http://registry.npm.sdp.nd'
        }
        self.ensure_template_builder.perform(variables_json)
        variables_json_path = os.path.join(os.getcwd(), "target", "variables.json")
        assert os.path.exists(variables_json_path)

        file_content_json = json.loads(read_file_content(variables_json_path))
        assert file_content_json["git_repository"] == 'git@git.sdp.nd:app-factory/react-native-main-template.git'
        assert file_content_json["commit_id"] == 'v1.0.19'
        assert file_content_json["build_tool"] == '@sdp.nd/react-native-widget-builder@0.0.45'
