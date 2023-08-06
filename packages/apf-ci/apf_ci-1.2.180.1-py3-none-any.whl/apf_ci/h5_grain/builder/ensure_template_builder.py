#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import platform

from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.log_utils import logger

class EnsureTemplateBuilder:
    def __init__(self, git_repository, commit_id):
        self.git_repository = git_repository
        self.commit_id = commit_id

    def perform(self):
        workspace_path = os.getcwd()
        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")
        if not os.path.exists(h5_grain_path):
            os.mkdir(h5_grain_path)

        if platform.system() == "Windows":
            logger.debug(" 执行命令 git clone %s ." % self.git_repository)
            execute_command(['git', 'clone', self.git_repository, '.'], chdir=h5_grain_path)
            logger.debug(" 执行命令 git checkout %s" % self.commit_id)
            execute_command(['git', 'checkout', self.commit_id], chdir=h5_grain_path)
        else:
            logger.debug(" 执行命令 /usr/bin/git clone %s ." % self.git_repository)
            execute_command(['/usr/bin/git', 'clone', self.git_repository, '.'], chdir=h5_grain_path)
            logger.debug(" 执行命令 /usr/bin/git checkout %s" % self.commit_id)
            execute_command(['/usr/bin/git', 'checkout', self.commit_id], chdir=h5_grain_path)

        # 判断node_modules是否存在
        node_modules_path = os.path.join(h5_grain_path, "node_modules")
        if os.path.exists(node_modules_path):
            execute_command(['chmod', '755', 'node_modules/.bin/h5-build'], chdir=h5_grain_path)
        return True
