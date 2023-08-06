#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
日志工厂接口类
"""


class ILogger:

    def debug(self, message):
        """
        以debug的格式输出日志
        :return:
        """
        pass

    def info(self, message):
        """
        以debug的格式输出日志
        :return:
        """
        pass

    def warning(self, message):
        """
        以debug的格式输出日志
        :return:
        """
        pass

    def error(self, message):
        """
        以debug的格式输出日志
        :return:
        """
        pass

    def critical(self, message):
        """
        以debug的格式输出日志
        :return:
        """
        pass
