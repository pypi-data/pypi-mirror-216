#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import json

from apf_ci.util.file_utils import *
from apf_ci.util.jenkins_utils import envs_value
from apf_ci.config.defines import Defines

class PageAttributes(Defines):
    """
    通过过滤生成page_attributes.json文件
    """
    def __init__(self, env_jenkins, is_local, target_path):
        super().__init__(target_path)
        self.env_jenkins = env_jenkins
        self.is_local = is_local

    def __page_attributes_array(self):
        """
        从CS上获取文件内容，并保存到/target/page_attributes.json
        :return:返回去重后的文件内容数组（list格式）
        """
        page_attributes_url = envs_value('JENKINS_PAGE_ATTRIBUTES_URL', self.env_jenkins, self.is_local)
        page_attributes_data = read_cs_content(page_attributes_url)
        page_attributes_array = json.loads(page_attributes_data.decode('utf-8'))

        page_attributes_path = os.path.join(self.target_path, 'page_attributes.json')
        write_content_to_file(page_attributes_path, json.dumps(page_attributes_array))

        return list(set(page_attributes_array))

    def __filter_pages(self):
        """
        过滤出存在于/target/page_attributes.json中数据的defines.json文件内容
        :return: 返回过滤出的defines.json文件内容
        """
        content = {}

        page_attributes_array = self.__page_attributes_array()
        if page_attributes_array.__len__() > 0:
            defines_json = super().defines_json()
            for defines_key in defines_json:
                define_json = defines_json[defines_key]
                namespace = define_json['namespace']
                biz_name = define_json['biz_name']
                key = '%s.%s' % (namespace, biz_name)
                value = {}

                pages_json = define_json['pages']
                for pages_key in pages_json:
                    page_json = pages_json[pages_key]
                    if isinstance(page_json, dict):
                        new_page_json = {}

                        for page_key in page_json:
                            if page_key in page_attributes_array:
                                new_page_json[page_key] = page_json[page_key]

                        if new_page_json.__len__() > 0:
                            value[pages_key] = new_page_json

                if value.__len__() > 0:
                    content[key] = value

        return content

    def __save_page_attributes(self, app_factory_path, page_attributes_data):
        """
        保存数据到/app/assets/app_factory/app/page_attributes.json文件中
        :param app_factory_path: 将要保存的路径
        :param page_attributes_data: 将要保存的数据
        :return: 无
        """
        app_page_attributes_path = os.path.join(app_factory_path, 'app', 'page_attributes.json')
        write_content_to_file(app_page_attributes_path, json.dumps(page_attributes_data))

    def handle_page_attributes(self, app_factory_path):
        page_attributes_data = self.__filter_pages()
        self.__save_page_attributes(app_factory_path, page_attributes_data)

