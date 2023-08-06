#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
应用工厂-构建H5颗粒插件
"""

import datetime
import json
import sys

from apf_ci.h5_grain.builder.analysis_pages_builder import AnalysisPagesBuilder
from apf_ci.h5_grain.builder.npm_operation_builder import NpmOperationBuilder
from apf_ci.h5_grain.builder.template_builder import TemplateBuilder
from apf_ci.util.content_service_config import ContentServiceConfig
from apf_ci.util.file_utils import *
from apf_ci.util.hook_service import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class H5GrainBuilder():
    def __init__(self, template_url, commit_id, build_command):
        self.template_url = template_url
        self.commit_id = commit_id
        self.build_command = build_command

    def perform(self, args):
        is_local = args.isLocal == "true"

        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, 'target')
        # 从variables.json文件中获取全局变量集合
        variables_path = os.path.join(target_path, 'variables.json')
        variables_data = read_file_content(variables_path)
        variables_dict = json.loads(variables_data)
        # 调用hook
        app_type = variables_dict["build_app_type"]
        gradle_home = variables_dict["gradleHome"]
        hook_service = HookService(app_type)
        hook_service.hook('pre_h5_grain', gradle_home, is_local)

        try:
            logger.info(" %s 开始H5 Grain构建" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            load_comps = os.getenv("loadComps", "")
            if load_comps:
                flag = False
                comps_str_arr = load_comps.split(",")
                for compstr in comps_str_arr:
                    ns_bn = compstr[:compstr.rfind(":")]
                    if ns_bn == "com.nd.apf.h5:widget":
                        flag = True
                if not flag:
                    logger.info("不需要进行H5颗粒构建")
                    return True

            env_target = variables_dict["envtarget"]
            factory_id = variables_dict["factoryId"]
            storage_host = variables_dict["app_native_storage"]

            # H5grain 从pages.json中筛选page、widget、npmdependency
            analysis_pages = AnalysisPagesBuilder(storage_host, factory_id)
            is_analysis_pages = analysis_pages.perform(workspace_path, variables_dict)
            if not is_analysis_pages:
                return False
            result_obj = variables_dict["resultObj"]
            logger.debug(" resultObj：%s" % result_obj)
            if result_obj != "EMPTY":
                template_builder = TemplateBuilder(storage_host, self.template_url, self.commit_id)
                is_template = template_builder.perform(workspace_path, variables_dict)
                if not is_template:
                    return False

                commands_url = variables_dict["h5_grain_commands_url"]

                # 配置内容服务，保存构建zip包及相关json文件
                cs_model = ContentServiceConfig()
                if env_target == "aws" or env_target == "aws-california":
                    lite_app_aws_json = variables_dict["liteAppAwsJson"]
                    logger.debug(" 解析aws json内容：%s" % lite_app_aws_json)
                    aws_cs_host = lite_app_aws_json.get("aws_cs_host", "")
                    aws_cs_server_name = lite_app_aws_json.get("aws_cs_server_name", "")
                    aws_cs_session_id = lite_app_aws_json.get("aws_cs_session_id", "")
                    aws_cs_user_id = lite_app_aws_json.get("aws_cs_user_id", "")

                    cs_model.host = aws_cs_host
                    cs_model.server_name = aws_cs_server_name
                    cs_model.session_id = aws_cs_session_id
                    cs_model.user_id = aws_cs_user_id
                    cs_model.access_key = lite_app_aws_json.get("access_key", "")
                    cs_model.secret_key = lite_app_aws_json.get("secret_key", "")
                else:
                    cs_model.host = variables_dict["h5_grain_cs_host"]
                    cs_model.server_name = variables_dict["h5_grain_cs_server_name"]
                    cs_model.session_id = variables_dict["h5_grain_cs_session_id"]
                    cs_model.user_id = variables_dict["h5_grain_cs_user_id"]
                    cs_model.access_key = variables_dict["h5_grain_cs_access_key"]
                    cs_model.secret_key = variables_dict["h5_grain_cs_secret_key"]
                    # 配置存储内容服务，保存皮肤和语言zip包
                storage_cs = ContentServiceConfig()
                storage_cs.host = variables_dict["h5_grain_storage_cs_host"]
                storage_cs.server_name = variables_dict["h5_grain_storage_cs_server_name"]
                storage_cs.session_id = variables_dict["h5_grain_storage_cs_session_id"]
                storage_cs.user_id = variables_dict["h5_grain_storage_cs_user_id"]
                storage_cs.access_key = variables_dict["h5_grain_storage_cs_access_key"]
                storage_cs.secret_key = variables_dict["h5_grain_storage_cs_secret_key"]

                close_cache = variables_dict["h5_grain_close_cache"] == "true"
                npm_operation = NpmOperationBuilder(close_cache, self.build_command, commands_url, cs_model, storage_cs)
                is_npm_operation = npm_operation.perform(variables_dict)
                if not is_npm_operation:
                    return False
        except Exception as e:
            error_message = 'h5 grain 构建失败: %s ' % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)
        return hook_service.hook('post_h5_grain', gradle_home, is_local)
