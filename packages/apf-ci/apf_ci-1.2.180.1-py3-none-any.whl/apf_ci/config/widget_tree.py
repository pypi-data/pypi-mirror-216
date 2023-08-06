#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import json
from apf_ci.util.log_utils import logger
class Node:
    def __init__(self):
        self.key = ''
        self.value = {}
        self.id = ''
        self.type = ''
        self.replacement = {}
        self.parent = None
        self.children = []

    def set_key(self, key):
        self.key = key

    def set_value(self, value):
        self.value = value

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type

    def set_replacement(self, replacement):
        self.replacement = replacement

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.children = children

    def __eq__(self, other):
        return self.id == other.id

class WidgetTree:
    def __init__(self):
        self.header = None
        self.widgets = {}

    def get_replacement(self):
        if self.header is None:
            return {}
        else:
            return self.header.replacement

    def remove_module(self, content):
        self.create_tree(content)
        # 在widget节点的 module_properties 增加 id 字段 对应redmine：#10202 需求方： cmk
        self.set_module_properties_id()
        self.remove_module_node()
        self.flush_relation()

        return self.convert_tree()

    def create_tree(self, content):
        for widget_key in content:
            widget_json = content[widget_key]
            template = widget_json['template']

            node = Node()
            node.set_key(template)
            node.set_value(widget_json)
            node.set_id(widget_key)

            try:
                type_value = widget_json['__type']
                node.set_type(type_value)
            except KeyError:
                pass

            self.widgets[template] = node

        for template_key in self.widgets:
            node = self.widgets[template_key]
            parent_key = node.value['__parent']

            if parent_key in self.widgets.keys():
                parent_node = self.widgets[parent_key]
                parent_node.children.append(node)
                node.set_parent(parent_node)

        self.header = Node()
        for template_key in self.widgets:
            node = self.widgets[template_key]
            if node.parent is None:
                node.set_parent(self.header)
                self.header.children.append(node)

    def remove_module_node(self):
        nodes = []
        nodes.append(self.header)

        index = 0
        while index < nodes.__len__():
            node = nodes[index]

            if node.type == 'modules':
                parent_node = node.parent
                if parent_node is not None:

                    for children_node in node.children:
                        # 将node的子节点添加到node的父节点里
                        '''Father - Me - Child 
                        => Father | - Me
                                  | - Child
                        '''
                        parent_node.children.append(children_node)

                        # node的template 是否在需要替换的字段里
                        if node.key in parent_node.replacement.values():
                            for replacement_key in parent_node.replacement:
                                if parent_node.replacement[replacement_key] == node.key:
                                    parent_node.replacement[replacement_key] = children_node.key
                                    break
                        else:
                            # 将node的template和child的template以K-V存成replacement
                            parent_node.replacement[node.key] = children_node.key
                    # parent节点的children移除node
                    parent_node.children.remove(node)
                    for children_node in node.children:
                        # 设置child node的父节点为parent
                        children_node.set_parent(parent_node)

                        if parent_node == self.header:
                            children_node.value['__parent'] = node.value['__parent']

            for children_node in node.children:
                nodes.append(children_node)

            index += 1

    def flush_relation(self):
        for template_key in self.widgets:
            node = self.widgets[template_key]
            widget_json = node.value

            if node.parent.key:
                widget_json['__parent'] = node.parent.key

            if 'properties' in widget_json.keys():
                properties_json = widget_json['properties']
                properties_str = json.dumps(properties_json)

                for replacement_key in node.replacement:
                    properties_str = properties_str.replace(replacement_key, node.replacement[replacement_key])

                widget_json['properties'] = json.loads(properties_str)

    def convert_tree(self):
        content = {}

        for template_key in self.widgets:
            node = self.widgets[template_key]

            if node.type != 'modules':
                content[node.id] = node.value

        return content

    def set_module_properties_id(self):
        """
        上一步会对存储给的widgets.json进行树的创建。结构大概如下：
        self.header : | module_leaf
                        |   widget_leaf
                            |   widget_leaf
                        |   widget_leaf
                      | module_leaf
                        |   widget_leaf
        :return:
        """
        logger.info("开始进行增加 module id到widget中")
        # 取根节点，进行遍历。
        root_widgets = self.header
        children_leaf = root_widgets.children
        self.__set_module_id_into_child_node(children_leaf)
        logger.info("进行增加 module id到widget结束")

    def __set_module_id_into_child_node(self, children_leaf):
        """
        递归遍历树的子节点，将module_id添加到每一个widgets节点的_module_properties中
        :param children_leaf: 子节点列表
        :return:
        """
        for child_node in children_leaf:
            # 若节点是 module 类型，则直接跳过
            if child_node.type == "widgets":
                # 若节点是 widget 类型，则寻找上一个节点的__module_id.
                # 取子节点的 原始数据
                child_node_value = child_node.value
                child_node_properties = child_node_value.get("properties")
                if not child_node_properties:
                    # 没有 properties 的话则跳过
                    continue
                child_node_module_properties = child_node_properties["_module_properties"]
                if not child_node_module_properties:
                    # 没有 _module_properties 的话则跳过
                    continue
                # 获取 module_id之前，需要取当前child节点父节点的module_id。
                parent_node = child_node.parent
                if not parent_node:
                    continue
                module_id = self.__get_module_id(parent_node)
                # 在子节点的 module_properties 中。添加 module_id
                child_node_module_properties["id"] = module_id

            # 子节点进行递归
            self.__set_module_id_into_child_node(child_node.children)

    def __get_module_id(self, parent_node):
        """
        获取父节点的module_id
        :param parent_node: 父节点
        :return: 返回module_id （字符串）
        """
        # 若父节点为module类型，则直接取父节点的id
        if parent_node.type == "modules":
            return parent_node.id
        elif parent_node.type == "widgets":
            # 若父节点为widgets类型，则需要获取 父节点 -> value -> properties -> _module_properties -> id
            parent_node_properties = parent_node.value.get("properties")
            if not parent_node_properties:
                logger.warning(" 父节点 type：widgets 类型的 properties 为空。父节点id为:%s" % parent_node.id)
                return ""
            parent_node_module_properties = parent_node_properties.get("_module_properties")
            if not parent_node_module_properties:
                logger.warning(" 父节点 type：widgets 类型的 _module_properties 为空。父节点id为:%s" % parent_node.id)
                return ""
            # 保证父节点的ID有值
            if "id" in parent_node_module_properties.keys():
                return parent_node_module_properties["id"]
            else:
                logger.warning(" 父节点 type：widgets 类型的 _module_properties 的 id 为空。父节点id为:%s" % parent_node.id)
                return ""

