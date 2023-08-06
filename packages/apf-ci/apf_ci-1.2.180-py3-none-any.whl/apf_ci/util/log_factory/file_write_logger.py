#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os

from apf_ci.util.log_factory.ilogger import ILogger

"""
日志文件记录 日志类
"""


class FileWriteLogger(ILogger):
    def __init__(self, is_remove_old=False):
        """
        logger目前功能是指定debug级别的日志，将日志存入到指定的文件中
        其他日志还是正常print到构建日志
        """
        # 创建logger对象，输出到控制台logger
        self.logger = logging.getLogger("jenkins_file_writer")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self.__init_logger(is_remove_old)

    def __init_logger(self, is_remove_old=False):
        # 创建日志文件
        log_file_path = os.path.join(os.getcwd(), "jenkins_build_debug.log")
        if not os.path.exists(log_file_path):
            parent_path = os.path.dirname(log_file_path)
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
        else:
            if is_remove_old:
                os.remove(log_file_path)
                #with open(log_file_path, "a",encoding='utf-8') as f:
            #    f.write(b'jenkins构建日志文件记录：\n')

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        #formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - [%(levelname)s]: %(message)s')
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    """
    根据日志输出级别，来定输出的格式。将Log内容输出到控制台
    :param message: 日志字符串
    :return:
    """

    def debug(self, message):
        self.logger.debug("[DEBUG] %s " % message)

    def info(self, message):
        self.logger.info("[INFO] %s " % message)

    def warning(self, message):
        self.logger.warning("[WARN] %s " % message)

    def error(self, message):
        self.logger.error("[ERROR] %s " % message)

    def critical(self, message):
        self.logger.critical("[CRITICAL] %s " % message)
