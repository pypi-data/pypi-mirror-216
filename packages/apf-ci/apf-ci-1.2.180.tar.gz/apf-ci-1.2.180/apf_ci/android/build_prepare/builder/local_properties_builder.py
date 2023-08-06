#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
strictMode,debugMode,targetSdkVersion统一处理，然后更新 ./local.properties文件内容
"""

import sys
import json
from apf_ci.util.file_utils import *
from apf_ci.util.property import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.version_utils import get_target_version_android
from apf_ci.app_init.utils.build_config_utils import BuildConfig


class LocalPropertiesBuilder:
    def __init__(self):
        pass

    def perform(self, variables_dict):
        """
        原java的3个builder有很多冗余代码，故重新整合。
        包含了： 1、StrictModelBuilder 2、DebugModelBuilder 3、TargetSdkVersionBuilder
        :param variables_dict:
        :return:
        """
        com_test_type = variables_dict["comTestType"]
        logger.debug("comTestType:%s" % com_test_type)

        if not com_test_type:
            com_test_type = "default"

        # 获取build_config.json 和 config.json文件内容
        workspace_path = os.getcwd()
        build_config = BuildConfig(os.path.join(workspace_path, 'target'))
        build_config_json = build_config.read_build_config()
        config_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/config.json")
        if not os.path.exists(config_file_path):
            return
        config_content_str = read_file_content(config_file_path)
        config_json = json.loads(config_content_str)

        # local.properties路径
        property_file_path = os.path.join(os.getcwd(), "local.properties")
        properties = Properties(property_file_path)

        # strict_mode
        self._strict_mode_perform(build_config_json, config_json, com_test_type, properties)

        # debug_mode
        self._debug_mode_perform(build_config_json, config_json, properties)

        # target_sdk_version
        self._target_sdk_version_perform(build_config_json, config_json, properties)


    def _strict_mode_perform(self, build_config_json, config_json, com_test_type, properties):
        """
        1、strict_mode 写入local.properties
        :param build_config_json:
        :param config_json:
        :param com_test_type:
        :param properties:
        :return:
        """
        logger.info(" 开始do strict mode config")
        strict_mode_config_object = build_config_json.get("strict_model_config", {})
        logger.debug("strict_model_config: %s" % strict_mode_config_object)

        real_strict_mode = ""
        temp = strict_mode_config_object.get(com_test_type)
        if temp:
            real_strict_mode = temp
        logger.debug("strictModeDefault: %s" % real_strict_mode)

        strict_mode_map = {}
        if not config_json:
            return

        strict_mode = config_json.get("strictModel")
        logger.debug("config.json中strictMode value: %s" % strict_mode)

        if not strict_mode:
            strict_mode = real_strict_mode

        strict_mode_map["strictModel"] = strict_mode
        # Android严格模式需要支持具体明细项的独立开关
        android_array = config_json.get("android")
        if android_array:
            # 严格模式明细开关默认值
            detail_config_json = build_config_json.get("strict_model_detail_config", {})
            logger.debug("strict_model_detail_config:%s" % detail_config_json)

            for android_json in android_array:
                if not isinstance(android_json, dict):
                    continue
                    # 将config.json中配置的严格模式明细项放入map中，如果不存在或者空值，则取build_config.json中的detail_config默认值
                self._parse_strict_mode_detail_config(strict_mode_map, android_json, detail_config_json, com_test_type)

        self._write_strict_mode_into_local_properties(properties, strict_mode_map)
        logger.info(" do strict model config完毕")


    def _debug_mode_perform(self, build_config_json, config_json, properties):
        """
        2、debug model 写入local.properties
        :param build_config_json:
        :param config_json:
        :param properties:
        :return:
        """
        logger.info(" 开始 do debug model config")
        debug_mode = build_config_json.get("android_debug_mode", "")
        logger.debug("android_debug_mode:%s" % debug_mode)

        real_debug_mode = ""
        android_array = config_json.get("android")
        if android_array:
            for debug_android_json in android_array:
                if not isinstance(debug_android_json, dict):
                    continue
                real_debug_mode = debug_android_json.get("android_debug_mode", "")
                logger.debug("android_debug_mode real:%s" % real_debug_mode)
                break

        if not real_debug_mode:
            real_debug_mode = debug_mode

        debug_mode_map = {
            "isOpenDebug": real_debug_mode
        }
        self._write_strict_mode_into_local_properties(properties, debug_mode_map)
        logger.info(" 结束 do debug model config")


    def _target_sdk_version_perform(self, build_config_json, config_json, properties):
        """
        解析组件中配置的target_sdk_version的值，写入local.properties
        :param config_json:
        :param properties:
        :return:
        """
        logger.info(" 开始解析 Android TargetSdkVersion 值")
        try:
            android_array = config_json.get("android")
            if android_array:
                for target_android_json in android_array:
                    if not isinstance(target_android_json, dict):
                        continue
                    target_sdk_version = target_android_json.get("targetSdkVersion", "")
                    logger.debug("config targetSdkVersion:%s" % target_sdk_version)
                    target_sdk_version = get_target_version_android(build_config_json, target_sdk_version)
                    logger.debug("final targetSdkVersion:%s" % target_sdk_version)
                    break

            # 若没有传值，则不保存到properties文件

            if not target_sdk_version:
                return

            target_sdk_map = {
                "targetSdkVersion": target_sdk_version
            }
            self._write_strict_mode_into_local_properties(properties, target_sdk_map)
        except Exception as e:
            error_message = "解析 Android TargetSdkVersion 值失败 %s" % e
            logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
            traceback.print_exc()
            sys.exit(1)

        logger.info(" do Android TargetSdkVersion Builder完毕")

    def _parse_strict_mode_detail_config(self, strict_mode_map, android_json, detail_config_json, com_test_type):
        if detail_config_json:
            for key in detail_config_json:
                strict_mode_value = android_json.get(key)
                # 编辑器配置为空时，取默认值
                if not strict_mode_value:
                    strict_mode_detail_json_obj = detail_config_json.get(key, {})
                    strict_mode_value = strict_mode_detail_json_obj.get(com_test_type, "")
                strict_mode_map[key] = strict_mode_value

    def _write_strict_mode_into_local_properties(self, properties, properties_key_value_map):
        try:
            for key in properties_key_value_map:
                properties.put(key, properties_key_value_map[key])
        except Exception as e:
            error_message = '严格模式写入异常 %s' % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)
