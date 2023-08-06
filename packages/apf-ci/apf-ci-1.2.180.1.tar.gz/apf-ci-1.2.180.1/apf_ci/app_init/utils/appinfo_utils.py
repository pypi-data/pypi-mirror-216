#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
"%s/v0.8/appinfo/%s" % (storage_host, factory_id)
target/app_info.json 相关操作

"""
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
import json


class AppInfo:
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_path = os.path.join(target_path, 'app_info.json')

    def get_app_info(self, storage_host, factory_id):
        """
        根据不同环境 下载 构建配置信息 并存储
        :return:
        """
        app_url = "%s/v0.8/appinfo/%s" % (storage_host, factory_id)
        app_json = get_data(app_url)
        return app_json

    def write_app_info(self, app_json):
        """
        写入 target/app_info.json
        :return:
        """
        write_content_to_file(self.file_path, json.dumps(app_json))

    def read_app_info(self):
        """
        读取 target/app_info.json
        :return:
        """
        if os.path.exists(self.file_path):
            build_config_data = read_file_content(self.file_path)
            return json.loads(build_config_data)

        return {}