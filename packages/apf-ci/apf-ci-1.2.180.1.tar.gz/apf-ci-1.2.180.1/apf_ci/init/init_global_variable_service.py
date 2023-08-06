#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Initializing global variables
"""

__author__ = 'LianGuoQing'

import os
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.jenkins_utils import envs_value
from apf_ci.config.defines import Defines
from apf_ci.app_init.utils.build_config_utils import BuildConfig


class InitGlobalVariableService:
    def __init__(self, target_path, env_jenkins, is_local):
        self.target_path = target_path
        self.env_jenkins = env_jenkins
        self.is_local = is_local


    def get_service_host(self, build_config_data, service_name, envtarget):
        """
        获取service_host节点下对应服务对应环境的服务地址值，没有对应环境则采取默认default值
        :param build_config_data: build_config数据
        :param service_name: 服务名称
        :param envtarget: 环境
        :return:
        """
        service_host_data = build_config_data['service_host']
        try:
            return service_host_data[service_name][envtarget]
        except KeyError:
            return service_host_data[service_name]['default']

    def get_build_environment_name(self, build_config_data, envtarget):
        """
        获取app_factory_build_environment节点下对应环境的name值
        :param build_config_data:
        :param envtarget:
        :return:
        """
        app_factory_build_environment = build_config_data['app_factory_build_environment']
        for build_environment in app_factory_build_environment:
            config_envtarget = build_environment['envtarget']
            if config_envtarget == envtarget:
                return build_environment['name']

    def get_cs_offline_host(self, build_config_data, name):
        """
        获取app_factory_deploy_host节点下cs_offline_host对应name的值，无对应name值则采用default
        :param build_config_data:
        :param name: 环境名称
        :return:
        """
        app_factory_deploy_host = build_config_data['app_factory_deploy_host']
        cs_offline_host_json = app_factory_deploy_host['cs_offline_host']
        if name:
            return cs_offline_host_json[name]
        else:
            return cs_offline_host_json['default']

    def read_build_config(self):
        build_config = BuildConfig(self.target_path)
        build_config_json_encrypt = build_config.get_build_config(self.env_jenkins,
                                                                  self.is_local)
        return build_config.decrypy_build_config(build_config_json_encrypt)

    def initGlobalVariable_sub(self, factory_id, envtarget, app_type, version_id):
        """
        初始化全局变量参数--子应用
        (子应用和应用构建所需要的参数有差别，分步设置参数)
        :param factory_id:
        :param envtarget:
        :param app_type:
        :param version_id:
        :return:
        """
        variable_dict = {}
        variable_dict['factoryId'] = factory_id
        variable_dict['build_app_type'] = app_type
        variable_dict['versionId'] = version_id
        variable_dict['envJenkins'] = self.env_jenkins

        build_config_data = self.read_build_config()

        storage_host = self.get_service_host(build_config_data, 'app_native_storage', envtarget)
        validate_host = self.get_service_host(build_config_data, 'app_factory_validate', envtarget)
        biz_component_mng_host = self.get_service_host(build_config_data, 'biz_component_mng', envtarget)
        fac_resource_manage_host = self.get_service_host(build_config_data, 'fac_resource_manage', envtarget)
        #sign_cert_host = self.get_service_host(build_config_data, 'codesign', envtarget)
        sign_cert_host = self.get_service_host(build_config_data, 'certificate', envtarget)
        mobile_grey_host = self.get_service_host(build_config_data, 'mobile_grey', envtarget)
        app_datasource_host = self.get_service_host(build_config_data, 'app_datasource', envtarget)
        lifecycle_manage_host = self.get_service_host(build_config_data, 'lifecycle_manage', envtarget)
        widget_manage_host = self.get_service_host(build_config_data, 'widget_manage', envtarget)
        page_manage_host = self.get_service_host(build_config_data, 'page_manage', envtarget)
        sub_app_manage_host = self.get_service_host(build_config_data, 'sub_app_manage', envtarget)
        component_mng = self.get_service_host(build_config_data, 'component_mng', envtarget)
        widget_i18n_store = self.get_service_host(build_config_data, 'widget_i18n_store', envtarget)

        npm_registry =build_config_data['npm_registry']
        logger.debug("npm_registry: %s" % npm_registry)
        if npm_registry is None:
            npm_registry = 'http://registry.npm.sdp.nd/'
        variable_dict['npm_registry'] = npm_registry

        logger.debug("storage_host: %s" % storage_host)
        logger.debug("validate_host: %s" % validate_host)
        logger.debug("biz_component_mng_host: %s" % biz_component_mng_host)
        logger.debug("fac_resource_manage_host: %s" % fac_resource_manage_host)
        logger.debug("sign_cert_host: %s" % sign_cert_host)
        logger.debug("mobile_grey_host: %s" % mobile_grey_host)
        logger.debug("app_datasource_host: %s" % app_datasource_host)
        logger.debug("lifecycle_manage_host: %s" % lifecycle_manage_host)
        logger.debug("widget_manage_host: %s" % widget_manage_host)
        logger.debug("page_manage_host: %s" % page_manage_host)
        logger.debug("sub_app_manage_host: %s" % sub_app_manage_host)
        logger.debug("component_mng: %s" % component_mng)
        logger.debug("widget_i18n_store: %s" % widget_i18n_store)

        variable_dict['app_native_storage'] = storage_host
        variable_dict['app_factory_validate'] = validate_host
        variable_dict['biz_component_mng'] = biz_component_mng_host
        variable_dict['fac_resource_manage'] = fac_resource_manage_host
        variable_dict['codesign'] = sign_cert_host
        variable_dict['mobile_grey'] = mobile_grey_host
        variable_dict['app_datasource'] = app_datasource_host
        variable_dict['lifecycle_manage'] = lifecycle_manage_host
        variable_dict['widget_manage'] = widget_manage_host
        variable_dict['page_manage'] = page_manage_host
        variable_dict['sub_app_manage'] = sub_app_manage_host
        variable_dict['component_mng'] = component_mng
        variable_dict['widget_i18n_store'] = widget_i18n_store

        proxy_server_host = build_config_data['proxy_server_host']
        proxy_url = build_config_data['proxy_url']

        logger.debug("proxy_server_host: %s" % proxy_server_host)
        logger.debug("proxy_url: %s" % proxy_url)
        variable_dict['proxy_server_host'] = proxy_server_host
        variable_dict['proxy_url'] = proxy_url

        name = self.get_build_environment_name(build_config_data, envtarget)
        cs_offline_host = self.get_cs_offline_host(build_config_data, name)
        logger.debug("cs_offline_host: %s" % cs_offline_host)
        variable_dict['cs_offline_host'] = cs_offline_host

        portal_host = envs_value('URL_PORTAL', self.env_jenkins, self.is_local)
        logger.debug("portal_host: %s" % portal_host)
        variable_dict['app_protal'] = portal_host

        build_config_json = build_config_data
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
        return variable_dict


    def initGlobalVariable(self, factory_id, envtarget, app_type, version_id, version2_app_factory):
        """
        初始化全局变量参数--应用
        :param factory_id:
        :param envtarget:
        :param app_type:
        :param version_id:
        :param version2_app_factory:
        :return:
        """
        variable_dict = self.initGlobalVariable_sub(factory_id, envtarget, app_type, version_id)
        variable_dict['version2AppFactory'] = version2_app_factory
        build_config_data = self.read_build_config()
        storage_host = variable_dict['app_native_storage']
        portal_host = variable_dict['app_protal']

        force = envs_value('force', self.env_jenkins, self.is_local)
        logger.debug("force: %s" % force)

        version_info = envs_value('versionInfo', self.env_jenkins, self.is_local)
        logger.debug("versionInfo: %s" % version_info)

        nowmillis = (int(round(time.time() * 1000)))
        variable_dict['lite_app_update_time'] = nowmillis

        version_code = (int((nowmillis - 1422720000402) / 60000)) + 600000
        logger.debug("build_version_code: %s" % version_code)
        variable_dict['build_version_code'] = str(version_code)

        # 获取 apf-jenkins-config 下的 config_xxx.json内容。
        build_config_json = build_config_data
        # 获取react轻应用-构建配置 缓存开关、发布内容服务用户名、发布内容服务地址、发布内容服务服务名、发布内容服务sessionid
        # 业务组件（react轻应用)-构建配置
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

        # 安卓构建前准备插件 - SDK路径
        variable_dict["sdk_path"] = build_config_json["android_build_prepare"]["sdk_path"]

        # 获取 ios构建前准备插件 的全局变量：模板替换字符串、默认identity
        variable_dict["replace_string"] = build_config_json["ios_build_prepare"]["replace_string"]
        variable_dict["default_identity"] = build_config_json["ios_build_prepare"]["default_identity"]

        variable_dict["local_h5_close_cache"] = build_config_json["local_h5"]["close_cache"]
        variable_dict["local_h5_cs_user_id"] = build_config_json["local_h5"]["cs_user_id"]
        variable_dict["local_h5_cs_host"] = build_config_json["local_h5"]["cs_host"]
        variable_dict["local_h5_cs_server_name"] = build_config_json["local_h5"]["cs_server_name"]
        variable_dict["local_h5_cs_session_id"] = build_config_json["local_h5"]["cs_session_id"]
        variable_dict["local_h5_cs_access_key"] = build_config_json["local_h5"]["access_key"]
        variable_dict["local_h5_cs_secret_key"] = build_config_json["local_h5"]["secret_key"]
        result_json = {}
        PACKAGE_NAME_ANDROID = ''
        PACKAGE_NAME_IOS = ''
        CHINESE_NAME = ''
        VERSION_NAME = ''
        VERSION_DESC = ''
        APP_NAME = ''

        if version_info:
            result_json = json.loads(version_info)

            PACKAGE_NAME_ANDROID = 'package_name_android'
            PACKAGE_NAME_IOS = 'package_name_ios'
            CHINESE_NAME = 'chinese_name'
            VERSION_NAME = 'version_name'
            VERSION_DESC = 'version_desc'
            APP_NAME = 'app_name'
        else:
            if version_id:
                portal_info_url = "%s/third/info/%s" % (portal_host, version_id)
                if version2_app_factory:
                    portal_info_url = version2_app_factory + version_id

                result_json = get_data(portal_info_url)

                try:
                    logger.warning("[ERROR] %s " % result_json['message'])
                    raise Exception()
                    sys.exit(1)
                except KeyError:
                    pass
            else:
                result_json = ''

            PACKAGE_NAME_ANDROID = 'packageName'
            PACKAGE_NAME_IOS = 'packageNameIOS'
            CHINESE_NAME = 'chineseName'
            VERSION_NAME = 'versionName'
            VERSION_DESC = 'versionDesc'
            APP_NAME = 'appName'

        com_test_type = ''
        build_type = ''

        if result_json:
            app_json = result_json['app']

            type_value = ''
            try:
                type_value = app_json['type']
            except KeyError:
                pass

            logger.debug("app type: %s (11--biz_component_fun_test, 12--biz_component_com_test)" % type_value)

            if type_value == 11 or type_value == 12:
                com_test_type = app_json['comTestType']

            app_info_url = "%s/v0.8/appinfo/%s" % (storage_host, factory_id)
            app_info_json = get_data(app_info_url)
            try:
                logger.warning("[ERROR] %s " % app_info_json['message'])
                raise Exception()
                sys.exit(1)
            except KeyError:
                pass

            icon_url = ''
            try:
                if app_info_json['icon'] and app_info_json['icon'].find('../') == -1:
                    icon_url = app_info_json['icon']
            except KeyError:
                icon_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/app.png'

            if icon_url == '' or icon_url == None:
                icon_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/app.png'

            factory_app_type = 'main'
            try:
                if app_info_json['app_type']:
                    factory_app_type = app_info_json['app_type']
            except KeyError:
                pass
            logger.debug("应用主子类型factoryAppType: %s" % factory_app_type)
            variable_dict['factoryAppType'] = factory_app_type

            package_name = ''
            package_name_str = ''
            if app_type.lower() == 'android':

                android_icon = app_info_json['android_icon']
                if android_icon:
                    icon_url = android_icon

                package_name = app_info_json['package_name']
                package_name_str = PACKAGE_NAME_ANDROID

                try:
                    launch_url = app_info_json['android_image']
                except KeyError:
                    launch_url = 'http://cdncs.101.com/v0.1/static/app_factorty_config/app_factory_config/android_launch.9.png'

                if launch_url == '' or launch_url == None:
                    launch_url = 'http://cdncs.101.com/v0.1/static/app_factorty_config/app_factory_config/android_launch.9.png'

                logger.debug("launch_url: %s" % launch_url)
                variable_dict['launch_url'] = launch_url

            elif app_type.lower() == 'ios':

                ios_icon = app_info_json['ios_icon']
                if ios_icon:
                    icon_url = ios_icon

                package_name = app_info_json['package_name_ios']
                package_name_str = PACKAGE_NAME_IOS

                try:
                    launch_small_url = app_info_json['ios5_image']
                except KeyError:
                    launch_small_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'

                if launch_small_url == '' or launch_small_url == None:
                    launch_small_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'
                logger.debug("启动小图标: %s" % launch_small_url)
                variable_dict['smallLaunchImg'] = launch_small_url

                try:
                    launch_big_url = app_info_json['ios6_image']
                except KeyError:
                    launch_big_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'

                if launch_big_url == '' or launch_big_url == None:
                    launch_big_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'
                logger.debug("启动大图标: %s" % launch_big_url)
                variable_dict['bigLaunchImg'] = launch_big_url

                try:
                    pad_launch_big_url = app_info_json['ios_pad_image']
                except KeyError:
                    pad_launch_big_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'

                if pad_launch_big_url == '' or pad_launch_big_url == None:
                    pad_launch_big_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'
                logger.debug("pad横屏启动大图标: %s" % pad_launch_big_url)
                variable_dict['padLaunchImg'] = pad_launch_big_url

                try:
                    pad_landscape_launch_img = app_info_json['ios_pad_landscape_image']
                except KeyError:
                    pad_landscape_launch_img = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'

                if pad_landscape_launch_img == '' or pad_landscape_launch_img == None:
                    pad_landscape_launch_img = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'
                logger.debug("pad竖屏启动大图标: %s" % pad_landscape_launch_img)
                variable_dict['padLandscapeLaunchImg'] = pad_landscape_launch_img

                try:
                    iphonex_launch_img = app_info_json['ios10_image']
                except KeyError:
                    iphonex_launch_img = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'

                if iphonex_launch_img == '' or iphonex_launch_img == None:
                    iphonex_launch_img = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/launch_image.png'
                logger.debug("iPhoneX启动图标: %s" % iphonex_launch_img)
                variable_dict['iPhoneXLaunchImg'] = iphonex_launch_img

                variable_dict['build_icon_64'] = os.path.join(os.getcwd(), 'target/temp/AppIcon64.png')
                variable_dict['build_icon_128'] = os.path.join(os.getcwd(), 'target/temp/AppIcon128.png')

            logger.debug("icon_url: %s" % icon_url)
            variable_dict['build_app_icon'] = icon_url

            if package_name == '':
                try:
                    package_name = app_json[package_name_str]
                except KeyError:
                    package_name = 'com.nd.app.factory.app' + app_json['name'].replace('-', '')

                if package_name == '' or package_name == None:
                    package_name = 'com.nd.app.factory.app' + app_json['name'].replace('-', '')

            logger.debug("package_name: %s" % package_name)
            variable_dict['build_package'] = package_name

            try:
                label = app_json[CHINESE_NAME]
            except KeyError:
                label = app_json['name']

            if label == '' or label == None:
                label = app_json['name']
            logger.debug("label: %s" % label)
            variable_dict['build_app_label'] = label

            version_json = result_json['version']

            version_name = ''
            try:
                version_name = version_json[VERSION_NAME]
            except KeyError:
                pass
            logger.debug("version_name: %s" % version_name)
            variable_dict['build_version_label'] = version_name

            version_description = ''
            try:
                version_description = version_json[VERSION_DESC]
            except KeyError:
                pass
            logger.debug("version_description: %s" % version_description)
            variable_dict['build_version_description'] = version_description

            build_multi_channel = ''
            try:
                build_multi_channel = version_json['build_multi_channel']
            except KeyError:
                pass
            logger.debug("build_multi_channel: %s" % build_multi_channel)
            variable_dict['build_multi_channel'] = build_multi_channel

            version_white_name = ''
            try:
                version_white_name = ','.join(version_json['version_white_name'])
            except KeyError:
                pass
            logger.debug("version_white_name: %s" % version_white_name)
            variable_dict['versionWhiteName'] = version_white_name

            env_client = 'dev'
            try:
                env_type = version_json['envType']
                if env_type == '8':
                    env_client = 'release'
                elif env_type == '10':
                    env_client = 'aws'
                elif env_type == '16':
                    env_client = 'party'
            except KeyError:
                pass
            logger.debug("env_client: %s" % env_client)
            variable_dict['env_client'] = env_client

            app_name = ''
            try:
                app_name = version_json[APP_NAME]
            except KeyError:
                pass
            logger.debug("app_name: %s" % app_name)
            variable_dict['build_app_name'] = app_name

            try:
                build_type = app_json['buildType']
            except KeyError:
                pass

            try:
                trial_period = app_json['trial_period']
            except KeyError:
                trial_period = '0'
            logger.debug("试用期（企业门户应用）trial_period: %s" % trial_period)
            variable_dict['trial_period'] = trial_period

            oid = ''
            try:
                oid = app_json['oid']
            except KeyError:
                pass
            logger.debug("oid: %s" % oid)
            variable_dict['build_app_id'] = oid

        logger.debug("com_test_type: %s" % com_test_type)
        variable_dict['comTestType'] = com_test_type

        logger.debug("应用版本（企业门户应用）buildType: %s" % build_type)
        variable_dict['build_type'] = build_type

        variable_dict['envtarget'] = envtarget

        if envtarget.lower() == 'aws-california-wx':
            envtarget = 'aws-california'
        variable_dict['env_target'] = envtarget

        return variable_dict


def main(args):
    factory_id = args.factoryId
    envtarget = args.envtarget
    app_type = args.appType
    env_jenkins = args.envJenkins
    version_id = args.versionId
    version2_app_factory = args.version2AppFactory
    is_local = args.isLocal

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    init_variable = InitGlobalVariableService(target_path, env_jenkins, is_local)
    variable_dict = init_variable.initGlobalVariable(factory_id, envtarget, app_type, version_id, version2_app_factory)
    variable_json = json.dumps(variable_dict)

    file_path = os.path.join(target_path, 'variables.json')
    with open(file_path, "w") as f:
        f.write(variable_json)
    logger.info("write data to %s" % file_path)

    if is_local:
        storage_host = variable_dict['app_native_storage']
        defines = Defines(target_path)
        defines.download_define(variable_dict,storage_host, factory_id)

        build_config = BuildConfig(target_path)
        build_config_json = build_config.get_build_config(env_jenkins,is_local)
        build_config.write_build_config(build_config_json)
        #build_config_data = init_variable.read_build_config()
        #build_config_json = json.loads(build_config_data)
        #build_config_path = os.path.join(target_path, 'build_config.json')
        #write_content_to_file(build_config_path, json.dumps(build_config_json))
        #logger.info("write data to %s" % build_config_path)

