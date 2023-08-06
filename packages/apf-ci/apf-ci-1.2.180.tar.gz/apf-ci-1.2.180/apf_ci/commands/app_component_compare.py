#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-app对比工具插件
"""

__author__ = '370418'

import sys
import argparse
import traceback
from apf_ci.app_component_compare.build.app_component_compare import main as app_component_compare
import apf_ci as ci


def main(argv):
    parser = argparse.ArgumentParser(prog="%s app-component-compare" % ci.__title__, description="应用工厂-app组件对比插件")
    parser.add_argument(
        "appId",
        type=str,
        help="应用id"
    )
    parser.add_argument(
        "factoryId",
        help="应用工厂id"
    )
    parser.add_argument(
        "appCompareId",
        type=str,
        help="应用对比id"
    )
    parser.add_argument(
        "versionFrom",
        type=str,
        help="对比版本1"
    )
    parser.add_argument(
        "versionTo",
        type=str,
        help="对比版本2"
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
        app_component_compare(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))