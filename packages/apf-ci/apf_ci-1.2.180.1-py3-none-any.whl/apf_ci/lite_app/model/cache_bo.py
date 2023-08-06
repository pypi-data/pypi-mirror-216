#!/usr/bin/python3
# -*- coding: utf-8 -*-

class CacheBO:
    def __init__(self):
        self.host = ""
        self.zip_url = ""
        self.version_url = ""
        self.dependencies = ""
        self.snapshot_time = ""
        self.first_level_cache_md5 = ""
        self.second_level_cache_md5 = ""
        self.three_level_cache_md5 = ""
        self.cache_level = ""

    def tostring_format(self):
        return "CacheBO {zipUrl=%s, host=%s, varsionUrl=%s, dependencies=%s, snapshotTime=%s, cacheLevel=%s," \
               " firstLevelCacheMd5=%s, secondLevelCacheMd5=%s, threeLevelCacheMd5=%s}" % (
                   self.zip_url, self.host, self.version_url, self.dependencies, self.snapshot_time, self.cache_level,
                   self.first_level_cache_md5, self.second_level_cache_md5, self.three_level_cache_md5)
