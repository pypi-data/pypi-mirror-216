#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
应用工厂-安卓构建前准备插件
"""

import sys
import argparse
import traceback
import apf_ci as ci
from apf_ci.android.build_prepare.builder.android_build_prepare_builder import *

def main(argv):
    parser = argparse.ArgumentParser(prog="%s config" % ci.__title__, description="应用工厂-安卓构建前准备插件")
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
        android_prepare_builder = AndroidBuildPrepareBuilder()
        android_prepare_builder.perform(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    """
    执行应用工厂-应用配置命令入口
    """
    sys.exit(main(sys.argv[1:]))