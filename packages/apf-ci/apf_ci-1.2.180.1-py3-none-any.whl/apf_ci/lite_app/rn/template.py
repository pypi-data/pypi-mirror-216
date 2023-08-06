#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Git template module
"""

__author__ = 'LianGuoQing'

import os
import json
from apf_ci.util.file_utils import read_file_content, write_content_to_file
from apf_ci.util.log_utils import logger

from apf_ci.util.file_utils import write_content_to_file
from apf_ci.util.http_utils import get_data, post_for_array

from apf_ci.init.git_template_service import get_main_component_templates_info, get_snapshot_templates_info


class TemplateService:
    def __init__(self, target_path, storage_host, biz_mng_host, factory_id):
        self.target_path = target_path
        self.storage_host = storage_host
        self.factory_id = factory_id
        self.biz_mng_host = biz_mng_host

    def create_git_templates(self, git_templates):
        """The create git_templates.json file"""
        git_templates_path = os.path.join(self.target_path, 'git_templates.json')
        write_content_to_file(git_templates_path, json.dumps(git_templates))
        logger.info(' 创建git_templates.json文件成功：%s' % git_templates_path)

    def create_snapshot_template(self, snapshot_templates):
        """The create snapshot_template.json file"""
        snapshot_template_path = os.path.join(self.target_path, 'snapshot_template.json')
        write_content_to_file(snapshot_template_path, snapshot_templates)
        logger.info('创建snapshot_template.json文件成功：%s' % snapshot_template_path)

    def parse_git_templates(self, templates, git_type):
        """
        The parse templates based on git_type.
        :param templates:
        :param git_type: [android | ios | react | react-widget | h5-widget]
        :return:
        """
        node_json = templates[git_type.lower()]
        git_json = node_json['git']
        git_repository = git_json['source']
        commit_id = git_json['commit-id']

        build_tool = ''
        if 'build-tool' in node_json.keys():
            build_tool = node_json['build-tool']

        return git_repository, commit_id, build_tool

    def parse_snapshot_template(self, templates, git_type):
        """
        The parse snapshot templates based on git_type
        :param templates:
        :param git_type:
        :return:
        """
        git_repository = ''
        commit_id = ''
        build_tool = ''

        for template_json in json.loads(templates):
            if template_json['type'].lower() == git_type:
                git_repository = template_json['template']
                commit_id = template_json['commitId']
                if 'buildTool' in template_json.keys():
                    build_tool = template_json['buildTool']

        return git_repository, commit_id, build_tool

    def get_server_template(self, git_type):
        """
        Get git_repository, commit_id, build_tool value on the server by git_type
        :param git_type:
        :return:
        """
        template_url = "%s/v0.8/template/%s" % (self.storage_host, git_type)
        template_json = get_data(template_url)
        git_repository = template_json['template']
        commit_id = template_json['commit_id']

        build_tool = ''
        if 'build_tool' in template_json.keys():
            build_tool = template_json['build_tool']

        return git_repository, commit_id, build_tool

    def get_template(self, git_type):
        """
        Get git_repository, commit_id, build_tool value on the template by git_type
        :param git_type:
        :return:
        """
        git_repository = ''
        commit_id = ''
        build_tool = ''

        git_templates = get_main_component_templates_info(self.storage_host, self.factory_id)
        if git_templates is not None:
            self.create_git_templates(git_templates)
            git_repository, commit_id, build_tool = self.parse_git_templates(git_templates, git_type)
            logger.info(' xml中配置%s模板template：%s, commitId: %s, buildTool: %s' % (
                git_type, git_repository, commit_id, build_tool))

        if git_repository == '' and commit_id == '' and build_tool == '':
            snapshot_templates = get_snapshot_templates_info(self.storage_host, self.factory_id)
            logger.debug(snapshot_templates)
            if snapshot_templates is not None:
                self.create_snapshot_template(snapshot_templates)
                git_repository, commit_id, build_tool = self.parse_snapshot_template(snapshot_templates, git_type)
                logger.info(' snapshot中配置%s模板template：%s, commitId: %s, buildTool: %s' % (
                    git_type, git_repository, commit_id, build_tool))

        if git_repository == '' and commit_id == '' and build_tool == '':
            git_repository, commit_id, build_tool = self.get_server_template(git_type)
            logger.info(' server中配置%s模板template：%s, commitId: %s, buildTool: %s' % (
                git_type, git_repository, commit_id, build_tool))

        return git_repository, commit_id, build_tool

    def get_build_tool_properties(self, version):
        url = self.biz_mng_host + "/v1.0/bizs/defines/dimensions/stage"
        body = [{"name": "js-build-tool",
                 "namespace": "com.nd.sdp.app.factory.build",
                 "stage": version}]
        resp = post_for_array(url, body)
        tool_key = "com.nd.sdp.app.factory.build:js-build-tool:" + version
        if tool_key in resp:
            component = resp[tool_key]
            if 'extensions' in component:
                extensions = component['extensions']
                properties = {}
                if 'build' in extensions:
                    properties = extensions['build']['properties']
                elif 'runtime' in extensions:
                    properties = extensions['runtime']['properties']
                return properties

    def get_variables_script_template(self, lite_app_type):
        """
            Get git_repository, commit_id, build_tool value on the build config biz
            :param git_type:
            :return:
        """
        git_repository = ''
        commit_id = ''
        build_tool = ''

        build_json_path = os.path.join(self.target_path, 'app', 'assets', 'app_factory', 'zh-CN', 'components',
                                       'build.json')
        build_json_data = read_file_content(build_json_path)
        build_json = json.loads(build_json_data)
        for each_build_json in build_json:
            component = each_build_json["component"]

            namespace = component["namespace"]
            biz_name = component["name"]

            if namespace == 'com.nd.sdp.app.factory.build' and biz_name == 'js-build-tool':
                version = each_build_json["version"]
                properties = self.get_build_tool_properties(version)
                #properties = each_build_json["properties"]

                if lite_app_type == 'react-widget':
                    git_repository = properties['react-widget_git']['_value']
                    commit_id = properties['react-widget_git_commitid']['_value']
                    build_tool = properties['react-widget_build_tool']['_value']
                elif lite_app_type == 'react':
                    git_repository = properties['react_git']['_value']
                    commit_id = properties['react_git_commitid']['_value']
                    build_tool = properties['react_build_tool']['_value']
                elif lite_app_type == 'h5-widget':
                    git_repository = properties['h5-widget_git']['_value']
                    commit_id = properties['h5-widget_git_commitid']['_value']
        return git_repository, commit_id, build_tool





