#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.cache.abstract_first_level_cache import *


class FirstLevelLocalH5Cache(AbstractFirstLevelCache):

    def get_first_level_cache_md5(self, cache_factor):
        first_level_buffer = ""
        first_level_buffer += cache_factor.js_package_name
        first_level_buffer += cache_factor.js_version
        first_level_buffer += str(cache_factor.js_publish_time)
        return self.get_md5(first_level_buffer)

    def save_first_level_cache(self, npm_dto, cache_md5):
        return self.get_js_package_cache(npm_dto, cache_md5, "target/local_h5")
