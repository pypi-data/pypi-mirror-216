#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
React native component module.
"""

__author__ = 'LianGuoQing'

import os
import json
import subprocess
import platform
import sys

from apf_ci.util.file_utils import read_file_content, write_content_to_file
from apf_ci.util.log_utils import logger

class ReactLocalBuilder:
    """The apf_ci build for react native component"""

    __component_type_dict = {
        'ios': 'react-ios',
        'android': 'react-android'
    }

    def __init__(self, app_factory_path, target_path, app_type):
        self.app_factory_path = app_factory_path
        self.target_path = target_path
        self.app_type = app_type

    def parse_components(self):
        """
        Parsing the react native features in the components.json file.
        :return: boolean
        """
        components_path = os.path.join(self.app_factory_path, 'app', 'components.json')
        components_data = read_file_content(components_path)
        components_json_array = json.loads(components_data)

        new_components_json_array = []

        component_type = self.__component_type_dict[self.app_type]
        for components_json in components_json_array:
            type_array = components_json['type']
            if component_type in type_array:
                new_components_json_array.append(components_json)

        new_components_path = os.path.join(self.target_path, 'react', 'config', 'components.json')
        write_content_to_file(new_components_path, json.dumps(new_components_json_array))

        if new_components_json_array.__len__() > 0:
            return True

        return False

    def execute_build(self, build_tool, git_repository, commit_id, is_dev, reset_cache):
        """
        Install build tools, and execute the build script.
        :param build_tool:
        :param git_repository:
        :param commit_id:
        :param is_dev:
        :param reset_cache:
        :return:
        """
        logger.info(' npm config set registry="http://registry.npm.sdp.nd/"')

        platform_name = platform.system()
        if platform_name == 'Windows':
            subprocess.call(['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"'], shell=True)

            if self.app_type == 'android':
                logger.info(' npm config set unsafe-perm true')
                subprocess.call(['npm', 'config', 'set', 'unsafe-perm', 'true'], shell=True)

            logger.info(" npm install %s" % build_tool)
            subprocess.call(['npm', 'install', build_tool], shell=True)

        else:
            self.execute_command(['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"'])

            if self.app_type == 'android':
                logger.info(' npm config set unsafe-perm true')
                self.execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'])

            logger.info(" npm install %s" % build_tool)
            self.execute_command(['npm', 'install', build_tool])

        # logger.info(" yarn add %s" % build_tool)
        # subprocess.call(['yarn', 'add', build_tool], shell=True)

        js_name = 'node_modules/@sdp.nd/react-native-component-builder/index.js'
        logger.info(" node %s --gitRepository %s --commitId %s --platform %s --dev %s --reset-cache %s"
              % (js_name, git_repository, commit_id, self.app_type, is_dev, reset_cache))
        subprocess.call(['node', js_name,
                         '--gitRepository', git_repository,
                         '--commitId', commit_id,
                         '--platform', self.app_type,
                         '--dev', is_dev,
                         '--reset-cache', reset_cache])
    def execute_command(self, popenargs):
        popen = subprocess.Popen(popenargs, stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            next_line = popen.stdout.readline()
            if next_line == '' and popen.poll() != None:
                break
            sys.__stdout__.write(next_line)
            sys.__stdout__.flush()