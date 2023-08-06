#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
使用subprocess 模块调用命令行
需要区分运行系统，windows和linux有所不同
"""

import sys
import subprocess
import platform
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


def execute_command(command_array, need_print=True, chdir=None):
    if not command_array:
        error_message = "执行的命令不能为空"
        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
        return
    if not isinstance(command_array, list):
        error_message = "执行的命令必须为list，格式为:['xx','xx','xx','xx']"
        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
        return
    platform_name = platform.system()
    if platform_name == 'Windows':
        return subprocess.call(command_array, shell=True, cwd=chdir)
    else:
        return __execute_popen_command(command_array, need_print, chdir)


def __execute_popen_command(popenargs, need_print, chdir):
    popen = subprocess.Popen(popenargs, stdout=subprocess.PIPE, universal_newlines=True, cwd=chdir)
    result = ""
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        result += next_line
        if need_print:
            sys.__stdout__.write(next_line)
            sys.__stdout__.flush()
    return result


def call_result(command_array):
    '''
    针对hook命令，支持错误执行，报错并中断构建
    '''
    if platform.system() == 'Windows':
        result = subprocess.call(command_array, shell=True, cwd=None)
    else:
        result = subprocess.call(command_array)
    if result != 0:
        command_str = ""
        for item in command_array:
            command_str = command_str + item + " "
        error_message = "命令 %s 调用失败" % command_str
        #logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
        raise Exception(error_message)
    return result


if __name__ == "__main__":
    #result = execute_command(['npm', 'install', '@sdp.nd/h5-social-notice@16.9.75'], chdir=None)
    # result = execute_command(['echo', 'hello'], False)
    result = call_result(['gradle', 'hello'])
    print(result)
