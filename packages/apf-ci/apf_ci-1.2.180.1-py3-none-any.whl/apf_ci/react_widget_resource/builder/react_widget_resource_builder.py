#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
react颗粒默认资源构建插件 - 入口
"""

import datetime
import json

from apf_ci.react_widget_resource.builder.create_resource_builder import CreateResourceBuilder
from apf_ci.rn_widget.model.page import Page

from apf_ci.react_widget_resource.builder.npm_builder import NpmBuilder
from apf_ci.react_widget_resource.builder.ensure_template_builder import EnsureTemplateBuilder
from apf_ci.react_widget_resource.builder.rn_resource_analysis_pages_builder import RnResourceAnalysisPages
from apf_ci.constant.path_constant import PathConstant
from apf_ci.constant.constants import Constants
from apf_ci.util.content_service_config import *
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger


class ReactWidgetResourceBuilder:
    def __init__(self, template_url, template_commit_id, build_tool):
        self.template_url = template_url
        self.template_commit_id = template_commit_id
        self.build_tool = build_tool

    def perform(self):
        workspace_path = os.getcwd()
        logger.info(" 开始构建生成react颗粒默认资源。 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        variables_json_path = os.path.join(workspace_path, "target", "variables.json")
        variables_json_content = read_file_content(variables_json_path)
        variables_json = json.loads(variables_json_content)

        app_type = variables_json["build_app_type"]
        logger.debug(" 构建类型build_app_type： %s" % app_type)

        load_comps = os.getenv("loadComps", "")
        logger.debug(" loadComps: %s" % load_comps)

        load_comp_list = []
        if not self.__check_rn(load_comps, load_comp_list):
            logger.info(" 不需要进行react颗粒构建")
            return True
        logger.debug(" loadCompList：%s" % load_comp_list)

        env_target = variables_json["envtarget"]
        logger.debug(" envtarget： %s" % env_target)

        factory_id = variables_json["factoryId"]
        # app_native_storage
        storage_host = variables_json[Constants.APP_NATIVE_STORAGE_HOST]
        # widget_manage
        widget_host = variables_json[Constants.WIDGET_MANAGE_HOST]
        logger.debug(" factoryId：%s" % factory_id)
        logger.debug(" 资源存储管理服务：%s" % storage_host)
        logger.debug(" widget管理服务： %s" % widget_host)
        # lifecycle_manage
        lifecycle_host = variables_json[Constants.LIFECYCLE_MANAGE_HOST]
        logger.debug(" 生命周期管理服务: %s" % lifecycle_host)

        component_type = ""
        if app_type.lower() == "ios":
            component_type = "react-ios"
        elif app_type.lower() == "android":
            component_type = "react-android"

        logger.info(" 解析pages.json文件，并匹配widget. %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        analysis_pages = RnResourceAnalysisPages(storage_host, lifecycle_host, factory_id, component_type,
                                                 load_comp_list)
        is_analysis_pages = analysis_pages.perform(variables_json)
        if not is_analysis_pages:
            return False

        pages_result = variables_json["pagesResult"]
        logger.debug(" pagesResult：%s" % pages_result)
        if pages_result == "EMPTY":
            logger.info(" pagesResult为空，结束默认颗粒资源构建.")

        ensure_template = EnsureTemplateBuilder(storage_host, self.template_url, self.template_commit_id,
                                                self.build_tool)
        ensure_template.perform(variables_json)

        # 配置内容服务，保存构建zip包及相关json文件
        cs_config = ContentServiceConfig()
        if env_target.lower() == "aws" or env_target.lower() == "aws-california":
            lite_app_aws_json = variables_json["liteAppAwsJson"]
            logger.debug(" 解析aws json内容：%s" % lite_app_aws_json)
            aws_cs_host = lite_app_aws_json.get("aws_cs_host")
            aws_cs_server_name = lite_app_aws_json.get("aws_cs_server_name")
            aws_cs_session_id = lite_app_aws_json.get("aws_cs_session_id")
            aws_cs_user_id = lite_app_aws_json.get("aws_cs_user_id")

            cs_config.host = aws_cs_host
            cs_config.server_name = aws_cs_server_name
            cs_config.session_id = aws_cs_session_id
            cs_config.user_id = aws_cs_user_id
            cs_config.access_key = lite_app_aws_json.get("access_key")
            cs_config.secret_key = lite_app_aws_json.get("secret_key")
        else:
            cs_config.host = variables_json["rn_resource_cs_host"]
            cs_config.server_name = variables_json["rn_resource_cs_server_name"]
            cs_config.session_id = variables_json["rn_resource_cs_session_id"]
            cs_config.user_id = variables_json["rn_resource_cs_user_id"]
            cs_config.access_key = variables_json["rn_resource_cs_access_key"]
            cs_config.secret_key = variables_json["rn_resource_cs_secret_key"]
        logger.debug(" CsConfig配置为：【host】%s 【serverName】%s 【sessionId】%s 【userId】%s" % (
        cs_config.host, cs_config.server_name, cs_config.session_id, cs_config.user_id))

        pages_result_json = json.loads(pages_result)
        for plugin_id_dir in pages_result_json:
            each_plugin_json_object = pages_result_json[plugin_id_dir]
            pages_json_arr = each_plugin_json_object.get("pages")
            # 将pages_json_arr转换成Page对象列表
            pages_object_list = self.__pages_arr_parse_pages_object_list(pages_json_arr)
            npm_dependencies = each_plugin_json_object.get("npmDependencies")

            # 执行构建
            for page in pages_object_list:
                page_id_list = []
                page_id_list.append(page.id)

                npm_dependencies_json = npm_dependencies.get(page.id, {})
                npm_builder = NpmBuilder(page, npm_dependencies_json, plugin_id_dir)
                npm_builder.perform(variables_json)

                create_resource = CreateResourceBuilder(page_id_list, env_target, factory_id, storage_host, widget_host, plugin_id_dir, cs_config)
                is_npm_operation = create_resource.perform(variables_json)
                if not is_npm_operation:
                    return False
        logger.info(" %s 构建生成react颗粒默认资源结束" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        variables_json["build_desc"] = "默认资源构建成功"
        write_content_to_file(variables_json_path, json.dumps(variables_json, ensure_ascii=False))
        return True

    def __check_rn(self, load_comps, load_comp_list):
        if load_comps:
            flag = False

            comps_arr = load_comps.split(".")
            for comps in comps_arr:
                ns_bn = comps[0: comps.rfind(":")]
                # 若是以 com.nd.sdp.plugin 开头的
                if ns_bn.startswith(PathConstant.PLUGIN_WIDGET_NAMESPACE):
                    flag = True
                    load_comp_list.append(comps)
            return flag
        return True

    def __pages_arr_parse_pages_object_list(self, pages_json_arr):
        pages_object_list = []
        for pages_json in pages_json_arr:
            page = Page()
            page.id = pages_json.get("id", "")
            page.path = pages_json.get("path", "")
            page.uri = pages_json.get("uri", "")
            page.widgets = pages_json.get("widgets", [])
            page.pluginKey = pages_json.get("pluginKey", "")
            pages_object_list.append(page)
        return pages_object_list
