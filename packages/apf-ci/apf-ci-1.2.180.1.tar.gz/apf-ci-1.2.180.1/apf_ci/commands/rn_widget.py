#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
React Native颗粒本地调试工具
"""

__author__ = 'LianGuoQing'

import sys
import os
import json
import platform
import argparse
import traceback


import apf_ci as ci
from apf_ci.rn_widget.rn_widget import init_rn_widget



def main(argv):
    """
    从命令行中获取构建参数
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser(prog="%s rn-widget" % ci.__title__, description="React Native颗粒本地调试工具")
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
        "-e",
        "--envJenkins",
        type=int,
        choices=[1, 2, 5, 8],
        default=8,
        help="默认值8，环境配置代码：1-开发库，2-测试库，5-预生产库，8-正式库",
    )

    parser.add_argument(
        "-b",
        "--buildToolVersion",
        default="",
        help="构建工具版本"
    )

    parser.add_argument(
        "-c",
        "--commitId",
        default="",
        help="git模板工程commitId"
    )

    parser.add_argument(
        "-d",
        "--isDev",
        default="",
        help="是否开发版本"
    )

    parser.add_argument(
        "-r",
        "--resetCache",
        type=str,
        choices=["true", "false"],
        default="false",
        help="是否重置缓存，默认值false",
    )

    parser.add_argument(
        "-l",
        "--isLocal",
        type=str,
        choices=["true", "false"],
        default="true",
        help="是否本地构建，默认值true"
    )
    try:
        args = parser.parse_args(argv)
        init_rn_widget(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)





if __name__ == "__main__":
    """
    执行React Native颗粒本地调试工具命令入口
    """

    sys.exit(main(sys.argv[1:]))