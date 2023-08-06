#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import BuildConfig


class CheckEnvNameBuilder:
    def __init__(self, env_target):
        self.env_target = env_target

    def perform(self, variables_json):
        workspace_path = os.getcwd()
        config_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/config.json")
        assemble_mode = self._get_assemble_mode(config_file_path)
        if assemble_mode == "":
            return self._get_env_name(workspace_path, self.env_target)
        logger.debug(" 从 %s 中取到assemble_mode值：%s" % (config_file_path, assemble_mode))

        env_name = assemble_mode
        is_dev = True
        if env_name.lower() == "debug":
            is_dev = True
        elif env_name.lower() == "release":
            is_dev = False

        logger.debug(" 【isDev】：%s" % is_dev)
        variables_json["is_dev"] = str(is_dev)
        variables_path = os.path.join(workspace_path, "target", "variables.json")
        write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
        return True

    def _get_assemble_mode(self, config_file_path):
        assemble_mode = ""
        if os.path.exists(config_file_path):
            config_content = read_file_content(config_file_path)
            if config_content != "":
                config_json = json.loads(config_content)
                assemble_mode = config_json.get("assemble_mode", "")
        return assemble_mode

    def _get_env_name(self, workspace_path, env_target):
        build_config = BuildConfig(os.path.join(workspace_path, 'target'))
        build_config_json = build_config.read_build_config()
        #build_config_file_path = os.path.join(workspace_path, "target/build_config.json")
        #if os.path.exists(build_config_file_path):
        #    build_config = read_file_content(build_config_file_path)
        #    build_config_json = json.loads(build_config)
        build_config_json_arr = build_config_json.get("app_factory_build_environment", [])
        for items_json in build_config_json_arr:
            if isinstance(items_json, dict):
                envtarget = items_json.get("envtarget", "")
                if envtarget == env_target:
                    env_name = items_json.get("name", "")
                    logger.debug(" envtarget对应的name值：%s" % env_name)
                    return env_name
        return ""