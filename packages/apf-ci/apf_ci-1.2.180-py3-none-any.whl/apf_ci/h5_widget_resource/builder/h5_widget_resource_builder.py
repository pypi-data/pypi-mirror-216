#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import json

from apf_ci.constant.constants import Constants
from apf_ci.h5_widget_resource.builder.create_package_builder import CreatePackageBuilder
from apf_ci.h5_widget_resource.builder.create_resource_builder import CreateResourceBuilder
from apf_ci.h5_widget_resource.builder.ensure_template_builder import EnsureTemplateBuilder
from apf_ci.util.content_service_config import ContentServiceConfig
from apf_ci.util.file_utils import *
from apf_ci.util.md5_utils import get_md5
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger

class H5WidgetResourceBuilder:

    def __init__(self, template_url, template_commit_id, build_command):
        self.template_url = template_url
        self.template_commit_id = template_commit_id
        self.build_command = build_command

    def perform(self):
        workspace_path = os.getcwd()
        logger.info("开始构建生成H5颗粒默认资源。 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        variables_json_path = os.path.join(workspace_path, "target", "variables.json")
        variables_json_content = read_file_content(variables_json_path)
        variables_json = json.loads(variables_json_content)

        env_target = variables_json["envtarget"]
        logger.debug("envtarget： %s" % env_target)

        factory_id = variables_json["factoryId"]
        # app_native_storage
        storage_host = variables_json[Constants.APP_NATIVE_STORAGE_HOST]
        logger.debug("factoryId：%s" % factory_id)
        logger.debug("资源存储管理服务：%s" % storage_host)

        # 从git上下载模板
        logger.info("开始从git上下载模板 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ensure_builder = EnsureTemplateBuilder(storage_host, self.template_url, self.template_commit_id)
        flag = ensure_builder.perform(variables_json)
        if not flag:
            error_message = '从git上下载模板失败。结束构建'
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            raise Exception(error_message)

        # 生成package.json文件
        logger.info("开始封装package.json文件 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        create_package = CreatePackageBuilder(storage_host, factory_id)
        is_create = create_package.perform(variables_json)
        if not is_create:
            error_message = '没有生成package.json文件，不需要构建H5颗粒资源'
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            return False

        git_commit_id = variables_json["git_commitid"]
        result_json = variables_json["resultObj"]

        pages = json.dumps(result_json.get("pages"))
        npm_dependencies = result_json.get("npmDependencies")

        project = git_commit_id + npm_dependencies + pages
        project_md5 = get_md5(project)
        logger.debug("project=【%s】" % project)
        logger.debug("projectMd5=【%s】" % project_md5)

        commands_url = variables_json["h5_resource_commands_url"]

        cs_config = ContentServiceConfig()
        cs_config.host = variables_json["h5_resource_cs_host"]
        cs_config.server_name = variables_json["h5_resource_cs_server_name"]
        cs_config.session_id = variables_json["h5_resource_cs_session_id"]
        cs_config.user_id = variables_json["h5_resource_cs_user_id"]
        cs_config.access_key = variables_json["h5_resource_cs_access_key"]
        cs_config.secret_key = variables_json["h5_resource_cs_secret_key"]
        logger.debug("创建CS配置对象: host:%s, server_name: %s, session_id: %s, user_id: %s" % (
            cs_config.host, cs_config.server_name, cs_config.session_id, cs_config.user_id))

        create_resource_builder = CreateResourceBuilder(project_md5, env_target, self.build_command, commands_url,
                                                        storage_host, factory_id, cs_config)
        is_create_resource = create_resource_builder.perform(variables_json)
        if not is_create_resource:
            return False

        logger.info("%s 构建生成H5颗粒默认资源结束" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        variables_json["build_desc"] = "默认资源构建成功"
        write_content_to_file(variables_json_path, json.dumps(variables_json, ensure_ascii=False))
        return True