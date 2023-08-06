#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-动态tab构建插件
"""

__author__ = '370418'

import sys
import argparse
import traceback
from apf_ci.commands.command_const import *
from apf_ci.tab.build.tab_init import main as tab_build
import apf_ci as ci


def main(argv):
    parser = argparse.ArgumentParser(prog="%s dynamic-tab" % ci.__title__, description="应用工厂-动态tab构建插件")
    parser.add_argument(
        "factoryId",
        help="应用工厂ID"
    )
    parser.add_argument(
        "appName",
        type=str,
        help="应用名称"
    )
    parser.add_argument(
        "packageName",
        type=str,
        help="应用包名"
    )
    parser.add_argument(
        "appType",
        type=str,
        help="应用类型"
    )
    parser.add_argument(
        "appVersionId",
        type=str,
        help="应用版本id"
    )
    parser.add_argument(
        "tabVersionId",
        type=str,
        help="动态tab版本id"
    )
    parser.add_argument(
        "versionCode",
        type=str,
        help="版本号"
    )
    parser.add_argument(
        "versionName",
        type=str,
        help="版本名称"
    )
    parser.add_argument(
        "versionDesc",
        type=str,
        help="版本描述"
    )
    env_list = get_environment_config()
    parser.add_argument(
        "envtarget",
        type=str,
        choices=env_list,
        help="环境值"
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
        "-l",
        "--isLocal",
        type=str,
        choices=["true", "false"],
        default="false",
        help="是否本地构建，默认值false",
    )
    try:
        args = parser.parse_args(argv)
        tab_build(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))