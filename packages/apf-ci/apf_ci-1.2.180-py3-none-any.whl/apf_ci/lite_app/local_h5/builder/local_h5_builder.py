#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
应用工厂-构建离线H5轻应用插件
"""

from apf_ci.util.hook_service import *
from apf_ci.lite_app.concurrent.concurrent_build_client import *
from apf_ci.lite_app.parser.local_h5_parser import *
from apf_ci.lite_app.service.apf_service import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
import datetime

class LocalH5Builder:
    def __init__(self):
        pass

    def perform(self, args):
        is_local = args.isLocal == "true"

        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, 'target')
        # 从variables.json文件中获取全局变量集合
        variables_path = os.path.join(target_path, 'variables.json')
        variables_data = read_file_content(variables_path)
        variables_dict = json.loads(variables_data)

        app_type = variables_dict["build_app_type"]
        gradle_home = variables_dict["gradleHome"]
        hook_service = HookService(app_type)
        hook_service.hook('pre_local_h5', gradle_home, is_local)

        try:
            logger.info(" %s 开始离线H5构建" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            param_map = self.init_parameter(variables_dict)
            parser = LocalH5Parser()
            components_json_array = parser.read_components()
            filter_json_array = parser.add_filter(os.getenv("loadComps", ""))
            parser.addParameter(param_map)
            npm_dto_list = parser.parse(filter_json_array, components_json_array, variables_dict)

            local_h5_path = os.path.join(os.getcwd(), "target/local_h5")
            if not os.path.exists(local_h5_path):
                os.mkdir(local_h5_path)
                # 轻应用组件缓存数据整合
            concurrent_build_client = ConcurrentBuildClient()
            concurrent_build_client.npm_dto_list = npm_dto_list
            concurrent_build_client.start("h5")
            logger.info(" %s 离线H5构建结束" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            error_message = "local h5 构建失败: %s " % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)
        return hook_service.hook('post_local_h5', gradle_home, is_local)

    def init_parameter(self, variables_dict):
        param_map = {}
        apf_service = ApfService()

        close_cache = variables_dict["local_h5_close_cache"]
        logger.info(" 离线H5是否关闭缓存: %s" % close_cache)

        local_h5_cs_config = ContentServiceConfig()
        local_h5_cs_config.user_id = variables_dict["local_h5_cs_user_id"]
        local_h5_cs_config.host = variables_dict["local_h5_cs_host"]
        local_h5_cs_config.server_name = variables_dict["local_h5_cs_server_name"]
        local_h5_cs_config.session_id = variables_dict["local_h5_cs_session_id"]
        local_h5_cs_config.secret_key = variables_dict["local_h5_cs_secret_key"]
        local_h5_cs_config.access_key = variables_dict["local_h5_cs_access_key"]

        param_map["closeCache"] = close_cache
        param_map["csConfig"] = local_h5_cs_config
        param_map["lite_app_server"] = variables_dict["lite_app_server"]
        param_map["cs_offline_host"] = variables_dict["cs_offline_host"]
        param_map["build_app_type"] = variables_dict["build_app_type"]
        param_map["envtarget"] = variables_dict["envtarget"]
        param_map["build_app_name"] = variables_dict["build_app_name"]
        param_map["factoryId"] = variables_dict["factoryId"]
        param_map["build_app_version"] = variables_dict["build_app_version"]
        param_map["lite_app_update_time"] = variables_dict["lite_app_update_time"]
        param_map["build_package"] = variables_dict["build_package"]
        param_map["build_version_code"] = variables_dict["build_version_code"]
        param_map["app_language_array"] = variables_dict["app_language_array"]
        if "appVersionId" in os.environ.keys():
            app_version_id = os.environ["appVersionId"]
        else:
            app_version_id = variables_dict["build_version_label"].replace(" ", "").replace(":", "")
        param_map["appVersionId"] = app_version_id
        # 子应用
        factory_app_type = variables_dict["factoryAppType"]
        is_sub_app = apf_service.is_sub_app(factory_app_type)
        param_map["isSubApp"] = is_sub_app
        param_map["packageName"] = os.getenv("packageName")

        # 资源配置相关
        param_map["target_path"] = variables_dict["target_path"]
        param_map["fac_resource_manage"] = variables_dict["fac_resource_manage"]
        param_map["defaultLang"] = variables_dict["defaultLang"]
        param_map["env"] = variables_dict["env"]

        return param_map
