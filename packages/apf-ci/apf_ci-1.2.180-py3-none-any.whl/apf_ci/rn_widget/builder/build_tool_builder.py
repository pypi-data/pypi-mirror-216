#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import platform
import subprocess
from apf_ci.util.jenkins_utils import *
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger
from apf_ci.util.execute_command_utils import execute_command


class BuildToolbuilder:
    def __init__(self, page_id_list, plugin_component_id_dir):
        self.page_id_list = page_id_list
        self.plugin_component_id_dir = plugin_component_id_dir

    def perform(self, variables_json):
        self._execute_npm_build(self.plugin_component_id_dir, variables_json)
        self.zip_page_project(os.getcwd(), self.plugin_component_id_dir)
        return True

    def _execute_npm_build(self, plugin_component_id_dir, variables_json):
        workspace = os.getcwd()
        app_type = variables_json["build_app_type"]
        is_dev = variables_json["rn_debug_mode"]
        git_repository = variables_json["react_widget"]["git_repository"]
        commit_id = variables_json["react_widget"]["commit_id"]
        build_tool = variables_json["react_widget"]["build_tool"]
        npm_registry = variables_json["npm_registry"]

        sub_app = "false"
        factory_app_type = variables_json["factoryAppType"]
        if factory_app_type != "" and factory_app_type.lower() == "sub":
            sub_app = "true"

        reset_cache = self._last_time_build_result()
        logger.debug("[resetCache] %s" % reset_cache)

        react_widget_path = os.path.join(os.getcwd(), "target/react_widget")
        # 开始执行npm命令，window和linux命令格式不太一样
        platform_name = platform.system()
        if platform_name == 'Windows':
            logger.info(' npm config set registry=%s' % npm_registry)
            execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=react_widget_path)

            if app_type.lower() == "android":
                # 设置npm构建缓存地址到/tmp下
                logger.info(' npm config set unsafe-perm true')
                execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'], chdir=react_widget_path)

            logger.info(" npm install %s" % build_tool)
            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            execute_command(['npm', 'install', build_tool], chdir=react_widget_path)
        else:
            logger.info(' npm config set registry=%s' % npm_registry)
            execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=react_widget_path)

            if app_type.lower() == "android":
                # 设置npm构建缓存地址到/tmp下
                logger.info(' npm config set unsafe-perm true')
                execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'], chdir=react_widget_path)

            logger.info(" npm install %s" % build_tool)
            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            execute_command(['npm', 'install', build_tool], chdir=react_widget_path)

        react_widget_path_component_id_dir = os.path.join(react_widget_path, plugin_component_id_dir)
        logger.info(" react_widget_path_component_id_dir %s" % react_widget_path_component_id_dir)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.info(" node ./../node_modules/@sdp.nd/react-native-widget-builder/index.js --gitRepository %s"
                    " --commitId %s --platform %s --dev %s --reset-cache %s --pluginDir %s" % (
                git_repository, commit_id, app_type.lower(), is_dev, reset_cache, plugin_component_id_dir))
        js_name = "./../node_modules/@sdp.nd/react-native-widget-builder/index.js"
        execute_command(['node', js_name, "--gitRepository", git_repository,
                              "--commitId", commit_id, "--platform", app_type.lower(),
                              "--dev", is_dev, "--reset-cache", reset_cache,
                              "--pluginDir", plugin_component_id_dir], chdir=react_widget_path_component_id_dir)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(
            "node ./../node_modules/@sdp.nd/react-native-widget-builder/publish.js --platform %s --subApp %s --pluginDir %s" % (
                app_type.lower(), sub_app, plugin_component_id_dir))
        publish_js_name = "./../node_modules/@sdp.nd/react-native-widget-builder/publish.js"
        execute_command(['node', publish_js_name, '--platform', app_type.lower(),
                              '--subApp', sub_app, '--pluginDir', plugin_component_id_dir], chdir=react_widget_path_component_id_dir)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _last_time_build_result(self):
        # 使用Python获取jenkins的内置环境变量
        build_url = os.getenv("BUILD_URL")
        build_number = os.getenv("BUILD_NUMBER")
        job_name = os.getenv("JOB_NAME")
        logger.debug("build_number %s" % build_number)
        if build_number == "1":
            return "false"

        jenkins_url = build_url[0:build_url.find("/job/")]
        jenkins_url = jenkins_url + "/job/" + job_name + "/" + str(int(build_number) - 1) + "/consoleText"
        logger.debug(" jenkins_url : %s ,build_number:%s" % (jenkins_url, build_number))
        job_content = get_jenkins_job_console_text(jenkins_url)
        compare_str = "==============【ReactWidgetBuilder】步骤构建结果【成功】====="
        # 上一次成功返回false
        if compare_str in job_content:
            return "false"
        else:
            return "true"

    def zip_page_project(self, workspace, plugin_component_id_dir):
        """
        将page下脚本文件压缩成zip包
        :param workspace:
        :param plugin_component_id_dir:
        :return:
        """
        for page_id in self.page_id_list:
            input_file_name = os.path.join(workspace, "target/react_widget", plugin_component_id_dir, page_id)
            zip_file_name = input_file_name + ".zip"

            filter_list = []
            filter_list.append(".git")
            filter_list.append(".idea")
            filter_list.append("dist")
            filter_list.append("node_modules")

            zip_filter_folder_file(zip_file_name, input_file_name, True, filter_list)

