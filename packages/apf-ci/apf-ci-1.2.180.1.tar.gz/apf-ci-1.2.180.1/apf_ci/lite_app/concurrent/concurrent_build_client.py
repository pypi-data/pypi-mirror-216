#!/usr/bin/python3
# -*- coding: utf-8 -*-


from concurrent.futures import ThreadPoolExecutor
import threading
import traceback
import sys

from apf_ci.lite_app.concurrent.react_build_callable import *
from apf_ci.lite_app.concurrent.local_h5_build_callable import *
from apf_ci.util.log_utils import logger
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum


class ConcurrentBuildClient:
    def __init__(self):
        # 原本限制为8个，限制触发到接口的频繁访问，改成4个尝试下
        self.CORE_POOL_SIZE = 4
        self.npm_dto_list = []

    def start(self, build_type):
        size = len(self.npm_dto_list)
        if size > 0:
            logger.debug(" the number of threads in the pool: %s" % self.CORE_POOL_SIZE)

        # 根据build_type实例callable对象
        abstract_callable = None
        if build_type == "h5":
            abstract_callable = LocalH5BuildCallable()
        elif build_type == "react":
            abstract_callable = ReactBuildCallable()

        # python，使用线程池执行任务，返回结果保存在future_result_list中
        future_result_list = []
        if abstract_callable is not None:
            # 创建线程池
            with ThreadPoolExecutor(self.CORE_POOL_SIZE) as executor:
                for npm_dto in self.npm_dto_list:
                    future = executor.submit(abstract_callable.call, npm_dto)

                    future_result_list.append(future)

        # 遍历任务的结果
        for future in future_result_list:
            try:
                # Future返回如果没有完成，则一直循环等待，直到Future返回完成
                while not future.done():
                    pass
                logger.info(" 当前线程: %s => 结果：%s" % (threading.current_thread().getName(), future.result()))
            except Exception:
                error_msg = "线程返回结果异常"
                logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
                traceback.print_exc()
                sys.exit(1)
