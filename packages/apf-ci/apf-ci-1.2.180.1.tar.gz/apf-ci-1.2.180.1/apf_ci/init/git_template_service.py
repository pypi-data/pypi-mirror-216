#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Git模板相关业务
"""

__author__ = 'LianGuoQing'

import os
import json
import subprocess

from apf_ci.util.http_utils import get_data
from apf_ci.util.log_utils import logger

class GitTemplateService:
    __git_template = ''
    __commit_id = ''
    __git_home = '/usr/bin/git'
    # 本地调试
    #__git_home = 'D:/software/other/Git/cmd/git.exe'

    def __init__(self, git_template, commit_id):
        self.__git_template = git_template
        self.__commit_id = commit_id

    def execute_command(self, popenargs):
        completed_process = subprocess.run(popenargs, stdout=subprocess.PIPE, universal_newlines=True, check=True)
        print(completed_process.stdout)
        return completed_process

    def clone_template(self):
        """
        下载git模板工程
        :return:
        """
        # 先按分支克隆
        branch_args = [self.__git_home, 'clone', '-b', self.__commit_id, '--depth', '1', self.__git_template, '.']
        try:
            self.execute_command(branch_args)
        except subprocess.CalledProcessError:
            logger.warning('[DEBUG] 按分支克隆失败')

            # 如果分支克隆失败，则先去前5的提交记录
            init_depth = 5
            clone_args = [self.__git_home, 'clone', '--depth', str(init_depth), self.__git_template, '.']
            self.execute_command(clone_args)

            # 按commitId进行克隆
            checkout_args = [self.__git_home, 'checkout', self.__commit_id]
            try:
                self.execute_command(checkout_args)
            except subprocess.CalledProcessError:
                logger.warning('[DEBUG] 按commitId克隆失败：depth=' + str(init_depth))

                for i in range(1, 11):
                    depth = i * 30
                    self.execute_command([self.__git_home, 'fetch', '--depth', str(depth)])

                    try:
                        self.execute_command([self.__git_home, 'checkout', self.__commit_id])
                        break
                    except subprocess.CalledProcessError:
                        logger.warning('[DEBUG] 按commitId克隆失败：depth=' + str(depth))

                        if i == 10:
                            raise Exception('[ERROR] 克隆失败')
                            sys.exit(1)

    def get_git_template_info(self, storage_host, factory_id, app_type, apf_ci_biz_version):
        if self.__git_template.strip() and self.__commit_id.strip():
            return None

        templates = get_git_templates_with_version(apf_ci_biz_version)
        if self.parse_main_component_templates(templates, app_type):
            return templates

        self.get_snapshot_templates(storage_host, factory_id, app_type)

        if self.__git_template.strip() == '' or self.__commit_id.strip() == '':
            self.get_server_templates(storage_host, app_type)
        
        return None

    def get_server_templates(self, storage_host, app_type):
        template_url = "%s/v0.8/template/%s" % (storage_host, app_type.lower())
        template_data_json = get_data(template_url)

        """
        {"commit_id": "c3204b9", "template": "git@git.sdp.nd:component-android/android-template-project.git","type": "android"}
        """
        source = template_data_json['template']
        commit_id = template_data_json['commit_id']

        if source and commit_id:
            logger.debug("server templates: [template]%s, [commitId]%s" % (source, commit_id))
            self.__git_template = source
            self.__commit_id = commit_id

    def get_snapshot_templates(self, storage_host, factory_id, app_type):
        """
        '[{"commitId": "c3204b9", "template": "git@git.sdp.nd:component-android/android-template-project.git","type": "android"},...]'
        """
        template = get_snapshot_templates_info(storage_host, factory_id)

        if template:
            template_arr = json.loads(template)
            for template_json in template_arr:
                type_str = template_json['type']
                source = template_json['template']
                commit_id = template_json['commitId']
                if type_str.lower() == app_type.lower() and source and commit_id:
                    logger.debug("snapshot templates: [template]%s, [commitId]%s" % (source, commit_id))
                    self.__git_template = source
                    self.__commit_id = commit_id

    def parse_main_component_templates(self, templates, app_type):
        """
        {
            'android': {
                'git': {
                    'source': 'git@git.sdp.nd:component-android/android-template-project.git',
                    'commit-id': '17598734'
                }
            },
            'ios': {
                'git': {
                    'source': 'git@git.sdp.nd:appcontainer/componentappbase.git',
                    'commit-id': '2a230fc'
                }
            },
            'h5-widget': {
                'git': {
                    'source': 'git@git.sdp.nd:h5/build-template.git',
                    'commit-id': '88fad9c7'
                }
            },
            'react-widget': {
                'git': {
                    'source': 'git@git.sdp.nd:app-factory/react-native-main-template.git',
                    'commit-id': 'e27ce7f3'
                }
            },
            'react': {
                'git': {
                    'source': 'git@git.sdp.nd:app-factory/react-native-main-module.git',
                    'commit-id': '70cb244'
                }
            }
        }
        """
        if templates:
            node = templates[app_type.lower()]
            git = node['git']
            source = git['source']
            commit_id = git['commit-id']

            if source and commit_id:
                logger.debug("main_component templates: [source]%s, [commit-id]%s" % (source, commit_id))
                self.__git_template = source
                self.__commit_id = commit_id
                return True
        return False

def get_git_templates_with_version(bizVersion):
    """
    获取项目模板信息
    :param biz_component_host: 获取业务组件定义的服务器地址
    :param bizVersion: 脚本工具业务组件 version
    :return: 项目模板信息 JSON 对象
    """

    biz_component_host = os.getenv('URL_BIZ_COMPONENT')
    comp_namespace = 'com.nd.sdp.app.factory.build'
    comp_name = 'apf-ci'

    define_url = "%s/v1.0/%s/%s/%s/define" % (biz_component_host, comp_namespace, comp_name, bizVersion)
    define_data_json = get_data(define_url)
    extensions = define_data_json['extensions']
    return extensions['templates']

def get_main_component_templates_info(storage_host, factory_id):
    """
    获取应用框架中的git模板配置信息
    :param storage_host: 应用存储服务地址
    :param factory_id:
    :return:
    """
    define_url = "%s/v0.8/define/%s" % (storage_host, factory_id)
    define_data_json = get_data(define_url)['data']

    for key in define_data_json:
        if key.startswith('com.nd.sdp.app.factory.build:apf-ci'):
            value = define_data_json[key]
            try:
                extensions = value['extensions']
                return extensions['templates']
            except KeyError:
                return

def get_snapshot_templates_info(storage_host, factory_id):
    """
    获取应用快照中的git模板配置信息
    :param storage_host: 应用存储服务地址
    :param factory_id:
    :return:
    """
    apps_url = "%s/v0.8/apps/%s" % (storage_host, factory_id)
    apps_json = get_data(apps_url)
    template = apps_json['template']
    return template




