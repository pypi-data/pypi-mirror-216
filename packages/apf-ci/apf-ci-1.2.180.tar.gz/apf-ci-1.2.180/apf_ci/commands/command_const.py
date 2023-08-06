#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
命令行常量


"""

__author__ = 'gpy'

import json
from apf_ci.util.file_utils import *


def get_environment_config():
    env_config_url = "http://git.sdp.nd/jenkins/apf-jenkins-config/raw/master/environment_config.json"
    env_config = read_cs_content(env_config_url)
    env_json = json.loads(env_config)
    env_list = env_json['ENV_TARGET_LIST']
    return env_list

