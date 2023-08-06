#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
应用工厂-构建离线H5轻应用插件
"""

import sys
import argparse
import traceback
import apf_ci as ci
from apf_ci.lite_app.local_h5.builder.local_h5_builder import *

def main(argv):
    parser = argparse.ArgumentParser(prog="%s local-h5" % ci.__title__, description="应用工厂-构建离线H5轻应用插件")
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
        local_h5 = LocalH5Builder()
        local_h5.perform(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-应用配置命令入口
    """
    sys.exit(main(sys.argv[1:]))