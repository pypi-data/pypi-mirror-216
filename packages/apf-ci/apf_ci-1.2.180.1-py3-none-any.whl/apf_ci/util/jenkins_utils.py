#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import os
import json
import sys
import requests
from requests.auth import HTTPBasicAuth
from apf_ci.util.file_utils import read_file_content

def envs_value(key, env_jenkins=8, is_local=False):
    """
    根据key获取jenkins全局变量值，如果是本地则从本地配置文件中取
    :param key:
    :param env_jenkins: jenkins环境值
    :param is_local: 是否本地构建
    :return:
    """
    if is_local :
        # 获取全局变量配置文件
        config_name = 'config.json'
        if env_jenkins == 1:
            config_name = 'config_dev.json'
        elif env_jenkins == 2:
            config_name = 'config_debug.json'
        elif env_jenkins == 5:
            config_name = 'config_beta.json'

        config_path = os.path.join(sys.prefix, 'apf_ci-config', config_name)
        config_data = read_file_content(config_path)
        return json.loads(config_data)[key]
    else:
        try:
            return os.environ[key]
        except KeyError:
            return ''

def variables_value(key, is_local=False):
    """
    根据key获取全局变量值，如果是本地则从variables.json中取
    :param key:
    :param is_local: 是否本地构建
    :return:
    """
    if is_local:
        # 获取当前变量配置文件
        variables_path = os.path.join(os.getcwd(), 'target', 'variables.json')
        variables_data = read_file_content(variables_path)
        return json.loads(variables_data)[key]
    else:
        try:
            return os.environ[key]
        except KeyError:
            return ''


def get_jenkins_job_console_text(jenkins_url):
    """
    获取job构建的控制台输出文本
    :param jenkins_url:
    :param job_name:
    :param build_number:
    :return:
    """
    #username = "11114444"
    #password = "sdp.ci.2017"
    username = "10009550"
    password = "APFabc123456"
    # 获取构建的控制台输出内容
    response = requests.get(jenkins_url, auth=(username, password))
    content = response.content.decode("utf-8")
    return content


if __name__ == "__main__":
    #get_jenkins_job_console_text("http://jenkins.cc.service.debug.sdp.nd/job/lite0821_AppUpdate_Lite_Factory/10/consoleText")
    #get_jenkins_job_console_text("http://jenkins.cc.app.service.sdp.nd/job/sdev_A_I_F/21/console")
    get_jenkins_job_console_text("http://jenkins.cc.app.service.debug.sdp.nd/job/1-apf-ci-android-test/6/consoleText")
    #get_jenkins_job_console_text("http://jenkins.cc.app.service.debug.sdp.nd/job/1-apf-ci-android-test/config.xml")

