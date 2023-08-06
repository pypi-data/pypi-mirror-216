#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
apf-ci模块
"""

__author__ = 'LianGuoQing'

import sys

from apf_ci.cli import dispatch

def main():
    try:
        return dispatch(sys.argv[1:])
    except Exception as exc:
        return '{0}: {1}'.format(
            exc.__class__.__name__,
            exc.args[0],
        )

if __name__ == "__main__":
    """
    执行apf-ci命令入口
    """
    sys.exit(main())