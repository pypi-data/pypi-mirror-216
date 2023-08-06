#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
hook模块
"""

__author__ = 'LianGuoQing'

import os
import subprocess
import traceback

from apf_ci.util.jenkins_utils import envs_value
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.execute_command_utils import call_result

def exec_cmd(cmd_array, *, check=True, chdir=None):
    logger.info("执行命令: %s" % ' '.join(cmd_array))
    r = subprocess.run(cmd_array, stdout=subprocess.PIPE, text=True, check=check, cwd=chdir)
    return r.stdout


def exec_ruby_hook(hook_name):
    workspace_root = os.getcwd()
    workdir = workspace_root + '/Scripts'
    try:
        return exec_cmd_in_rvm([
            'ruby',
            '-r',
            './main.rb',
            '-e',
            "SDPScript.%s" % hook_name
        ], chdir=workdir)
    except Exception:
        traceback.print_exc()
        return None


def exec_cmd_in_rvm(cmd_array, *, check=True, chdir=None):
    workspace_root = os.getcwd()
    cmd_prefix = "rvm use %s" % workspace_root
    cmd = ' '.join(cmd_array)
    logger.info("在 ruby 环境中执行指令: %s" % cmd)
    cmd = cmd_prefix + ' && ' + cmd
    r = subprocess.run(['bash', '-l', '-c', cmd], stdout=subprocess.PIPE, text=True, check=check, cwd=chdir)
    return r.stdout


class HookService:
    def __init__(self, app_type):
        self.app_type = app_type

    def hook(self, method, gradle_home=None, is_local=False):
        workspace_path = os.getcwd()

        if self.app_type.lower() == "android":
            if gradle_home == None or gradle_home == '':
                gradle_home = 'GRADLE_HOME_SHELL'
            if os.path.exists(workspace_path + "/script/hook.gradle"):
                gradle_home_shell = envs_value(gradle_home, is_local)
                logger.debug(" gradle hook shell execute finish：%s/bin/gradle -b ./script/hook.gradle -Pmethod=%s" % (
                    gradle_home_shell, method))
                retcode = call_result(
                    [gradle_home_shell + "/bin/gradle", "-b", "./script/hook.gradle", "-Pmethod=" + method])
                logger.debug('retcode=%s' % retcode)
        elif self.app_type.lower() == "ios":
            exec_ruby_hook(method)
