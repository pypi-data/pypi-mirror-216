#!/usr/bin/python3
# -*- coding: utf-8 -*-
import traceback

from apf_ci.util.log_factory.file_write_logger import FileWriteLogger
from apf_ci.util.log_factory.logger_enum import LoggerEnum
from apf_ci.util.log_factory.print_logger import PrintLogger

"""
二次封装logger模块。logger单例工厂
"""

class LoggerFactory:
    # 单例对象logger
    __print_logger = None
    __file_logger = None

    @staticmethod
    def get_logger(log_enum=LoggerEnum.PRINT_LOGGER):
        """
        创建logger对象，默认生成为控制台输出类型的Logger
        :param log_enum:
        :return:
        """
        try:
            if log_enum == LoggerEnum.PRINT_LOGGER:
                if not LoggerFactory.__print_logger:
                    LoggerFactory.__print_logger = PrintLogger()
                return LoggerFactory.__print_logger
            elif log_enum == LoggerEnum.FILE_WRITE_LOGGER:
                if not LoggerFactory.__file_logger:
                    LoggerFactory.__file_logger = FileWriteLogger()
                return LoggerFactory.__file_logger
        except Exception as e:
            print("[ERROR] 实例化缓存对象失败 %s" % e)
            traceback.print_exc()
