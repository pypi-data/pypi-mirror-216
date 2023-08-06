#!/usr/bin/python3
# -*- coding:utf-8 -*-

class IParser:
    def read_components(self):
        """
        读取components.json文件信息
        :return:
        """
        pass

    def add_filter(self, fileters):
        """
        过滤器，将需要构建的轻应用组件封装到过滤器中
        :param fileters: 需要构建的轻应用组件
        :return:
        """
        pass

    def addParameter(self, param_map):
        """
        添加参数
        :param param_map:参数集合
        :return:
        """
        pass

    def parse(self, filter_json_array, components_json_array, variables_json):
        """
        过滤出需要构建的轻应用组件
        :param filter_json_array: 过滤器
        :param components_json_array:  需要过滤的内容
        :return:
        """
        pass
