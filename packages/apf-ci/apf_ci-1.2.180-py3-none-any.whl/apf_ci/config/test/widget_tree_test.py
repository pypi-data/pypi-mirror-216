#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import unittest

from apf_ci.config.widget_tree import WidgetTree
from apf_ci.util.file_utils import read_file_content


# 需要继承python自带的unittest
class WidegtTreeTest(unittest.TestCase):

    # test打头的方法会被识别为测试方法
    def test_create_tree(self):
        # 工作空间 切换到测试目录下
        os.chdir("F:\\temp")
        # 需要用存储服务给的widgets内容进行测试
        widgets_file_path = os.path.join(os.getcwd(), "widgets.json")
        widgets_file_json = json.loads(read_file_content(widgets_file_path));
        widgets_tree = WidgetTree()
        widgets_tree.create_tree(widgets_file_json)

    def test_set_module_properties_id(self):
        # 工作空间 切换到测试目录下
        os.chdir("F:\\temp")
        # 需要用存储服务给的widgets内容进行测试
        widgets_file_path = os.path.join(os.getcwd(), "widgets.json")
        widgets_file_json = json.loads(read_file_content(widgets_file_path));
        widgets_tree = WidgetTree()
        widgets_tree.create_tree(widgets_file_json)
        widgets_tree.set_module_properties_id()
