#!/usr/bin/python3
# -*- coding:utf-8 -*-

from apf_ci.h5_grain.package_model import PackageModel
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger

class CreatePackageBuilder:
    def __init__(self, pages, dependencies):
        self.pages = pages
        self.dependencies = dependencies

    def perform(self, workspace_path):
        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")

        template_file_path = os.path.join(h5_grain_path, "packageTemplate.json")
        template_file_str = read_file_content(template_file_path)
        logger.info("[INFO] 正在读取packageTemplate.json文件内容")

        package_model = PackageModel()
        package_model.other = template_file_str
        package_model.pages = self.pages
        package_model.dependencies = self.dependencies

        package_file_path = os.path.join(workspace_path, "target/h5_grain/package.json")
        logger.info("[INFO] 正在创建package.json文件：%s" % package_file_path)

        logger.info("[INFO] 正在向package.json文件中写入内容...")
        write_content_to_file(package_file_path, package_model.tostring_format())
        return True
