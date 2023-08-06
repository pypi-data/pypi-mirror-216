#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from apf_ci.lite_app.cache.abstract_cache import *
from apf_ci.lite_app.model.cache_bo import *


class AbstractThreeLevelCache(AbstractCache, metaclass=ABCMeta):

    @abstractmethod
    def get_three_level_cache_md5(self, cache_factor):
        """
        通过缓存因素获取三级缓存Md5值
        :return:
        """
        pass

    @abstractmethod
    def get_snapshot_time(self, host):
        """
        压缩，上传，并保存三级缓存和本地缓存数据
        :param npm_dto:
        :param cache_md5:
        :return:
        """
        pass

    def get_cache_md5(self, cache_factor):
        return self.get_three_level_cache_md5(cache_factor)

    def get_cache(self, cache_md5, param_map):
        cache_bo = None

        lite_app_host = param_map["lite_app_server"]
        package_name = param_map["build_package"]
        app_type = param_map["build_app_type"]
        env_target = param_map["envtarget"]

        url_buffer = ""
        url_buffer += lite_app_host
        url_buffer += "/v0.1/app/"
        url_buffer += package_name
        url_buffer += "/"
        url_buffer += app_type
        url_buffer += "/"
        url_buffer += env_target
        url_buffer += "/"
        url_buffer += cache_md5
        url_buffer += "/latest"

        r = requests.get(url_buffer)
        logger.debug(" abstract_three_level_cache 获取三级缓存url_buffer ： %s" % url_buffer)
        if r.status_code != 200:
            error_message = "获取 %s 失败。status_code : %s" % (url_buffer, r.status_code)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            body = ""
        else:
            body = r.content.decode("utf-8")
        if body != "":
            body = json.loads(body)
            logger.debug(" abstract_three_level_cache 取到返回结果: %s" % body)
            items_json_array = body.get("items")
            if items_json_array is not None:
                item_json = items_json_array[0]

                zip_url = item_json["zip_url"]
                host = item_json["host"]
                version_url = item_json["version_url"]
                dependencies = body["dependencies"]

                cache_bo = CacheBO()
                cache_bo.zip_url = zip_url
                cache_bo.host = host
                cache_bo.version_url = version_url
                cache_bo.dependencies = dependencies
                cache_bo.snapshot_time = self.get_snapshot_time(host)
                cache_bo.three_level_cache_md5 = cache_md5

                logger.debug(" 取到三级缓存： %s" % cache_bo.tostring_format())

        return cache_bo
