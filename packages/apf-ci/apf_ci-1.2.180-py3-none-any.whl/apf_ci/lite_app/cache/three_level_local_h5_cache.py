#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.cache.abstract_three_level_cache import *


class ThreeLevelLocalH5Cache(AbstractThreeLevelCache):

    def get_three_level_cache_md5(self, cache_factor):
        three_level_buffer = ""
        three_level_buffer += cache_factor.js_package_name
        three_level_buffer += cache_factor.js_version
        three_level_buffer += str(cache_factor.js_publish_time)
        three_level_buffer += cache_factor.skin_file_md5
        three_level_buffer += cache_factor.i18n_file_md5
        three_level_buffer += cache_factor.build_file_md5
        three_level_buffer += cache_factor.pages_file_md5

        if cache_factor.sub_app == "true":
            three_level_buffer += cache_factor.components_file_md5
            three_level_buffer += cache_factor.service_file_md5
        return self.get_md5(three_level_buffer)

    def get_snapshot_time(self, host):
        begin_index = host.find("/local-h5/") + 10
        end_index = host.rfind("/test")
        snapshot_time = host[begin_index: end_index]
        return snapshot_time
