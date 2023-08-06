#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

#from apf_ci.util.build_config_utils import *
from apf_ci.config.language_service import *
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import *

class EnvService:
    __env_stage_dict = {
        1: 'dev',
        2: 'debug',
        8: 'release'
    }

    __component_function_list = [
        'APP_FACTORY_FUNCTION',
        'CUSTOM_ENV_APP_FACTORY_FUNCTION'
    ]
    __component_integration_list = [
        'APP_FACTORY_INTEGRATE',
        'CUSTOM_ENV_APP_FACTORY_INTEGRATE'
    ]

    def __init__(self, variable_dict, env_jenkins):
        self.variable_dict = variable_dict
        self.env_jenkins = env_jenkins

    def __get_stage(self, environment_dict):
        """
        如果envtarget对应的stage值不为空，则取该值；否则为env_jenkins对应的值，默认为dev
        :param environment_dict: build_config.json文件中app_factory_build_environment节点下envtarget为key的集合
        :return:
        """
        stage = 'dev'
        if self.env_jenkins in self.__env_stage_dict.keys():
            stage = self.__env_stage_dict[self.env_jenkins]

        envtarget = self.variable_dict['envtarget']
        environment_json = environment_dict[envtarget]
        if environment_json['stage']:
            stage = environment_json['stage']

        return stage

    def __get_scope(self):
        com_test_type = self.variable_dict['comTestType']
        if com_test_type in self.__component_function_list:
            scope = 'component_function'
        elif com_test_type in self.__component_integration_list:
            scope = 'component_integration'
        else:
            scope = 'app'

        return scope

    def __init_build_version_code(self, version_code_start):
        build_version_code = self.variable_dict['build_version_code']
        if not build_version_code.isdigit():
            return
        init_build_version_code = int(build_version_code)

        logger.debug('version_code_start: %s' % version_code_start)
        logger.debug('before build_version_code: %s' % build_version_code)

        if version_code_start and version_code_start.isdecimal() and int(version_code_start) > 0:
            init_build_version_code += int(version_code_start)

        self.variable_dict['build_version_code'] = str(init_build_version_code)

    def __init_pad_ios_standard_architecture(self, config_json):
        pad = ''
        ios_standard_architecture = ''

        if 'ios' in config_json:
            ios_array = config_json['ios']
            if ios_array.__len__() > 0:
                ios_json = ios_array[0]
                pad = ios_json['pad']
                ios_standard_architecture = ios_json['ios_standard_architecture']

        logger.debug('pad: %s' % pad)
        logger.debug('ios_standard_architecture: %s' % ios_standard_architecture)
        self.variable_dict['pad'] = pad
        self.variable_dict['ios_standard_architecture'] = ios_standard_architecture

    def append_data_to_config(self, app_factory_path, environment_dict, build_config_json, app_json, app_info_json):
        config_path = os.path.join(app_factory_path, 'app', 'config.json')
        config_data = read_file_content(config_path)
        config_json = json.loads(config_data)

        # 写入 factory_id
        config_json['factory_id'] = self.variable_dict['factoryId']

        dns_enable = False
        if self.env_jenkins == 8:
            #ios_dns_enable_environment = get_ios_dns_enable_environment(build_config_json)
            ios_dns_disable_environment = get_ios_dns_disable_environment(build_config_json)
            dns_enable = get_dns_enable(config_json['env'], ios_dns_disable_environment)
            logger.debug('dns_enable: %s' % dns_enable)
        config_json['dns_enable'] = dns_enable

        rn_debug_mode = ''
        if 'react' in config_json:
            react = config_json['react']
            if react:
                react0 = react.__getitem__(0)
                if react0:
                    rn_debug_mode = react0['rn_debug_mode']
        if rn_debug_mode is None or rn_debug_mode.strip()=="":
            rn_debug_mode = get_rn_debug_mode(build_config_json)
        rn_flag = False
        if rn_debug_mode.lower() == 'true':
            rn_flag = True
        config_json['rn_debug_mode'] = rn_flag

        stage = self.__get_stage(environment_dict)
        config_json['stage'] = stage

        envtarget = self.variable_dict['envtarget']
        environment_json = environment_dict[envtarget]
        env_client = environment_json['env_client']
        config_json['env_client'] = env_client

        languages_array = self.variable_dict['languages']
        resource_host = self.variable_dict['fac_resource_manage']
        all_languages_array = self.variable_dict['allLanguages']
        lang_array, i18n_json = language_i18n(languages_array, all_languages_array)
        config_json['language'] = lang_array
        config_json['i18n'] = i18n_json

        nowmillis = (int(round(time.time() * 1000)))
        config_json['build_time'] = nowmillis

        build_type = ''
        if 'build_type' in self.variable_dict:
            build_type = self.variable_dict['build_type']
        if build_type == 'trial':
            trial_period = self.variable_dict['trial_period']
            config_json['trial_period'] = int(trial_period)
            config_json['build_type'] = build_type

        config_json['scope'] = self.__get_scope()

        allow_check_update = True
        if 'use_app_factory_update' in app_info_json and type(app_info_json['use_app_factory_update']) == bool:
            allow_check_update = app_info_json['use_app_factory_update']
        config_json['allow_check_update'] = allow_check_update

        language_tree_array = get_language_tree(resource_host)
        language_weight_map, language_parent_map, language_list = language_weight_parent_list(language_tree_array)
        language_enable_map, language_enable_parent_map = language_enable_parent(languages_array, language_weight_map, language_parent_map)
        sort_language_enables = sort_by_value(language_enable_map)

        config_json['language_list'] = language_list
        config_json['language_enable'] = sort_language_enables

        language_groups_list = language_groups(language_enable_parent_map, language_parent_map, language_weight_map)
        config_json['language_group'] = language_groups_list

        language_default_json = get_language_default_json(sort_language_enables, language_parent_map, app_json)
        config_json['language_default'] = language_default_json

        lite_app_host = self.variable_dict['lite_app_server']
        app_cdn_host = get_app_cdn_host(build_config_json, config_json, self.variable_dict['factoryId'])
        parse_app_factory_deploy_host(build_config_json, config_json, lite_app_host, app_cdn_host)

        logger.debug('进行config.json写入')
        write_content_to_file(config_path, json.dumps(config_json))
        logger.info('config.json写入结束')

        self.variable_dict['app_build_time'] = config_json['build_time']
        self.variable_dict['env'] = config_json['env']
        self.variable_dict['env_client'] = env_client
        self.variable_dict['stage'] = stage
        logger.debug('rn_debug_mode: '+ rn_debug_mode)
        self.variable_dict['rn_debug_mode'] = rn_debug_mode

        self.__init_build_version_code(config_json['version_code_start'])
        self.__init_pad_ios_standard_architecture(config_json)

        self.variable_dict['installPackageName'] = config_json['filename']
        #self.variable_dict['allLanguages'] = all_languages_array
