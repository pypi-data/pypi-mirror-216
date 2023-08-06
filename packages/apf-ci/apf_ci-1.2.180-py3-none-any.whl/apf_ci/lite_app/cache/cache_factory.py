#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.lite_enum.cache_enum import *
# react cache
from apf_ci.lite_app.cache.first_level_react_cache import *
from apf_ci.lite_app.cache.second_level_react_cache import *
from apf_ci.lite_app.cache.three_level_react_cache import *
# h5 cache
from apf_ci.lite_app.cache.first_level_local_h5_cache import *
from apf_ci.lite_app.cache.second_level_local_h5_cache import *
from apf_ci.lite_app.cache.three_level_local_h5_cache import *
import traceback
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger

class CacheFactory:
    @staticmethod
    def get_cache(cache_enum):
        cache = None
        try:
            # react枚举 和 h5枚举判断
            if cache_enum == CacheEnum.FIRST_LEVEL_REACT_CACHE:
                cache = FirstLevelReactCache()
            elif cache_enum == CacheEnum.SECOND_LEVEL_REACT_CACHE:
                cache = SecondLevelReactCache()
            elif cache_enum == CacheEnum.THREE_LEVEL_REACT_CACHE:
                cache = ThreeLevelReactCache()
            elif cache_enum == CacheEnum.FIRST_LEVEL_LOCAL_H5_CACHE:
                cache = FirstLevelLocalH5Cache()
            elif cache_enum == CacheEnum.SECOND_LEVEL_LOCAL_H5_CACHE:
                cache = SecondLevelLocalH5Cache()
            elif cache_enum == CacheEnum.THREE_LEVEL_LOCAL_H5_CACHE:
                cache = ThreeLevelLocalH5Cache()
        except Exception:
            error_message = "实例化缓存对象失败"
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
        return cache
