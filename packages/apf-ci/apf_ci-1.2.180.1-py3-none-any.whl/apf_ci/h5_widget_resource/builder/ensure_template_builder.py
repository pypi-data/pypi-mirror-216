#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import platform
import sys
import traceback

from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.h5_grain.builder.template_builder import TemplateBuilder


class EnsureTemplateBuilder:

    def __init__(self, storage_host, template_url, template_commit_id):
        self.storage_host = storage_host
        self.template_url = template_url
        self.template_commit_id = template_commit_id

    def perform(self, variables_json):
        workspace_path = os.getcwd()

        template_build = TemplateBuilder(self.storage_host, self.template_url, self.template_commit_id)
        template_git_repository, commit_id = template_build.get_git_template(workspace_path)

        variables_json["git_commitid"] = template_git_repository + commit_id

        self.get_git_project_by_repository(template_git_repository, commit_id)
        return True

    def get_git_project_by_repository(self, git_repository, commit_id):
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, "target")
        h5_grain_path = os.path.join(target_path, "h5_grain")

        if not os.path.exists(h5_grain_path):
            os.makedirs(h5_grain_path)

        try:
            platform_name = platform.system()
            if platform_name == 'Windows':
                git_clone_command = ["git", "clone", git_repository, "."]
            else:
                git_clone_command = ["/usr/bin/git", "clone", git_repository, "."]
            logger.info(" 命令: %s, 执行 /usr/bin/git clone %s ." % (git_clone_command, git_repository))
            execute_command(git_clone_command, chdir=h5_grain_path)

            if platform_name == 'Windows':
                git_checkout_command = ["git", "checkout", commit_id]
            else:
                git_checkout_command = ["/usr/bin/git", "checkout", commit_id]
            logger.info(" 命令：%s, 执行 /usr/bin/git checkout %s ." % (git_checkout_command, commit_id))
            execute_command(git_checkout_command, chdir=h5_grain_path)

            node_modules_path = os.path.join(h5_grain_path, "node_modules")
            logger.info(" 下载下来的Node_modules路径为 %s" % node_modules_path)
            if os.path.exists(node_modules_path):
                chmod_command = ["chmod", "755", 'node_modules/.bin/h5-build']
                logger.info(" 命令：%s, 执行 chmod 755 node_modules/.bin/h5-build")
                execute_command(chmod_command, chdir=h5_grain_path)
        except Exception as e:
            error_message = ' 网络异常： %s' % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)
