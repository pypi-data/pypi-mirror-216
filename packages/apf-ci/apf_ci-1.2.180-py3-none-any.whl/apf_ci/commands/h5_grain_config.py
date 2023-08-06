#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-轻应用配置插件
"""

__author__ = '370418'

import sys
import argparse
import traceback
from apf_ci.h5_grain_config.h5_grain_init import main as h5_grain_init
import apf_ci as ci


def main(argv):
    parser = argparse.ArgumentParser(prog="%s h5-grain-config" % ci.__title__, description="应用工厂-轻应用配置插件")
    parser.add_argument(
        "factoryId",
        help="应用工厂ID"
    )

    parser.add_argument(
        "envtarget",
        type=str,
        choices=[
            "development",
            "test",
            "preproduction",
            "product",
            "aws",
            "party",
            "aws-california",
            "aws-california-wx",
            "wjt",
            "hk",
            "snwjt",
            "promethean",
            "global-beta",
            "global"
        ],
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
        "appName",
        type=str,
        help="应用名称"
    )
    parser.add_argument(
        "componentType",
        type=str,
        help="组件类型"
    )
    parser.add_argument(
        "appVersionId",
        type=str,
        help="应用版本号"
    )
    parser.add_argument(
        "packageName",
        type=str,
        help="包名"
    )
    parser.add_argument(
        "versionCode",
        type=str,
        help="应用版本"
    )
    parser.add_argument(
        "buildVersion",
        type=str,
        help="构建应用版本"
    )
    parser.add_argument(
        "liteAppUpdateTime",
        type=str,
        help="轻应用更新时间"
    )
    parser.add_argument(
        "-c",
        "--comTestType",
        type=str,
        default="",
        help="严格模式下区分参数？"
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
        #h5_grain_config(args)
        h5_grain_init(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-轻应用配置插件
    """
    sys.exit(main(sys.argv[1:]))