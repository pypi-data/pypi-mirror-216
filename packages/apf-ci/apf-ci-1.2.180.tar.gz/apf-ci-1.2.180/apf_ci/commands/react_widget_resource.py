#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-构建react颗粒默认资源插件
"""

import argparse
import os
import sys
import traceback

import apf_ci as ci
from apf_ci.react_widget_resource.builder.react_widget_resource_builder import ReactWidgetResourceBuilder
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


def main(argv):
    parser = argparse.ArgumentParser(prog="%s react-widget-resource" % ci.__title__, description="应用工厂-构建react颗粒默认资源插件")
    # 暂时不需要参数
    # parser.add_argument(
    #     "-l",
    #     "--isLocal",
    #     type=str,
    #     choices=["true", "false"],
    #     default="false",
    #     help="是否本地构建，默认值false",
    # )
    # args = parser.parse_args(argv)
    try:
        git_repository = os.getenv("reactWidgetResourceTemplateUrl", "")
        commit_id = os.getenv("reactWidgetResourceCommitId", "")
        build_tool = os.getenv("reactWidgetResourceBuildTool", "")
        react_widget_resource = ReactWidgetResourceBuilder(git_repository, commit_id, build_tool)
        react_widget_resource.perform()
    except Exception as e:
        error_message = 'react颗粒默认资源构建失败'
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    """
    执行应用工厂-应用配置命令入口
    """
    sys.exit(main(sys.argv[1:]))