#!/usr/bin/python3
# -*- coding: utf-8 -*-

class CacheFactorBO:
    def __init__(self):
        self.js_package_name = ""
        self.js_version = ""
        self.js_publish_time = ""
        self.dev = ""
        self.js_template_commitid = ""
        self.js_build_tool = ""
        self.skin_file_md5 = ""
        self.i18n_file_md5 = ""
        self.build_file_md5 = ""
        self.pages_file_md5 = ""
        self.components_file_md5 = ""
        self.service_file_md5 = ""
        self.sub_app = ""
        self.app_type = ""

    def tostring_format(self):
        return "CacheFactoreBo {jsPackageName=%s, jsVersion=%s, jsPublishTime=%s, dev=%s, jsTemplateCommitId=%s, " \
               "jsBuildTool=%s, skinFileMd5=%s, i18nFileMd5=%s, buildFileMd5=%s, pagesFileMd5=%s, subApp=%s, " \
               "appType=%s, componentsFileMd5=%s, serviceFileMd5=%s}" % (
                   self.js_package_name, self.js_version, self.js_publish_time, self.dev, self.js_template_commitid,
                   self.js_build_tool,
                   self.skin_file_md5, self.i18n_file_md5, self.build_file_md5, self.pages_file_md5, self.sub_app,
                   self.app_type, self.components_file_md5, self.service_file_md5)
