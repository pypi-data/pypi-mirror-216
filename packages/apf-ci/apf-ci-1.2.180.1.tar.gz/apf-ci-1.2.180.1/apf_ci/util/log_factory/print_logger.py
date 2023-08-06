#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from apf_ci.util.log_factory.ilogger import ILogger

"""
控制台打印 日志类
"""


class PrintLogger(ILogger):

    def __init__(self):
        """
       初始化日志对象。该对象可将传入的Message打印到控制台中。
        """
        # 创建logger对象，输出到控制台logger
        self.logger = logging.getLogger("jenkins_console_printer")
        self.logger.setLevel(logging.DEBUG)
        # 判断日志的handler列表是否为空，为空的时候才初始化，否则不初始化（用于防止重复实例对象，导致重复输出日志的问题。）
        if not self.logger.handlers:
            self.__init_logger()

    def __init_logger(self):
        # 创建一个handler，用于打印日志到屏幕上，替换掉print方法，输出的日志级别为INFO以上
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        sh.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(sh)


    def debug(self, message):
        """
        根据日志输出级别，来定输出的格式。将Log内容输出到控制台
        :param message: 日志字符串
        :return:
        """
        self.logger.debug("[DEBUG] %s " % message)

    def info(self, message):
        self.logger.info("[INFO] %s " % message)

    def warning(self, message):
        self.logger.warning("[WARN] %s " % message)

    def error(self, message):
        self.logger.error("[ERROR] %s " % message)

    def critical(self, message):
        self.logger.critical("[CRITICAL] %s " % message)
