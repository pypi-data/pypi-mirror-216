#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import json
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.lite_app.rn.template import TemplateService


class TemplateBuilder():
    def __init__(self, storage_host, template_url, template_commit_id, template_build_tool):
        self.storage_host = storage_host
        self.template_url = template_url
        self.template_commit_id = template_commit_id
        self.template_build_tool = template_build_tool

    def perform(self, variables_json):
        workspace_path = os.getcwd()
        git_repository = ""
        commit_id = ""
        build_tool = ""

        variables_script_json = None
        target_variable_scriot_path = os.path.join(workspace_path, "target", 'variables_script.json')
        if os.path.exists(target_variable_scriot_path):
            # 从variables_script.json文件中,获取构建脚本的配置
            variables_script_data = read_file_content(target_variable_scriot_path)
            variables_script_json = json.loads(variables_script_data)

        # 模板工程地址优先级：jenkinsJob（三个值都不能为空） > snapshot（只有buildTool可以为空） > xml（只有buildTool可以为空） > server（三个值都不能为空）
        if self.template_url != "" and self.template_commit_id != "" and self.template_build_tool != "":
            git_repository = self.template_url
            commit_id = self.template_commit_id
            build_tool = self.template_build_tool
        else:
            if variables_script_json is not None:
                git_repository = variables_script_json['react-widget_git']
                commit_id = variables_script_json['react-widget_git_commitid']
                build_tool = variables_script_json['react-widget_build_tool']
            else:
                # 从应用的组件定义中, 获取构建脚本的配置
                template_service = TemplateService(os.path.join(workspace_path), None, None, variables_json["factoryId"])
                git_repository, commit_id, build_tool = template_service.get_variables_script_template('react')

                if git_repository == "" and commit_id == "" and build_tool == "":
                    # git_templates.json取模板信息
                    git_templates_json = self._get_gittemplates_json_source(workspace_path)
                    if git_templates_json != {}:
                        git_repository = git_templates_json.get("source", "")
                        commit_id = git_templates_json.get("commit-id", "")
                        build_tool = git_templates_json.get("build-tool", "")
                    else:
                        # snapshot取模板信息
                        snapshot_templates_json = self._get_snapshot_templates_json_source(workspace_path)
                        if snapshot_templates_json != {}:
                            git_repository = snapshot_templates_json.get("template", "")
                            commit_id = snapshot_templates_json.get("commitId", "")
                            build_tool = snapshot_templates_json.get("buildTool", "")
                        else:
                            # 去server配置模板
                            app_template_url = self.storage_host + "/v0.8/template/react-widget"
                            app_template_json = get_data(app_template_url)

                            git_repository = app_template_json.get("template", "")
                            commit_id = app_template_json.get("commit_id", "")
                            build_tool = app_template_json.get("build_tool", "")

        variables_json["react_widget"] = {}
        variables_json["react_widget"]["git_repository"] = git_repository
        variables_json["react_widget"]["commit_id"] = commit_id
        variables_json["react_widget"]["build_tool"] = build_tool
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
        return True

    def _get_gittemplates_json_source(self, workspace_path):
        result_json_obejct = {}
        git_templates_file_path = os.path.join(workspace_path, "target/git_templates.json")
        if os.path.exists(git_templates_file_path):
            git_templates = read_file_content(git_templates_file_path)
            git_templates_json_object = json.loads(git_templates)
            node_json_object = git_templates_json_object.get("react-widget", {})
            if node_json_object != {}:
                git_json_object = node_json_object.get("git", {})
                if git_json_object != {}:
                    source = git_json_object.get("source", "")
                    xml_commit_id = git_json_object.get("commit-id", "")
                    xml_build_tool = node_json_object.get("build-tool")

                    if source != "" and source != "{}" and xml_commit_id != "" and xml_commit_id != "{}":
                        logger.info(" xml中配置react-widget模板source：%s ，commitId：%s, build-tool：%s" % (
                            source, xml_commit_id, xml_build_tool))

                        result_json_obejct["source"] = source
                        result_json_obejct["commit-id"] = xml_commit_id
                        result_json_obejct["build-tool"] = xml_build_tool
        return result_json_obejct

    def _get_snapshot_templates_json_source(self, workspace_path):
        result_json_obejct = {}
        git_templates_file_path = os.path.join(workspace_path, "target/snapshot_template.json")
        if os.path.exists(git_templates_file_path):
            snapshot_templates = read_file_content(git_templates_file_path)
            snapshot_templates_json = json.loads(snapshot_templates)
            for snapshot_object in snapshot_templates_json:
                if isinstance(snapshot_object, dict):
                    type = snapshot_object.get("type", "")
                    if type == "react-widget":
                        templates = snapshot_object.get("template", "")
                        snapshot_commit_id = snapshot_object.get("commitId", "")
                        snapshot_build_tool = snapshot_object.get("buildTool", "")
                        if templates != "" and snapshot_commit_id != "":
                            logger.info(" snapshot中配置react-widget模板template：%s,commitId：%s,buildTool：%s" % (
                                templates, snapshot_commit_id, snapshot_build_tool))

                            result_json_obejct["template"] = templates
                            result_json_obejct["commitId"] = snapshot_commit_id
                            result_json_obejct["buildTool"] = snapshot_build_tool
        return result_json_obejct
