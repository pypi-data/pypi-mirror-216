#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
初始化全局变量
"""

__author__ = 'LianGuoQing'

import sys
import argparse
import traceback

from apf_ci.init.init_global_variable_service import main as init_variable
import apf_ci as ci

def main(argv):
    parser = argparse.ArgumentParser(prog="%s variable" % ci.__title__, description="初始化全局变量")
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
        "versionId",
        help="SDP门户ID"
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
    try:
        args = parser.parse_args(argv)
        init_variable(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    """
    执行初始化全局变量命令入口
    """
    sys.exit(main(sys.argv[1:]))