#!/usr/bin/python3
# -*- coding: utf-8 -*-


class JsPackageCache:

    def __init__(self):
        self.package_name = ""
        self.version = ""
        self.publish_time = ""
        self.cache_md5 = ""
        self.cache_level = ""
        self.url = ""

    def tostring_format(self):
        return "JsPackageCache {packageName=%s, version=%s, publish_time=%s, cache_md5=%s, cache_level=%s, url=%s}" % (
            self.package_name, self.version, self.publish_time, self.cache_md5, self.cache_level, self.url)
