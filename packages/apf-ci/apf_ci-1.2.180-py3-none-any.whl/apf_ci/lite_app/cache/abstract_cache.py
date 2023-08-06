#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta
from apf_ci.lite_app.cache.icache import *
from apf_ci.util import md5_utils
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger

class AbstractCache(ICache, metaclass=ABCMeta):

    def get_md5(self, s):
        return md5_utils.get_md5(s)

    def get_cache_url(self, lite_app_host, cache_level, cache_md5):
        cache_url = ""
        url_buffer = lite_app_host + "/v0.1/js/" + cache_level + "/" + cache_md5

        body = {}
        response = None
        for i in range(3):
            logger.debug(" 取第[%s]等级的缓存数据:%s"% (cache_level, url_buffer))
            response = requests.get(url_buffer, timeout=300)
            if response.status_code != 200:
                error_message = "获取 %s 超时300s,失败。status_code : %s" % (url_buffer, response.status_code)
                logger.error(LoggerErrorEnum.TIME_OUT, error_message)
                if i == 2:
                    sys.exit(1)
                time.sleep(0.5)
            else:
                break
        content = response.content.decode('utf-8')
        if content:
            body = json.loads(content)
        if body:
            cache_url = body["url"]
        return cache_url
