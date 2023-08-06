#!/usr/bin/python3
# -*- coding:utf-8 -*-

from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *


class TemplateBuilder:
    def __init__(self, storage_host, template_url, template_commit_id):
        self.storage_host = storage_host
        self.template_url = template_url
        self.template_commit_id = template_commit_id

    def perform(self, workspace_path, variables_dict):
        template_git_repository, commit_id = self.get_git_template(workspace_path)
        variables_dict["h5_grain"] = {}
        variables_dict["h5_grain"]["git_repository"] = template_git_repository
        variables_dict["h5_grain"]["commit_id"] = commit_id
        variables_path = os.path.join(workspace_path, "target/variables.json")
        write_content_to_file(variables_path, json.dumps(variables_dict, ensure_ascii=False))
        return True

    def get_git_template(self, workspace_path):
        template_git_repository = ""
        commit_id = ""

        # 模板工程地址优先级：jenkinsJob > xml > snapshot > server
        if self.template_url and self.template_commit_id:
            template_git_repository = self.template_url
            commit_id = self.template_commit_id
        else:
            git_templates_json = {}
            git_templates_file_path = os.path.join(workspace_path, "target/git_templates.json")
            if os.path.exists(git_templates_file_path):
                git_templates = read_file_content(git_templates_file_path)
                git_templates_json_obj = json.loads(git_templates)
                node_json_object = git_templates_json_obj.get("h5-widget")
                if node_json_object:
                    git_json_object = node_json_object.get("git")
                    if git_json_object:
                        source = git_json_object.get("source")
                        commit_id = git_json_object.get("commit-id")

                        if source and commit_id:
                            logger.debug(" xml中配置h5-widget模板source： %s,commitId： %s" % (source, commit_id))
                            git_templates_json = git_json_object
            # xml配置模板
            if git_templates_json:
                template_git_repository = git_templates_json.get("source")
                commit_id = git_templates_json.get("commit-id")
            else:
                snapshot_templates_json = {}
                snapshot_template_file_path = os.path.join(workspace_path, "target/snapshot_template.json")
                if os.path.exists(snapshot_template_file_path):
                    snapshot_template_content = read_file_content(snapshot_template_file_path)
                    snapshot_template_arr = json.loads(snapshot_template_content)
                    for object in snapshot_template_arr:
                        if not isinstance(object, dict):
                            continue
                        type = object.get("type")
                        if type.lower() != "widget":
                            continue
                        template = object.get("template")
                        commit_id = object.get("commitId")
                        if template and commit_id:
                            logger.debug(" snapshot中配置h5-widget模板template：%s, commitId：%s" % (template, commit_id))

                            git_json_object = {
                                "template": template,
                                "commitId": commit_id
                            }
                            snapshot_templates_json = git_json_object
                            break
                # snapshot配置模板
                if snapshot_templates_json:
                    template_git_repository = snapshot_templates_json.get("template")
                    commit_id = snapshot_templates_json.get("commitId")
                else:
                    # server配置模板
                    app_template_url = self.storage_host + "v0.8/template/widget"
                    response_body = get_data(app_template_url)
                    template_git_repository = response_body.get("template")
                    commit_id = response_body.get("commit_id")
        return template_git_repository, commit_id

