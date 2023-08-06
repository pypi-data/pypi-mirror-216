#!/usr/bin/python3
# -*- coding: utf-8 -*-
import ast
import sys

from apf_ci.util.content_service_config import ContentServiceConfig
from apf_ci.util.http_utils import post_for_array
from apf_ci.util.upload_utils import upload_file_to_cs, get_cs_session
from apf_ci.lite_app.lite_enum.component_type_enum import *
from apf_ci.util.rsa_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class ApfService:
    def __init__(self):
        pass

    def get_content_service_config(self, host, server_name, session_id, userid):
        cs_config = ContentServiceConfig()
        cs_config.host = host
        cs_config.server_name = server_name
        cs_config.session_id = session_id
        cs_config.user_id = userid
        return cs_config

    def is_sub_app(self, factoryAppType):
        sub_app = "false"
        if factoryAppType != "" and factoryAppType == "sub":
            sub_app = "true"

        return sub_app

    def is_exist(self, local_cache_path):
        if os.path.exists(local_cache_path):
            return True
        else:
            return False

    def download_cache_from_cs(self, module_relative_path, zip_url, zip_file_name):
        """
        从CS上下载并解压缓存数据
        :param module_relative_path:
        :param zip_url:
        :param zip_file_name:
        :return:
        """
        workspace_path = os.getcwd()
        module_path = os.path.join(workspace_path, module_relative_path)
        zip_file_path = os.path.join(module_path, zip_file_name)
        logger.debug(" downloading file to: %s" % zip_file_path)
        try:
            download_cs_file(zip_url, zip_file_path, 3)
        except Exception:
            error_message = "下载zip包失败 %s" % zip_url
            logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, error_message)
            traceback.print_exc()
        logger.debug(" unzip file to: %s" % module_path)
        unzip(zip_file_path, module_path)

    def download_cache_from_local(self, module_relative_path, local_cache_path):
        """
        从本地获取缓存数据
        :param module_relative_path:
        :param local_cache_path:
        :return:
        """
        workspace_path = os.getcwd()
        module_path = os.path.join(workspace_path, module_relative_path)
        logger.debug(" unzip file to: %s" % module_path)
        unzip(local_cache_path, module_path)

    def get_nd_dependencies(self, module_relative_path):
        module_path = os.path.join(os.getcwd(), module_relative_path)
        nd_dependencies_file_path = os.path.join(module_path, "ndDependencies.version")
        if os.path.exists(nd_dependencies_file_path):
            return read_file_content(nd_dependencies_file_path)
        else:
            return "{}"

    def create_md5_file(self, module_path, module_dist_path):
        """
        计算文件路径MD5值，并保存生成md5.json文件
        :param module_path:
        :param module_dist_path:
        :return:
        """
        logger.debug("计算md5值路径 %s" % module_dist_path)
        md5_json = {}
        if os.path.isdir(module_dist_path):
            files = os.listdir(module_dist_path)
            for file in files:
                try:
                    file_abs_path = module_dist_path + "/" + file
                    upload_and_calc_md5(file_abs_path, md5_json, module_path)
                except Exception as e:
                    traceback.print_exc()
                    error_message ="【ERROR】计算md5出错 %s , module_dist_path=> %s, file=> %s" % (e, module_dist_path, file)
                    logger.error(LoggerErrorEnum.INVALID_ARGUMENT,error_message)
        md5_file_path = os.path.join(module_path, "md5.json")
        logger.debug("生成md5.json： %s" % md5_file_path)
        write_content_to_file(md5_file_path, json.dumps(md5_json))

    def create_version_file(self, module_path, zip_cs_path, npm_dto, cs_path):
        md5_file_path = os.path.join(module_path, "md5.json")
        md5_file_content = read_file_content(md5_file_path)
        md5_file_md5 = get_md5(md5_file_content)

        logger.debug(" RSA签名前数据为: %s" % md5_file_md5)
        md5_file_rsa = rsa_util_jar_encryptMd5(md5_file_md5)
        logger.debug(" RSA签名后数据为: %s" % md5_file_rsa)

        update_time = npm_dto.param_map.get("lite_app_update_time", "")

        version_obj = {}
        version_obj["namespace"] = npm_dto.namespace
        version_obj["bizName"] = npm_dto.biz_name
        version_obj["version"] = npm_dto.version
        version_obj["zip"] = zip_cs_path
        version_obj["md5FileRSA"] = md5_file_rsa
        version_obj["updateTime"] = update_time

        version_file_path = os.path.join(module_path, "version.json")
        logger.debug(" 生成version.json： %s" % version_file_path)
        file_in_content = json.dumps(version_obj)
        write_content_to_file(version_file_path, file_in_content)

        cs_config = npm_dto.param_map.get("csConfig")
        upload_file_to_cs(version_file_path, cs_path, "version.json", cs_config)

    def cs_offline_unzip(self, cs_path, cs_offline_host, unzip_package_file_name, cs_config):
        session = get_cs_session(cs_config)
        unzip_cs_path = cs_config.server_name + "/" + cs_path
        unzip_file_path = os.path.join(unzip_cs_path, unzip_package_file_name)

        request_body = {}
        request_body["dentry_id"] = ""
        # 待解压文件的目录项path
        request_body["file_path"] = unzip_file_path
        # 目标保存路径（必选
        request_body["parent_path"] = unzip_cs_path
        # 0-私密，1-公开，默认：0，可选
        request_body["scope"] = 1
        # 过期天数，0-永不过期，可选，默认：30 天
        request_body["expire_days"] = 0

        unzip_offline_post_url = cs_offline_host + "/v0.1/offline/unpack?session=" + session
        logger.info(" 离线解压zip包：%s " % unzip_offline_post_url)
        logger.debug(request_body)
        resp = requests.post(unzip_offline_post_url, json=json.loads(json.dumps(request_body)))
        logger.debug(resp)
        if resp.status_code != 200:
            error_message = "请求 %s 失败。status_code : %s" % (unzip_offline_post_url, resp.status_code)
            if resp.text:
                error_message += ' \n 失败原因：'+resp.text
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            sys.exit(1)


    def send_lite_app_data(self, npm_dto, cache_bo):
        logger.info(" 发送消息到轻应用服务上...")
        param_map = npm_dto.param_map
        app_type = param_map.get("build_app_type", "")
        lite_app_json = {
            "namespace": npm_dto.namespace,
            "biz_name": npm_dto.biz_name,
            "component_type": npm_dto.component_type,
            "version": npm_dto.version,
            "app_type": app_type.lower(),
            "update_time": param_map.get("lite_app_update_time", ""),
            "factory_id": param_map.get("factoryId", ""),
            "version_code": param_map.get("build_version_code", ""),
            "package_name": param_map.get("build_package", ""),
            "build_status": "SUCCESS"
        }

        snapshot_time = cache_bo.snapshot_time
        if snapshot_time != "":
            lite_app_json["snapshot_time"] = snapshot_time

        try:
            logger.debug(" cache_bo dependencies: %s type:%s" % (cache_bo.dependencies, type(cache_bo.dependencies)))
            if isinstance(cache_bo.dependencies, dict):
                dependencies_json = cache_bo.dependencies
            else:
                dependencies_json = json.loads(cache_bo.dependencies)
        except Exception as e:
            error_message = "dependencies转json错误"
            logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
            dependencies_json = {}
        lite_app_json["dependencies"] = self._get_sdks(dependencies_json)
        lite_app_json["three_level_cache_md5"] = cache_bo.three_level_cache_md5

        is_sub_app = param_map.get("isSubApp", "")

        # 获取variable.json
        variable_path = os.path.join(os.getcwd(), "target", "variables.json")
        variable_data = read_file_content(variable_path)
        variable_json = json.loads(variable_data)

        if is_sub_app == "true":
            sub_app_packagen_name = param_map.get("packageName", "")
            logger.debug(" 子应用包名: %s" % sub_app_packagen_name)
            lite_app_json["sub_app_package_name"] = sub_app_packagen_name
            zips_str = variable_json.get("zips", "")
            zips_json_array = None

            if zips_str == "":
                zips_json_array = []
            else:
                zips_json_array = ast.literal_eval(zips_str)
            zips_json_array.append(lite_app_json)

            variable_json["zips"] = str(zips_json_array)
            write_content_to_file(variable_path, json.dumps(variable_json, ensure_ascii=False))

        item_json = {
            "env": "test",
            "host": cache_bo.host,
            "zip_url": cache_bo.zip_url,
            "version_url": cache_bo.version_url,
            "npm": npm_dto.npm,
            "npm_version": npm_dto.js_version
        }
        items_json_array = []
        items_json_array.append(item_json)
        lite_app_json["items"] = items_json_array

        logger.debug(" npmDTO.getComponentType()： %s" % npm_dto.component_type)
        if npm_dto.component_type.lower() == ComponentTypeEnum.Android.value or npm_dto.component_type.lower() == ComponentTypeEnum.iOS.value:
            template_bo = param_map.get("templateBO", {})
            logger.debug(" TemplateBO.getDev()：%s" % template_bo.dev)
            lite_app_json["dev"] = template_bo.dev.lower() == str(True).lower()

        # 发布到轻应用服务上
        lite_app_host = param_map.get("lite_app_server", "")
        build_app_name = param_map.get("build_app_name", "")
        env_target = param_map.get("envtarget", "")
        build_app_version = param_map.get("build_app_version", "")
        app_version_id = param_map.get("appVersionId", "")

        lite_app_url_str = lite_app_host + "/v0.1/app/" + build_app_name + "/" + env_target + "/" + build_app_version \
                           + "/" + app_version_id
        post_for_array(lite_app_url_str, lite_app_json, True)

    def _get_sdks(self, sdks_json):
        data = {}
        for key, value in sdks_json.items():
            if isinstance(value, str):
                if value != "":
                    try:
                        # 走缓存情况，可能格式符合，不需要兼容
                        json.dumps(value)
                        value = json.loads(value)
                        data[key] = str(value)
                    except Exception as e:
                        value_json_object = {
                            "version": str(value)
                        }
                        data[key] = json.dumps(value_json_object)
            elif isinstance(value, dict):
                # 新版本格式
                value_json_object = value
                if "version" in value_json_object.keys():
                    if value_json_object["version"] != "":
                        data[key] = json.dumps(value_json_object)
        return data

