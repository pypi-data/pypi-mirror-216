#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum

"""
Logger类型枚举
"""

class LoggerEnum(Enum):
    # 控制台打印logger
    PRINT_LOGGER = "console_print_logger"
    # 日志输入文件logger
    FILE_WRITE_LOGGER = "file_write_logger"

