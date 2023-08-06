#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.util.execute_command_utils import execute_command

from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger

class EnsureTemplateBuilder:

    def __init__(self, storage_host, template_url, template_commit_id, template_build_tool):
        self.storage_host = storage_host
        self.template_url = template_url
        self.template_commit_id = template_commit_id
        self.template_build_tool = template_build_tool

    def perform(self, variables_json):
        workspace_path = os.getcwd()
        app_type = variables_json["build_app_type"]
        npm_registry = variables_json["npm_registry"]
        git_repository = ""
        commit_id = ""
        build_tool = ""

        # 模板工程地址优先级：jenkinsJob > snapshot > xml > server
        if self.template_url != "" and self.template_commit_id != "" and self.template_build_tool != "":
            git_repository = self.template_url
            commit_id = self.template_commit_id
            build_tool = self.template_build_tool
        else:
            git_templates_jsonobject = {}
            git_templates_file_path = os.path.join(workspace_path, "target/git_templates.json")
            if os.path.exists(git_templates_file_path):
                git_templates = read_file_content(git_templates_file_path)
                git_templates_json = json.loads(git_templates)
                node_json_object = git_templates_json.get("react-widget")
                if node_json_object:
                    git_json = node_json_object.get("git")
                    if git_json:
                        source = git_json.get("source")
                        xml_commit_id = git_json.get("commit-id")
                        xml_build_tool = node_json_object.get("build-tool")
                        if source and xml_commit_id and xml_build_tool:
                            logger.info(" xml中配置react-widget模板source：%s, commitId：%s, build-tool：%s" % (
                            source, xml_commit_id, xml_build_tool))

                        git_templates_jsonobject = {
                            "source": source,
                            "commit-id": xml_commit_id,
                            "build-tool": xml_build_tool
                        }
            if git_templates_jsonobject:
                # xml配置模板
                git_repository = git_templates_jsonobject.get("source")
                commit_id = git_templates_jsonobject.get("commit-id")
                build_tool = git_templates_jsonobject.get("build-tool")
            else:
                snapshot_templates_jsonobejct = {}
                git_templates_file_path = os.path.join(workspace_path, "target/snapshot_template.json")
                if os.path.exists(git_templates_file_path):
                    snapshot_templates = read_file_content(git_templates_file_path)
                    snapshot_templates_arr = json.loads(snapshot_templates)
                    for snapshot_object in snapshot_templates_arr:
                        if isinstance(snapshot_object, dict):
                            snapshot_type = snapshot_object.get("type", "")
                            if snapshot_type == "react-widget":
                                templates = snapshot_object.get("template", "")
                                snapshot_commit_id = snapshot_object.get("commitId", "")
                                snapshot_build_tool = snapshot_object.get("buildTool", "")
                                if templates != "" and snapshot_commit_id != "":
                                    logger.info(" snapshot中配置react-widget模板template：%s,commitId：%s,buildTool：%s" % (
                                        templates, snapshot_commit_id, snapshot_build_tool))

                                    snapshot_templates_jsonobejct = {"template": templates,
                                                                     "commitId": snapshot_commit_id,
                                                                     "buildTool": snapshot_build_tool}
                if snapshot_templates_jsonobejct:
                    # snapshot配置模板
                    git_repository = snapshot_templates_jsonobejct.get("template")
                    commit_id = snapshot_templates_jsonobejct.get("commitId")
                    build_tool = snapshot_templates_jsonobejct.get("buildTool")
                else:
                    # server配置模板
                    app_template_url = self.storage_host + "/v0.8/template/react-widget"
                    app_template_json = get_data(app_template_url)

                    git_repository = app_template_json.get("template", "")
                    commit_id = app_template_json.get("commit_id", "")
                    build_tool = app_template_json.get("build_tool", "")
        variables_json["git_repository"] = git_repository
        variables_json["commit_id"] = commit_id
        variables_json["build_tool"] = build_tool
        logger.debug(" 取得模板配置 git_repository：%s" % git_repository)
        logger.debug(" 取得模板配置 commit_id：%s" % commit_id)
        logger.debug(" 取得模板配置 build_tool：%s" % build_tool)
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
        self.set_npm_config(app_type, npm_registry)

    def set_npm_config(self, app_type, npm_registry):
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, "target")
        react_widget_path = os.path.join(target_path, "react_widget")
        if not os.path.exists(react_widget_path):
            os.makedirs(react_widget_path)
        try:
            logger.info(" 执行命令： npm config set tmp=%s" % react_widget_path)
            execute_command(['npm', 'config', 'set', 'tmp=%s' % react_widget_path], chdir=react_widget_path)

            logger.info(" 执行命令： npm config set registry='%s'" % npm_registry)
            execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=react_widget_path)

            if app_type.lower() == "android":
                # 设置npm构建缓存地址到 / tmp下
                logger.info(" 执行命令： npm config set unsafe-perm true")
        except Exception as e:
            error_message = "网络异常： %s" % e
            logger.error(LoggerErrorEnum.NETWORK_CONNECT_LOST, error_message)
            traceback.print_exc()
            sys.exit(1)
