#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import post_for_array
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import *
import os
import json


class LiteApp:
    def __init__(self, app_factory_path):
        self.app_factory_path = app_factory_path

    def get_host_map(self, lite_app_host, language, lite_app_map):
        """
        获取业务组件对应的轻应用地址集合
        :param lite_app_host:
        :param language:
        :param lite_app_map:
        :return:
        """
        app_build_path = os.path.join(self.app_factory_path, language, 'components', 'build.json')
        if os.path.exists(app_build_path):
            app_build_data = read_file_content(app_build_path)
            app_build_array = json.loads(app_build_data)

            request_body_array = []
            for app_build_json in app_build_array:
                component_json = app_build_json['component']

                request_body_json = {}
                request_body_json['namespace'] = component_json['namespace']
                request_body_json['name'] = component_json['name']
                request_body_json['version'] = app_build_json['version']
                request_body_array.append(request_body_json)

            url = lite_app_host + '/v0.1/versions/batch'
            response_body_array = post_for_array(url, request_body_array)
            for response_body_json in response_body_array:
                namespace = response_body_json['namespace']
                biz_name = response_body_json['biz_name']
                host = response_body_json['host']
                logger.debug('namespace: %s, biz_name: %s, host: %s' % (namespace, biz_name, host))

                if host is None:
                    host = ''

                key = '%s_%s' % (namespace, biz_name)
                lite_app_map[key] = host

    def get_lite_app_host(self, target_path, env, lite_app_host, lite_app_aws_json):
        lite_app_host_map = {}

        if lite_app_host:
            return

        if env == '':
            config_path = os.path.join(self.app_factory_path, 'app', 'config.json')
            if not os.path.exists(config_path):
                return

            config_data = read_file_content(config_path)
            env = json.loads(config_data)['env']

        build_config = BuildConfig(os.path.join(os.getcwd(), 'target'))
        build_config_json = build_config.read_build_config()
        deploy_host_json = get_app_factory_deploy_host(build_config_json)
        lite_app_host_json = deploy_host_json['lite_app_host']

        search_key = ''
        if env == '8':
            search_key = 'release'
        elif env == '10':
            search_key = 'aws'
        elif env == '17':
            search_key = 'aws-california'

        stage_host = ''
        if search_key:
            lite_app_aws_json = lite_app_host_json[search_key]
            stage_host = lite_app_aws_json['stage']

        if stage_host:
            lite_app_host = stage_host
        else:
            lite_app_host = lite_app_host_json['default']

        lite_app_host_map['liteAppAwsJson'] = lite_app_aws_json
        lite_app_host_map['liteAppHost'] = lite_app_host

        return lite_app_host_map


