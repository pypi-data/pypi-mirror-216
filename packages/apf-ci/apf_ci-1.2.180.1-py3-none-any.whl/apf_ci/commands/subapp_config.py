#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-子应用配置插件
"""

__author__ = '370418'

import sys
import argparse
import traceback
from apf_ci.subapp_config.subapp_config_init import main as subapp_config_init
import apf_ci as ci


def main(argv):
    parser = argparse.ArgumentParser(prog="%s subapp-config" % ci.__title__, description="应用工厂-子应用配置插件")
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
        "appVersionId",
        type=str,
        help="应用版本号"
    )
    parser.add_argument(
        "callbackQueue",
        type=str,
        help="回调队列名称"
    )
    parser.add_argument(
        "versionId",
        type=str,
        help="SDP门户ID"
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
        #init_subapp_config(args)
        subapp_config_init(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-子应用配置插件
    """
    sys.exit(main(sys.argv[1:]))