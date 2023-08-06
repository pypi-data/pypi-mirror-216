#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-构建空间初始化插件
"""

__author__ = 'LianGuoQing'

import sys
import argparse
import traceback
from apf_ci.app_init.app_init import main as app_init
import apf_ci as ci
import json
from apf_ci.util.file_utils import *
from apf_ci.commands.command_const import *


def main(argv):
    parser = argparse.ArgumentParser(prog="%s app-init" % ci.__title__, description="应用工厂-应用配置插件")
    parser.add_argument(
        "factoryId",
        help="应用工厂ID"
    )

    env_list = get_environment_config()
    parser.add_argument(
        "envtarget",
        type=str,
        choices=env_list,
        help="环境值"
    )

    parser.add_argument(
        "appType",
        type=str,
        choices=[
            "android",
            "ios"
        ],
        help="应用类型"
    )

    parser.add_argument(
        "versionId",
        help="SDP门户ID"
    )
    parser.add_argument(
        "resourceCacheSwitch",
        type=str,
        choices=["true", "false"],
        default="false",
        help="是否关闭缓存，默认值false,关闭"
    )
    parser.add_argument(
        "-e",
        "--envJenkins",
        type=int,
        choices=[1, 2, 5, 8],
        default=8,
        help="默认值8，环境配置代码：1-开发库，2-测试库，5-预生产库，8-正式库",
    )

    parser.add_argument(
        "-g",
        "--gitTemplate",
        default="",
        help="git模板工程地址"
    )

    parser.add_argument(
        "-c",
        "--commitId",
        default="",
        help="git模板工程commitId"
    )

    parser.add_argument(
        "-v",
        "--version2AppFactory",
        default="",
        help="版本信息应用工厂服务"
    )

    parser.add_argument(
        "-l",
        "--isLocal",
        type=str,
        choices=["true", "false"],
        default="false",
        help="是否本地构建，默认值false",
    )
    parser.add_argument(
        "-i",
        "--isLightApp",
        type=str,
        choices=["true", "false"],
        default="false",
        help="是否轻应用构建，默认值false",
    )
    try:
        args = parser.parse_args(argv)
        app_init(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-构建空间初始化命令入口
    """
    sys.exit(main(sys.argv[1:]))