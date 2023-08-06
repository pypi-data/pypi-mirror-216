
"""
flutter 命令相关工具类
使用subprocess 模块调用命令行
需要区分运行系统，windows和linux有所不同
"""

import sys
import subprocess
import platform
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.string_utils import StringUtils

def execute_command(command_array, need_print=True, chdir=None):
    return_info = subprocess.Popen(command_array, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=chdir)
    output, error = return_info.communicate()
    if output is not None:
        output = output.decode('utf-8')
    if error is not None:
        error = error.decode('utf-8')
    return_code = return_info.wait()
    if need_print:
        if not StringUtils.is_string_empty(output):
            final_output = "Command Output:\n" + output
            sys.__stdout__.write(final_output)
            sys.__stdout__.flush()
        if not StringUtils.is_string_empty(error):
            final_error = "Command Error Output:\n" + error
            sys.__stdout__.write(final_error)
            sys.__stdout__.flush()
    if return_code != 0:
        raise Exception('[ERROR] 执行失败')
    return output, error, return_code


# def execute_command_backup(command_array, need_print=True, chdir=None):
#     if not command_array:
#         error_message = "执行的命令不能为空"
#         logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
#         return
#     if not isinstance(command_array, list):
#         error_message = "执行的命令必须为list，格式为:['xx','xx','xx','xx']"
#         logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
#         return
#     platform_name = platform.system()
#     if platform_name == 'Windows':
#         return subprocess.call(command_array, shell=True, cwd=chdir)
#     else:
#         return __execute_popen_command(command_array, need_print, chdir)
#
#
# def __execute_popen_command(popenargs, need_print, chdir):
#     popen = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=chdir)
#     result = ""
#     error_result = ""
#     end_code = 0
#     while True:
#         next_line = popen.stdout.readline()
#         next_error_line = popen.stderr.readline()
#         end_code = popen.poll()
#         if next_line == '' and next_error_line == '' and end_code != None:
#             break
#         result += next_line
#         error_result += next_error_line
#         if need_print:
#             sys.__stdout__.write(next_line)
#             sys.__stdout__.flush()
#     logger.info("执行完成. end_code=" + str(end_code) + " error_result=" + error_result + "result=" + result)
#     return result, error_result, end_code
