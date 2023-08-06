#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
应用工厂-构建离线H5轻应用插件
"""

import argparse
import apf_ci as ci
from apf_ci.lite_app.local_h5.builder.local_h5_builder import *
from apf_ci.flutter.flutter import *

def main(argv):
    parser = argparse.ArgumentParser(prog="%s app-factory-flutter" % ci.__title__, description="应用工厂-构建flutter插件")
    try:
        args = parser.parse_args(argv)
        flutter = FlutterService()
        flutter.perform(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    执行应用工厂-应用配置命令入口
    """
    sys.exit(main(sys.argv[1:]))