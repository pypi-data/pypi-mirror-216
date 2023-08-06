#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from apf_ci.lite_app.cache.abstract_cache import *
from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.lite_app.model.cache_bo import *
from apf_ci.lite_app.model.js_package_cache import *
from apf_ci.lite_app.lite_enum.app_type_enum import *


class AbstractSecondLevelCache(AbstractCache, metaclass=ABCMeta):

    @abstractmethod
    def get_second_level_cache_md5(self, cache_factor):
        """
        通过缓存因素获取二级缓存Md5值
        :return:
        """
        pass

    @abstractmethod
    def save_second_level_cache(self, npm_dto, cache_md5):
        """
        压缩，上传，并保存二级缓存和本地缓存数据
        :param npm_dto:
        :param cache_md5:
        :return:
        """
        pass

    def get_js_package_cache(self, npm_dto, cache_md5, build_path):
        param_map = npm_dto.param_map
        cs_config = param_map.get("csConfig")
        app_type = param_map.get("build_app_type", "")
        module_name = npm_dto.module_name
        js_package_name = npm_dto.js_package_name
        js_version = str(npm_dto.js_version)
        js_publish_time = str(npm_dto.js_publish_time)

        zip_file_name = cache_md5 + ".zip"
        upload_cs_path = js_package_name + "/" + js_version + "/" + js_publish_time

        # 压缩、上传操作
        workspace_path = os.getcwd()
        module_path = os.path.join(workspace_path, build_path, module_name)
        zip_file_path = os.path.join(module_path, "2_" + zip_file_name)
        dist_path = ""
        if build_path == "target/local_h5":
            dist_path = os.path.join(module_path, "dist")
        elif build_path == "target/react":
            dist_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))

        nd_dependencies_file_path = os.path.join(module_path, "ndDependencies.version")
        # 压缩
        files_list = []
        files_list.append(dist_path)
        files_list.append(nd_dependencies_file_path)
        zip_multi_file(zip_file_path, files_list, False)
        # 上传二级缓存到cs上
        upload_file_to_cs(zip_file_path, upload_cs_path, zip_file_name, cs_config)

        # 保存缓存数据到服务上
        host_path = cs_config.host + "/static/" + cs_config.server_name + "/" + upload_cs_path
        zip_cs_path = host_path.replace("http://cs.101.com", "https://gcdncs.101.com") + "/" + zip_file_name

        js_package_cache = JsPackageCache()
        js_package_cache.package_name = js_package_name
        js_package_cache.version = js_version
        js_package_cache.publish_time = js_publish_time
        js_package_cache.cache_md5 = cache_md5
        js_package_cache.cache_level = "2"
        js_package_cache.url = zip_cs_path
        return js_package_cache

    def get_cache_md5(self, cache_factor):
        return self.get_second_level_cache_md5(cache_factor)

    def get_cache(self, cache_md5, param_map):
        cache_bo = None
        lite_app_host = param_map["lite_app_server"]
        cache_url = self.get_cache_url(lite_app_host, "2", cache_md5)

        if cache_url is not None and cache_url != "":
            cache_bo = CacheBO()
            cache_bo.zip_url = cache_url
            cache_bo.second_level_cache_md5 = cache_md5
            logger.debug("取到二级缓存: %s" % cache_bo.tostring_format())
        return cache_bo

    def save_cache(self, npm_dto, cache_md5):
        js_package_cache = self.save_second_level_cache(npm_dto, cache_md5)
        request_body_str = json.dumps(js_package_cache.__dict__)
        request_body = json.loads(request_body_str)

        lite_app_host = npm_dto.param_map.get("lite_app_server", "")
        cache_url = self.get_cache_url(lite_app_host, "2", cache_md5)
        if cache_url != "":
            lite_app_url = lite_app_host + "/v0.1/js"
            post_for_array(lite_app_url, request_body)
