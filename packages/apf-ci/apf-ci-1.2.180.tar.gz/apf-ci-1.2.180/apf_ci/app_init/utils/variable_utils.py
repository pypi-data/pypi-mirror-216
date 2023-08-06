#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
target/variable.json 相关操作

"""
from apf_ci.app_init.utils.build_config_utils import *
from apf_ci.app_init.utils.language_utils import logger


class Variable:
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_path = os.path.join(target_path, 'variables.json')

    def get_service_host(self, build_config_json, service_name, envtarget):
        """
        获取service_host节点下对应服务对应环境的服务地址值，没有对应环境则采取默认default值
        :param build_config_json: build_config数据
        :param service_name: 服务名称
        :param envtarget: 环境
        :return:
        """
        service_host_data = build_config_json['service_host']
        try:
            return service_host_data[service_name][envtarget]
        except KeyError:
            return service_host_data[service_name]['default']


    def get_build_environment_name(self, build_config_json, envtarget):
        """
        获取app_factory_build_environment节点下对应环境的name值
        :param build_config_json:
        :param envtarget:
        :return:
        """
        app_factory_build_environment = build_config_json['app_factory_build_environment']
        for build_environment in app_factory_build_environment:
            config_envtarget = build_environment['envtarget']
            if config_envtarget == envtarget:
                return build_environment['name']


    def get_cs_offline_host(self, build_config_json, name):
        """
        获取app_factory_deploy_host节点下cs_offline_host对应name的值，无对应name值则采用default
        :param build_config_json:
        :param name: 环境名称
        :return:
        """
        app_factory_deploy_host = build_config_json['app_factory_deploy_host']
        cs_offline_host_json = app_factory_deploy_host['cs_offline_host']
        if name:
            return cs_offline_host_json[name]
        else:
            return cs_offline_host_json['default']


    def init_variable_json(self, variable_dict, build_config_json):
        """
        初始化全局变量参数--默认
        (如子应用和应用构建所需要的参数有差别，分步设置参数)
        :param variable_dict: 部分输入参数
        :return:
        """
        envtarget = variable_dict['envtarget']
        env_jenkins = variable_dict['envJenkins']
        is_local = variable_dict['is_local']
        #build_config_json = get_build_config(target_path)

        storage_host = self.get_service_host(build_config_json, 'app_native_storage', envtarget)
        validate_host = self.get_service_host(build_config_json, 'app_factory_validate', envtarget)
        biz_component_mng_host = self.get_service_host(build_config_json, 'biz_component_mng', envtarget)
        component_mng_host = self.get_service_host(build_config_json, "component_mng", envtarget)
        widget_i18n_store_host = self.get_service_host(build_config_json, "widget_i18n_store", envtarget)
        fac_resource_manage_host = self.get_service_host(build_config_json, 'fac_resource_manage', envtarget)
        #sign_cert_host = self.get_service_host(build_config_json, 'codesign', envtarget)
        # 证书服务升级
        sign_cert_host = self.get_service_host(build_config_json, 'certificate', envtarget)
        mobile_grey_host = self.get_service_host(build_config_json, 'mobile_grey', envtarget)
        app_datasource_host = self.get_service_host(build_config_json, 'app_datasource', envtarget)
        lifecycle_manage_host = self.get_service_host(build_config_json, 'lifecycle_manage', envtarget)
        widget_manage_host = self.get_service_host(build_config_json, 'widget_manage', envtarget)
        page_manage_host = self.get_service_host(build_config_json, 'page_manage', envtarget)
        sub_app_manage_host = self.get_service_host(build_config_json, 'sub_app_manage', envtarget)
        portal_web_domain_manage = self.get_service_host(build_config_json, 'portal_web_domain_manage', envtarget)
        factory_dependency_check = self.get_service_host(build_config_json, 'factory_dependency_check', envtarget)

        npm_registry = build_config_json['npm_registry']
        logger.debug(" npm_registry: %s" % npm_registry)
        if npm_registry is None:
            npm_registry = 'http://registry.npm.sdp.nd/'
        variable_dict['npm_registry'] = npm_registry

        logger.debug(" storage_host: %s" % storage_host)
        logger.debug(" validate_host: %s" % validate_host)
        logger.debug(" biz_component_mng_host: %s" % biz_component_mng_host)
        logger.debug(" component_mng_host: %s" % component_mng_host)
        logger.debug(" widget_i18n_store_host: %s" % widget_i18n_store_host)
        logger.debug(" fac_resource_manage_host: %s" % fac_resource_manage_host)
        logger.debug(" sign_cert_host: %s" % sign_cert_host)
        logger.debug(" mobile_grey_host: %s" % mobile_grey_host)
        logger.debug(" app_datasource_host: %s" % app_datasource_host)
        logger.debug(" lifecycle_manage_host: %s" % lifecycle_manage_host)
        logger.debug(" widget_manage_host: %s" % widget_manage_host)
        logger.debug(" page_manage_host: %s" % page_manage_host)
        logger.debug(" sub_app_manage_host: %s" % sub_app_manage_host)
        logger.debug(" portal_web_domain_manage: %s" % portal_web_domain_manage)
        logger.debug(" factory_dependency_check: %s" % factory_dependency_check)


        variable_dict['app_native_storage'] = storage_host
        variable_dict['app_factory_validate'] = validate_host
        variable_dict['biz_component_mng'] = biz_component_mng_host
        variable_dict['component_mng'] = component_mng_host
        variable_dict['widget_i18n_store'] = widget_i18n_store_host
        variable_dict['fac_resource_manage'] = fac_resource_manage_host
        variable_dict['codesign'] = sign_cert_host
        variable_dict['mobile_grey'] = mobile_grey_host
        variable_dict['app_datasource'] = app_datasource_host
        variable_dict['lifecycle_manage'] = lifecycle_manage_host
        variable_dict['widget_manage'] = widget_manage_host
        variable_dict['page_manage'] = page_manage_host
        variable_dict['sub_app_manage'] = sub_app_manage_host
        variable_dict['portal_web_domain_manage'] = portal_web_domain_manage
        variable_dict['factory_dependency_check'] = factory_dependency_check


        proxy_server_host = build_config_json['proxy_server_host']
        proxy_url = build_config_json['proxy_url']

        logger.debug(" proxy_server_host: %s" % proxy_server_host)
        logger.debug(" proxy_url: %s" % proxy_url)
        variable_dict['proxy_server_host'] = proxy_server_host
        variable_dict['proxy_url'] = proxy_url

        name = self.get_build_environment_name(build_config_json, envtarget)
        cs_offline_host = self.get_cs_offline_host(build_config_json, name)
        logger.debug(" cs_offline_host: %s" % cs_offline_host)
        variable_dict['cs_offline_host'] = cs_offline_host

        portal_host = envs_value('URL_PORTAL', env_jenkins, is_local)
        logger.debug(" portal_host: %s" % portal_host)
        variable_dict['app_protal'] = portal_host

        nowmillis = (int(round(time.time() * 1000)))
        variable_dict['lite_app_update_time'] = nowmillis

        version_code = (int((nowmillis - 1422720000402) / 60000)) + 600000
        logger.debug(" build_version_code: %s" % version_code)
        variable_dict['build_version_code'] = str(version_code)

        # 获取 apf-jenkins-config 下的 config_xxx.json内容。
        # 获取react轻应用-构建配置 缓存开关、发布内容服务用户名、发布内容服务地址、发布内容服务服务名、发布内容服务sessionid
        # 业务组件（react轻应用)-构建配置
        # 会被 脚本工具 不为空同名属性配置覆盖
        variable_dict["react_builder_close_cache"] = build_config_json["react_build_config"]["close_cache"]  # 是否关闭缓存构建
        # 内容服务配置
        variable_dict["react_builder_cs_user_id"] = build_config_json["react_build_config"][
            "react_cs_user_id"] # 发布内容服务用户名
        variable_dict["react_builder_cs_host"] = build_config_json["react_build_config"]["react_cs_host"] # 发布内容服务地址
        variable_dict["react_builder_cs_server_name"] = build_config_json["react_build_config"][
            "react_cs_server_name"] # 发布内容服务服务名
        variable_dict["react_builder_cs_session_id"] = build_config_json["react_build_config"][
            "react_cs_session_id"] # 发布内容服务sessionid
        variable_dict["react_builder_cs_access_key"] = build_config_json["react_build_config"][
            "access_key"] # 发布内容服务access_key
        variable_dict["react_builder_cs_secret_key"] = build_config_json["react_build_config"][
            "secret_key"] # 发布内容服务secret_key

        # 业务组件（React颗粒)-构建配置
        variable_dict["react_widget_builder_close_cache"] = build_config_json["react_widget_build_config"][
            "close_cache"] # 是否关闭缓存构建
        variable_dict["react_widget_builder_commands_url"] = build_config_json["react_widget_build_config"][
            "react_widget_build_commands_url"] # 构建命令模板地址
        # 内容服务配置
        variable_dict["react_widget_builder_cs_user_id"] = build_config_json["react_widget_build_config"][
            "react_widget_cs_user_id"] # 发布内容服务用户名
        variable_dict["react_widget_builder_cs_host"] = build_config_json["react_widget_build_config"][
            "react_widget_cs_host"] # 发布内容服务地址
        variable_dict["react_widget_builder_cs_server_name"] = build_config_json["react_widget_build_config"][
            "react_widget_cs_server_name"] # 发布内容服务服务名
        variable_dict["react_widget_builder_session_id"] = build_config_json["react_widget_build_config"][
            "react_widget_cs_session_id"] # 发布内容服务sessionid
        variable_dict["react_widget_builder_access_key"] = build_config_json["react_widget_build_config"][
            "access_key"] # 发布内容服务access_key
        variable_dict["react_widget_builder_secret_key"] = build_config_json["react_widget_build_config"][
            "secret_key"] # 发布内容服务secret_key


        # react颗粒默认资源构建 jenkins配置的全局变量
        variable_dict["rn_resource_commands_url"] = build_config_json["react_widget_resource"]["commands_url"]
        variable_dict["rn_resource_cs_user_id"] = build_config_json["react_widget_resource"]["cs_user_id"]
        variable_dict["rn_resource_cs_host"] = build_config_json["react_widget_resource"]["cs_host"]
        variable_dict["rn_resource_cs_server_name"] = build_config_json["react_widget_resource"]["cs_server_name"]
        variable_dict["rn_resource_cs_session_id"] = build_config_json["react_widget_resource"]["cs_session_id"]
        variable_dict["rn_resource_cs_access_key"] = build_config_json["react_widget_resource"]["access_key"]
        variable_dict["rn_resource_cs_secret_key"] = build_config_json["react_widget_resource"]["secret_key"]

        # H5颗粒默认资源构建 jenkins配置的全局变量
        variable_dict["h5_resource_commands_url"] = build_config_json["h5_widget_resource"]["commands_url"]
        variable_dict["h5_resource_cs_user_id"] = build_config_json["h5_widget_resource"]["cs_user_id"]
        variable_dict["h5_resource_cs_host"] = build_config_json["h5_widget_resource"]["cs_host"]
        variable_dict["h5_resource_cs_server_name"] = build_config_json["h5_widget_resource"]["cs_server_name"]
        variable_dict["h5_resource_cs_session_id"] = build_config_json["h5_widget_resource"]["cs_session_id"]
        variable_dict["h5_resource_cs_access_key"] = build_config_json["h5_widget_resource"]["access_key"]
        variable_dict["h5_resource_cs_secret_key"] = build_config_json["h5_widget_resource"]["secret_key"]

        # 业务组件（H5颗粒)-构建配置
        variable_dict["h5_grain_close_cache"] = build_config_json["h5_grain"]["close_cache"] # 是否关闭缓存构建
        variable_dict["h5_grain_commands_url"] = build_config_json["h5_grain"]["commands_url"] # 构建命令模板地址
        # 内容服务配置
        variable_dict["h5_grain_cs_user_id"] = build_config_json["h5_grain"]["cs_user_id"] # 发布内容服务用户名
        variable_dict["h5_grain_cs_host"] = build_config_json["h5_grain"]["cs_host"] # 发布内容服务地址
        variable_dict["h5_grain_cs_server_name"] = build_config_json["h5_grain"]["cs_server_name"] # 发布内容服务服务名
        variable_dict["h5_grain_cs_session_id"] = build_config_json["h5_grain"]["cs_session_id"] # 发布内容服务sessionid
        variable_dict["h5_grain_cs_access_key"] = build_config_json["h5_grain"]["access_key"] # 发布内容服务access_key
        variable_dict["h5_grain_cs_secret_key"] = build_config_json["h5_grain"]["secret_key"] # 发布内容服务secret_key
        # 存储内容服务配置
        variable_dict["h5_grain_storage_cs_user_id"] = build_config_json["h5_grain"]["storage_cs_user_id"] # 发布内容服务用户名
        variable_dict["h5_grain_storage_cs_host"] = build_config_json["h5_grain"]["storage_cs_host"] # 发布内容服务地址
        variable_dict["h5_grain_storage_cs_server_name"] = build_config_json["h5_grain"][
            "storage_cs_server_name"] # 发布内容服务服务名
        variable_dict["h5_grain_storage_cs_session_id"] = build_config_json["h5_grain"][
            "storage_cs_session_id"] # 发布内容服务sessionid
        variable_dict["h5_grain_storage_cs_access_key"] = build_config_json["h5_grain"][
            "storage_cs_access_key"] # 发布内容服务access_key
        variable_dict["h5_grain_storage_cs_secret_key"] = build_config_json["h5_grain"][
            "storage_cs_secret_key"] # 发布内容服务secret_key

        # android插件-构建配置
        variable_dict["android_plugin_build_close_cache"] = build_config_json["android_plugin_build_config"]["close_cache"] # 是否关闭缓存构建
        # 安卓构建前准备插件 - SDK路径
        variable_dict["sdk_path"] = build_config_json["android_build_prepare"]["sdk_path"]

        # 获取 ios构建前准备插件 的全局变量：模板替换字符串、默认identity
        variable_dict["replace_string"] = build_config_json["ios_build_prepare"]["replace_string"]
        variable_dict["default_identity"] = build_config_json["ios_build_prepare"]["default_identity"]

        variable_dict["local_h5_close_cache"] = build_config_json["local_h5"]["close_cache"]
        variable_dict["local_h5_cs_user_id"] = build_config_json["local_h5"]["cs_user_id"]
        variable_dict["local_h5_cs_host"] = build_config_json["local_h5"]["cs_host"  ]
        variable_dict["local_h5_cs_server_name"] = build_config_json["local_h5"]["cs_server_name"]
        variable_dict["local_h5_cs_session_id"] = build_config_json["local_h5"]["cs_session_id"]
        variable_dict["local_h5_cs_access_key"] = build_config_json["local_h5"]["access_key"]
        variable_dict["local_h5_cs_secret_key"] = build_config_json["local_h5"]["secret_key"]

        return variable_dict


    def write_variable_json(self, variable_dict):
        write_content_to_file(self.file_path, json.dumps(variable_dict, ensure_ascii=False))

    def read_variable_json(self):
        if os.path.exists(self.file_path):
            variable_data = read_file_content(self.file_path)
            return json.loads(variable_data)