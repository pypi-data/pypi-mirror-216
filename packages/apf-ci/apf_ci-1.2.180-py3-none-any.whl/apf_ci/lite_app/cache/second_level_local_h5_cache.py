#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.cache.abstract_second_level_cache import *


class SecondLevelLocalH5Cache(AbstractSecondLevelCache):

    def get_second_level_cache_md5(self, cache_factor):
        second_level_buffer = ""
        second_level_buffer += cache_factor.js_package_name
        second_level_buffer += cache_factor.js_version
        second_level_buffer += str(cache_factor.js_publish_time)
        second_level_buffer += cache_factor.skin_file_md5
        second_level_buffer += cache_factor.i18n_file_md5
        return self.get_md5(second_level_buffer)

    def save_second_level_cache(self, npm_dto, cache_md5):
        return self.get_js_package_cache(npm_dto, cache_md5, "target/local_h5")
