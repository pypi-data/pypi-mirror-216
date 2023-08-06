#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

from apf_ci.util.log_factory.logger_factory import LoggerFactory
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_factory.log_error_message import LogErrorMessage

from apf_ci.util.log_factory.logger_enum import LoggerEnum


class Logger():
    def __init__(self):
        self.is_file_init = False
        self.is_delay_init = False
        self.logger = ''
        self.logger_file = ''
        # 初始化 打印日志类
        self.logger = LoggerFactory.get_logger(LoggerEnum.PRINT_LOGGER)
        pass

    def delay_init(self, is_delay_init):
        """
         是否要延迟初始化日志文件，防止和git clone 命令冲突
         必须在调用任意一条日志输出前调用
         """
        self.is_delay_init = is_delay_init

    def init_file_log(self):
        """
        初始化日志对象。该对象可将传入的Message打印到控制台中。
        由于工作空间初始化，可能会清空工作空间，之类在具体调用时候再初始化log文件
         """
        if not self.is_delay_init:
        # 初始化 输出到文件日志类
            self.logger_file = LoggerFactory.get_logger(LoggerEnum.FILE_WRITE_LOGGER)
            self.is_file_init = True
            self.info('开始输出日志到log文件中')

    def debug(self, message, is_print=False):
        if not self.is_file_init:
            self.init_file_log()

        if self.is_file_init:
            self.logger_file.debug(message)

        if (not self.is_file_init) or is_print:
            self.logger.debug(message)


    def info(self, message):
        if not self.is_file_init:
            self.init_file_log()

        if self.is_file_init:
            self.logger_file.info(message)

        self.logger.info(message)


    def warning(self, message):
        if not self.is_file_init:
            self.init_file_log()
        if self.is_file_init:
            self.logger_file.warning(message)
        self.logger.warning(message)


    def error(self, code, message):
        """
        按照 指定格式输出错误日志
        """

        error_message = {}
        error_message['code'] = code
        if code in LoggerErrorEnum:
            error_message['code'] = code.value
        error_message['message'] = message
        #error_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #error_message['time'] = error_time

        if not self.is_file_init:
            self.init_file_log()

        if self.is_file_init:
            self.logger_file.error(error_message)

        self.logger.error(error_message)

    #def error_plus(self, log_error_msg: LogErrorMessage):
    #    """
    #    按照 指定格式输出错误日志，暂不使用
    #    """
    #    if not self.is_file_init:
    #        self.init_file_log()
    #
    #    if self.is_file_init:
    #        self.logger_file.error(log_error_msg)
    #
    #    self.logger.error(log_error_msg)

    def critical(self, message):
        self.logger.critical(message)
        #self.logger_file.critical(message)


logger = Logger()

if __name__ == "__main__":
    #raise  Exception('1111')
    logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, '超时')
    #log_msg = LogErrorMessage()
    #log_msg.reason = "测试报错"
    #logger.error_plus(log_msg)
