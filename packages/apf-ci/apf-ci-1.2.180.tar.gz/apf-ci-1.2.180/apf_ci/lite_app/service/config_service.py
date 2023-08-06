#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
轻应用资源处理模块
"""

__author__ = '961111'

from  apf_ci.app_init.update_variable_json import *
from apf_ci.init.validate_service import ValidateService
from apf_ci.init.git_template_service import *
from apf_ci.util.file_utils import *
from apf_ci.resource.resource_builder import *
from apf_ci.app_init.app_config import main as app_config
from apf_ci.app_init.app_resource import main as app_resource

class ConfigService:

    def create_lite_app_service_json(self, param_map):
        '''
        创建轻应用包中的service.json文件
        '''
        workspace_path = os.getcwd()
        logger.info(" param_map: %s" % param_map)

        target_path = param_map['target_path']
        logger.info(" target_path: %s" % target_path)
        resource_host = param_map['fac_resource_manage']
        default_language = param_map['defaultLang']
        resource_config = ResourceConfig(workspace_path)
        environment_resource_map, environment_name_map = resource_config.init_environment_resource(resource_host)

        app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')
        biz_env_path = os.path.join(app_factory_path, default_language, 'components', 'biz_env.json')
        biz_plugin_path = os.path.join(app_factory_path, default_language, 'components', 'plugin.json')
        target_build_path = os.path.join(target_path, 'app_component_pages', default_language, 'build.json')
        env = param_map['env']
        biz_version_map = resource_config.init_bizs_version(target_build_path)
        each_environment_bizs_map, plugin_env_map = resource_config.init_each_environment_bizs(biz_env_path,
                                                                                               biz_plugin_path,
                                                                                               biz_version_map,
                                                                                               environment_resource_map,
                                                                                               env,
                                                                                               environment_name_map)

        lite_app_config_path = os.path.join(workspace_path, 'target', 'local_h5')
        resource_config.create_service_json(each_environment_bizs_map, resource_host, lite_app_config_path)
        logger.info(" 轻应用 生成service.json成功: %s" % lite_app_config_path)


    def copy_lite_app_json(self, npm_dto):
        workspace_path = os.getcwd()
        module_name = npm_dto.module_name
        # 拷贝service.json
        service_json_source = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app', 'service.json')
        service_json_target = os.path.join(workspace_path, 'target/local_h5', module_name, 'app/service.json')
        self.copy_common_json(npm_dto, service_json_source, service_json_target)
        # 拷贝component.json
        component_json_source = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app', 'components.json')
        component_json_target = os.path.join(workspace_path, 'target/local_h5', module_name, 'app/components.json')
        self.copy_common_json(npm_dto, component_json_source, component_json_target)
        # 拷贝datasources.json
        datasources_json_source = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app', 'datasources.json')
        datasources_json_target = os.path.join(workspace_path, 'target/local_h5', module_name, 'app/datasources.json')
        self.copy_common_json_without_filter(datasources_json_source, datasources_json_target)
        # 拷贝page_controller.json
        page_controller_json_source = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app', 'page_controller.json')
        page_controller_json_target = os.path.join(workspace_path, 'target/local_h5', module_name, 'app/page_controller.json')
        self.copy_common_json_without_filter(page_controller_json_source, page_controller_json_target)
        # 拷贝page_attributes.json
        page_attributes_json_source = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app',
                                                   'page_attributes.json')
        page_attributes_json_target = os.path.join(workspace_path, 'target/local_h5', module_name,
                                                   'app/page_attributes.json')
        self.copy_page_attributes_json(npm_dto, page_attributes_json_source, page_attributes_json_target)
        logger.info("[INFO] 初始化轻应用配置文件成功")


    def copy_common_json(self, npm_dto, source_config_path, target_config_path):
        '''
        统一格式的配置文件拷贝
        :param npm_dto:
        :param source_config_path:
        :param target_config_path:
        :return:
        '''
        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        config_json_content = read_file_content(source_config_path)
        formatted_config_json = json.loads(config_json_content)
        final_config_json = []
        for item in formatted_config_json:
            component_info = item["component"]
            if namespace == component_info["namespace"] and biz_name == component_info["name"]:
                final_config_json.append(item)
                break

        write_content_to_file(target_config_path, json.dumps(final_config_json))

    def copy_common_json_without_filter(self, source_config_path, target_config_path):
        '''
        全量拷贝文件
        :param npm_dto:
        :param source_config_path:
        :param target_config_path:
        :return:
        '''
        copy_file(source_config_path, target_config_path)

    def copy_page_attributes_json(self, npm_dto, source_config_path, target_config_path):
        '''
        拷贝page_attributes.json
        :param npm_dto:
        :param source_config_path:
        :param target_config_path:
        :return:
        '''
        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        key_filter = namespace + "." + biz_name
        config_json_content = read_file_content(source_config_path)
        formatted_config_json = json.loads(config_json_content)
        final_config_json = {}
        for key in formatted_config_json:
            if key == key_filter:
                final_config_json[key] = formatted_config_json[key]
                break

        write_content_to_file(target_config_path, json.dumps(final_config_json))