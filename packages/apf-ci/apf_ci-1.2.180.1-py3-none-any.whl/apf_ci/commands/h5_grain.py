#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
应用工厂-构建H5颗粒插件
"""

import sys
import os
import argparse
import traceback
import apf_ci as ci
from apf_ci.h5_grain.builder.h5_grain_builder import H5GrainBuilder

def main(argv):
    parser = argparse.ArgumentParser(prog="%s h5-grain" % ci.__title__, description="应用工厂-构建H5颗粒插件")
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
        # 参数取的是jenkins构建参数的值
        git_repository = os.getenv("H5GrainTemplateUrl", "")
        commit_id = os.getenv("H5GrainCommitId", "")
        build_tool = os.getenv("H5GrainBuildCommand", "")
        h5grain = H5GrainBuilder(git_repository, commit_id, build_tool)
        h5grain.perform(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-应用配置命令入口
    """
    sys.exit(main(sys.argv[1:]))
