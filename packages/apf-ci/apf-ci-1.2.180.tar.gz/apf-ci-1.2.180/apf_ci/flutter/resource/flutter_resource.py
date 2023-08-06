#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = '961111'

from abc import ABCMeta, abstractmethod

from apf_ci.util.file_utils import *


class FlutterResource(metaclass=ABCMeta):

    def __init__(self, flutter_template_path, target_path, flutter_component_dependency):
        self.flutter_template_path = flutter_template_path
        self.target_path = target_path
        self.flutter_component_dependency = flutter_component_dependency
        self.md5_buffer = ''

    def get_file_md5(self, file_path):
        """
        通过文件路径获取文件MD5值，若文件不存在，则对空值进行MD5加密
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_content = f.read()
            return get_md5(file_content)
        else:
            return get_md5("")

    def unzip_file_with_path(self, file_zip, file, unzip_path):
        """
        解压文件
        :param file_zip:
        :param file:
        :param unzip_path:
        :return:
        """
        # 这里多线程操作，extract内有创建目录操作，偶发会同时创建一个目录，暂无合适解决方案，捕获后再创建一次
        # 报错 FileExistsError: [Errno 17] File exists
        try:
            file_zip.extract(file, unzip_path)
        except Exception as e:
            logger.warning('file_zip.extract file: %s , unzip_path: %s' % (file, unzip_path))
            logger.warning(e)
            file_zip.extract(file, unzip_path)

    @abstractmethod
    def load(self):
        """
        构建
        :return:
        """
        pass
