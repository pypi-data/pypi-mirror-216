#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime
import platform

from apf_ci.constant.constants import Constants
from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class CreateResourceBuilder:

    def __init__(self, project_md5, env_target, build_command, commands_url, storage_host, factory_id, storage_cs):
        self.project_md5 = project_md5
        self.env_target = env_target
        self.build_command = build_command
        self.commands_url = commands_url
        self.storage_host = storage_host
        self.factory_id = factory_id
        self.storage_cs = storage_cs

    def perform(self, variables_json):
        logger.info(" 开始创建资源create_resource_builder")
        logger.debug(" projectMd5:%s, envTarget:%s, buildCommand:%s, commandsUrl:%s, storageHost:%s, factoryId:%s, storageCs:%s" % (
                self.project_md5, self.env_target, self.build_command, self.commands_url, self.storage_host,
                self.factory_id, self.storage_cs))
        workspace_path = os.getcwd()
        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")

        # 进行npm构建
        self.npm_build(h5_grain_path)

        languages_json = variables_json["languages"]
        all_languages_json = variables_json["allLanguages"]

        app_language_arr = self.get_app_language_array(languages_json, all_languages_json)
        logger.debug(" 【语言资源下载】应用语言【app_language_array】===》: %s" % app_language_arr)

        resource_service_host = variables_json[Constants.FAC_RESOUCE_MANAGE_HOST]
        skin_resource_id = self.get_skin_resource_id(resource_service_host)
        # skin_resource_id为空直接退出
        if not skin_resource_id:
            return False
        logger.debug(" 皮肤资源ID【skinResourceId】===》: %s" % skin_resource_id)

        self.create_resource(skin_resource_id, app_language_arr, workspace_path, variables_json)
        logger.info(" 结束创建资源create_resource_builder")
        return True

    def npm_build(self, path):
        if not self.build_command:
            try:
                logger.debug(" commandsUrl: %s" % self.commands_url)
                # 使用爬虫获取build_command.json的内容
                resp = requests.get(self.commands_url)
                command_list = resp.content.decode("utf-8").split('\n')

                for command in command_list:
                    line = command.replace('\r', '')
                    if line.startswith("widget="):
                        self.build_command = line[7:]
            except Exception as e:
                logger.warning(" 下载构建命令模板文件失败，设置为默认值npm run build")
                self.build_command = "npm run build"

        set_tmp_command = ['npm', 'config', 'set', 'tmp=%s' % path]
        logger.info(" 执行命令： %s" % set_tmp_command)
        execute_command(set_tmp_command, chdir=path)

        set_registry_command = ['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"']
        logger.info(" 执行命令： %s" % set_registry_command)
        execute_command(set_registry_command, chdir=path)

        build_command_split = self.build_command.split(" ")
        logger.info(" 执行命令： %s" % build_command_split)
        execute_command(build_command_split, chdir=path)

        npm_install_command = ['npm', 'install', '@sdp.nd/light-app-build']
        logger.info(" 安装构建工具： %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令： %s" % npm_install_command)
        execute_command(npm_install_command, chdir=path)

        platform_name = platform.system()
        if platform_name == 'Windows':
            nd_dependencies_command = ['node', 'node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.']
        else:
            nd_dependencies_command = ['node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.']
        logger.info(" 生成ndDependencies.version文件... %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令： %s" % nd_dependencies_command)
        execute_command(nd_dependencies_command, chdir=path)
        logger.info(" npm build 结束... %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def get_app_language_array(self, languages_json_arr, all_languages_json_arr):
        logger.debug(" 【语言资源下载】应用语言【languages】===》:%s" % languages_json_arr)

        app_language_map = {}
        for language in languages_json_arr:
            if isinstance(language, str):
                logger.debug("【语言资源下载】应用语言 ===》: 【String】:%s" % language)
                app_language_map[language] = language
        logger.debug(" 【语言资源下载】应用语言列表 ===》【allLanguagesJson】%s" % all_languages_json_arr)

        all_app_language_map = []
        for all_language in all_languages_json_arr:
            if not isinstance(all_language, dict):
                continue

            logger.debug(" 【语言资源下载】应用语言列表 ===》: 【obj.getString('name')】: %s" % all_language.get("name"))
            app_language_name = app_language_map.get(all_language.get("name"))
            if app_language_name:
                all_app_language_map.append(all_language)

        return all_app_language_map

    def get_skin_resource_id(self, resource_service_host):
        # http://fac-resouce-manage.oth.web.sdp.101.com/v0.1/resconfig/skin
        skin_resource_url = resource_service_host + "/v0.1/resconfig/skin"
        skin_resource_config_arr = get_data(skin_resource_url)
        if not skin_resource_config_arr:
            logger.warning("【error】皮肤资源类型未配置，请联系管理员进行配置管理！")
            return ""

        skin_resource_id = skin_resource_config_arr[0].get("id")
        return skin_resource_id

    def create_resource(self, skin_resource_id, app_language_arr, workspace_path, variables_json):
        cs_config = self.storage_cs
        # 配置存储内容服务，保存皮肤和语言zip包
        storage_cs_path = "/" + self.env_target + "/" + "com.nd.apf.h5" + "/" + "widget" + "/all"
        storage_cs_host_path = cs_config.host + "/static/" + cs_config.server_name + storage_cs_path

        current_time = str(int(round(time.time() * 1000)))
        skin_zip_file_name = "skin_" + current_time + ".zip"
        language_zip_file_name = "language_" + current_time + ".zip"

        skin_zip_cs_path = storage_cs_host_path + "/" + skin_zip_file_name
        skin_zip_cs_path = skin_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" skinZipCsPath: %s" % skin_zip_cs_path)
        language_zip_cs_path = storage_cs_host_path + "/" + language_zip_file_name
        language_zip_cs_path = language_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" languageZipCsPath: %s" % language_zip_cs_path)

        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")
        dist_path = os.path.join(h5_grain_path, "dist")
        if not os.path.exists(dist_path):
            error_message = '目录： %s 找不到'% dist_path
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            raise Exception(error_message)

        version_txt_file_path = os.path.join(workspace_path, "target/h5_grain/version.txt")
        logger.info(" 正在创建version.txt文件：%s" % version_txt_file_path)
        version_md5_str = self.project_md5
        write_content_to_file(version_txt_file_path, version_md5_str)

        # 压缩皮肤和语言zip包，并上传到存储CS内容服务上
        skin_path = os.path.join(dist_path, "style")
        language_path = os.path.join(dist_path, "i18n")
        skin_zip_file_path = os.path.join(h5_grain_path, skin_zip_file_name)
        language_zip_file_path = os.path.join(h5_grain_path, language_zip_file_name)

        skin_files_list = [skin_path, version_txt_file_path]
        language_files_list = [language_path, version_txt_file_path]

        try:
            zip_multi_file(skin_zip_file_path, skin_files_list, False)
            zip_multi_file(language_zip_file_path, language_files_list, False)
        except Exception as e:
            error_message = '皮肤和语言资源压缩有误 %s' % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            raise Exception(error_message)

        upload_file_to_cs(skin_zip_file_path, "/" + storage_cs_path, skin_zip_file_name,
                          cs_config)
        upload_file_to_cs(language_zip_file_path, "/" + storage_cs_path, language_zip_file_name,
                          cs_config)

        post_body = self.get_body_data(version_md5_str, workspace_path, skin_resource_id, app_language_arr,
                                       skin_zip_cs_path, language_zip_cs_path)
        url = self.storage_host + "/v0.8/widget_resources/apps/" + self.factory_id
        post_for_array(url, post_body)
        return True

    def get_body_data(self, version_md5_str, workspace_path, skin_resource_id, app_language_arr, skin_zip_cs_path,
                      language_zip_cs_path):
        skin_resource_arr = self.get_json_array(version_md5_str, skin_zip_cs_path)
        resource_json = {
            skin_resource_id: skin_resource_arr
        }
        for language_json in app_language_arr:
            if not isinstance(language_json, dict):
                continue
            resource_id = language_json.get("id")
            language_resource_arr = self.get_json_array(version_md5_str, language_zip_cs_path)
            resource_json[resource_id] = language_resource_arr
        obj = {
            "namespace": "com.nd.apf.h5",
            "biz_name": "widget",
            "version": "release",
            "resources": resource_json
        }
        return obj

    def get_json_array(self, version_content_md5, resource_url):
        resource_id_arr = []
        resource_id_json = {
            "os_type": "all",
            "component_type": "h5",
            "version": version_content_md5,
            "resource_url": resource_url
        }
        resource_id_arr.append(resource_id_json)
        return resource_id_arr
