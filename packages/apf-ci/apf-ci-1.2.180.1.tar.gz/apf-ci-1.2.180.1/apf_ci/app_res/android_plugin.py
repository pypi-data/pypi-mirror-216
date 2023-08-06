#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
android_plugin.json文件内容处理业务
"""

__author__ = 'ZhouHuiTong'

from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *

class AndroidPlugin:
    existIos = True

    def __init__(self, target_path):
        self.target_path = target_path

    def android_json(self):
        """get components xml failure
        读取/target/android_plugin.json文件内容
        :return: 文件内容（dict格式）
        """
        android_json_path = os.path.join(self.target_path, 'android_plugin.json')
        android_json_data = read_file_content(android_json_path)
        return json.loads(android_json_data)

    def check_android_plugin(self,android_json ,file_name):
        """
        判断安卓插件是否存在
        :param file_name:
        :return:
        """
        if "plugin-setting" in android_json:
            # 判断产品启用了插件抡
            if android_json["plugin-setting"] == True:
                # 判断该安卓插件存在
                if file_name in android_json:
                    return True

        return False