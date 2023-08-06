#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from apf_ci.util.file_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class RouteToJson:

    def __init__(self):
        self.route_map = {}

    def perform(self):
        defines_file_path = os.path.join(os.getcwd(), "target", "defines.json")
        defines_data = read_file_content(defines_file_path)
        self.transform(defines_data)

    def transform(self, defines_data):
        """
        将 defines.json 文件中的路由信息写入 app/assets/app_factory/app/routes.json 文件中
        :param defines_data: defines.json 的文件内容
        :return:
        """
        if defines_data is None or defines_data == "":
            error_message = "【defines】文件没找到，结束route转换！！！"
            logger.error(LoggerErrorEnum.FILE_NOT_EXIST, error_message)
            return

        print("【INFO】defines =========>please check defines file: /ws/target/defines.json")
        biz_comp_xmls = self._init_biz_comp_map(defines_data)
        if not biz_comp_xmls:
            print("【ERROR】【 bizCompXmls 】为空！！！")
            return

        source_map = {}
        for comp_namespace_bizname in biz_comp_xmls:
            component = biz_comp_xmls[comp_namespace_bizname]
            component = json.loads(component)
            # routes数组
            routes = component["routes"]
            if len(routes) <= 0:
                continue
            i = 0
            for route in routes:
                source = route["_source"]
                new_str = comp_namespace_bizname.replace(":", ".")
                source = source.replace("${component_id}", new_str)
                destination = route["_destination"]
                destination = destination.replace("${component_id}", new_str)
                if source == "":
                    print("【INFO】【{0}】组件第【{1}】route source 值为空！".format(comp_namespace_bizname, (i + 1)))
                if destination == "":
                    print("【INFO】【{0}】组件第【{1}】route destination 值为空！".format(comp_namespace_bizname, (i + 1)))
                if source in source_map.keys():
                    print(
                        "【ERROR】【{0}】组件第【{1}】route source【{2}】已被包含在【{3}】组件中！！！".format(comp_namespace_bizname, (i + 1),
                                                                                       source, source_map[source]))
                source_map[source] = comp_namespace_bizname
                self.route_map[source] = destination
                i = i + 1
        path = os.path.join(os.getcwd(), "app", "assets", "app_factory", "app", "routes.json")
        print("【INFO】route.json 文件写入到【%s】" % path)
        self.write_route_json(path)

    def write_route_json(self, path):
        json_dumps = json.dumps(self.route_map)
        write_content_to_file(path, json_dumps)

    def _init_biz_comp_map(self, defines_data):
        biz_comp_map = {}
        print("【INFO】解析 defines 开始！！！")
        define_json_object = json.loads(defines_data)
        for defines_json_key in define_json_object:
            element = define_json_object[defines_json_key]
            namespace = element["namespace"]
            biz_name = element["biz_name"]
            bizcomp_key = namespace + ":" + biz_name
            biz_comp_map[bizcomp_key] = json.dumps(element)
        return biz_comp_map
