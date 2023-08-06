#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.util.hook_service import HookService
from apf_ci.rn_widget.builder.analysis_pages_builder import *
from apf_ci.rn_widget.builder.templater_builder import *
from apf_ci.rn_widget.builder.npm_operation_builder import *
from apf_ci.util.content_service_config import *
from apf_ci.util.property import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
import datetime

class ReactWidgetBuilder:
    def __init__(self, template_url, template_commit_id, build_tool):
        self.template_url = template_url
        self.template_commit_id = template_commit_id
        self.build_tool = build_tool

    def perform(self, variables_json, is_local):
        logger.info(" %s 开始构建react颗粒" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        app_type = variables_json["build_app_type"]

        hook_service = HookService(app_type)
        app_type = variables_json['build_app_type']
        gradle_home = variables_json['gradleHome']
        hook_service.hook('pre_react_widget', gradle_home, is_local)

        load_comps = os.getenv("loadComps", "")
        load_comp_list = []
        if not self._check_rn(load_comps, load_comp_list):
            logger.info("不需要进行react颗粒构建")
            return True
        logger.debug(" loadCompList: %s" % load_comp_list)
        env_target = variables_json["envtarget"]
        factory_id = variables_json["factoryId"]
        storage_host = variables_json["app_native_storage"]
        lifecycle_host = variables_json["lifecycle_manage"]

        component_type = ""
        if app_type.lower() == "ios":
            component_type = "react-ios"
        elif app_type.lower() == "android":
            component_type = "react-android"

        logger.info(" %s  解析pages.json文件，并匹配widget。" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        analysis_pages_builder = AnalysisPagesBuilder(storage_host, lifecycle_host, factory_id, component_type,
                                                      load_comp_list)
        is_analysis_pages = analysis_pages_builder.perform(variables_json)
        if not is_analysis_pages:
            return False

        pages_result = variables_json["pagesResult"]
        logger.debug(" pagesResult： %s" % pages_result)
        if pages_result != "EMPTY":
            template_builder = TemplateBuilder(storage_host, self.template_url, self.template_commit_id,
                                               self.build_tool)
            is_templatde_builder = template_builder.perform(variables_json)
            if not is_templatde_builder:
                return False

            # 配置内容服务，保存构建zip包及相关json文件
            cs_config = ContentServiceConfig()
            cs_config.user_id = variables_json["react_widget_builder_cs_user_id"]
            cs_config.host = variables_json["react_widget_builder_cs_host"]
            cs_config.server_name = variables_json["react_widget_builder_cs_server_name"]
            cs_config.session_id = variables_json["react_widget_builder_session_id"]
            cs_config.access_key = variables_json["react_widget_builder_access_key"]
            cs_config.secret_key = variables_json["react_widget_builder_secret_key"]
            # 是否开启缓存 / 该值是用jenkins全局配置的 业务组件（React颗粒)-构建配置-缓存开关 控制
            close_cache = variables_json["react_widget_builder_close_cache"] == "true"
            logger.info("【是否关闭缓存构建】：%s" % close_cache)

            check_env_name_builder = CheckEnvNameBuilder(env_target)
            check_env_name_builder.perform(variables_json)

            # 遍历widget.json，取出每个widget对应的ModuleId。供后续下载颗粒语言资源使用。
            # 需求来源：redmine #9940 移动端：cmk
            multi_language_builder = MultiLanguageResourceBuilder()
            widget_module_json = multi_language_builder.get_widget_module_id_json(variables_json["app_language_array"])

            pages_result_json = json.loads(pages_result)
            # 遍历每个插件进行构建
            for pages_key in pages_result_json:
                each_pages_result_json = pages_result_json[pages_key]
                npm_operation_builder = NpmOperationBuilder(pages_key, each_pages_result_json, close_cache,
                                                            component_type, cs_config)
                result = npm_operation_builder.perform(variables_json, widget_module_json)
                if not result:
                    return False

            logger.info(" %s 将react=true/false键值对写入到local.properties文件中" % datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'))
            self._write_react(app_type)
        logger.info(" %s 构建react颗粒结束" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return hook_service.hook('post_react_widget', gradle_home, is_local)

    def _check_rn(self, load_comps, load_comp_list):
        if load_comps != "":
            flag = False

            coms_arr = load_comps.split(",")
            for comps_ele in coms_arr:
                ns_bn = comps_ele[:comps_ele.rfind(":")]
                if ns_bn.startswith("com.nd.sdp.plugin"):
                    flag = True
                    load_comp_list.append(comps_ele)
            return flag
        return True

    def _write_react(self, app_type):
        workspace_path = os.getcwd()
        if app_type.lower() == "android":
            # 将react=true/false键值对写入到local.properties文件中
            local_file_path = os.path.join(workspace_path, "local.properties")
            try:
                properties = Properties(local_file_path)
                properties.put("react", "true")
            except Exception as e:
                error_message = "向local.properties文件中写入react=true/false键值对信息异常 %s" % e
                logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
                traceback.print_exc()
                sys.exit(1)
