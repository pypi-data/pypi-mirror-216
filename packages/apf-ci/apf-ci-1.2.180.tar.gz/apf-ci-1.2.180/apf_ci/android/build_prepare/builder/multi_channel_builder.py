#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

from apf_ci.util.file_utils import *
from apf_ci.util.jenkins_utils import variables_value
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class MultiChannelBuilder:
    def __init__(self):
        pass

    def perform(self, config_json, variables_dict):
        gradle_buffer = ""
        gradle_buffer += "android {\n"
        gradle_buffer += "productFlavors {\n"
        gradle_buffer += "nd{}\n"

        multi_channel_arr = config_json.get("multi_channel")
        build_multi_channel = variables_dict.get("build_multi_channel")
        logger.info("======多渠道包插件构建 build_multi_channel====" + str(build_multi_channel))
        isMultiChannel = False
        if build_multi_channel == True or str(build_multi_channel) is 'True':
            isMultiChannel = True
        if isMultiChannel and multi_channel_arr:
            for object in multi_channel_arr:
                if isinstance(object, dict):
                    channel_name = object.get("channel_name", "")
                    if not channel_name:
                        error_message = "多渠道名称 channel_name 不能为空，%s" % object
                        logger.error(LoggerErrorEnum.JENKINS_BUILD_ERROR_004001, error_message)
                        traceback.print_exc()
                        sys.exit(1)
                    url = object.get("url", "")
                    if url == '':
                        logger.warning('多渠道 %s 的资料包为空 ' % channel_name)
                        continue
                    zip_file_path = os.path.join(os.getcwd(), "target/multi-channel", channel_name + ".zip")
                    try:
                        logger.debug(" 正在下载文件到：%s， url:%s" % (zip_file_path, url))
                        download_cs_file(url, zip_file_path, 3)
                    except Exception as e:
                        error_message = '下载ZIP包失败：%s' % url
                        logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, error_message)
                        traceback.print_exc()
                        sys.exit(1)

                    if not os.path.exists(zip_file_path):
                        logger.debug(" 文件不存在：%s" % zip_file_path)
                    else:
                        dir_path = os.path.join(os.getcwd(), "app/src", channel_name)
                        if not os.path.exists(dir_path):
                            os.mkdir(dir_path)
                        logger.debug(" 正在解压文件到：%s" % dir_path)
                        unzip(zip_file_path, dir_path)
                    gradle_buffer += channel_name + "{}\n"
        gradle_file_path = os.path.join(os.getcwd(), "app/app-factory-product.gradle")
        logger.debug(" 正在创建app-factory-product.gradle文件：%s" % gradle_file_path)
        logger.debug(" 正在向app-factory-product.gradle文件中写入内容...")
        gradle_buffer += "}\n"
        gradle_buffer += "productFlavors.all {\n"
        gradle_buffer += "flavor -> flavor.manifestPlaceholders = [CHANNEL_NAME: name]\n"
        gradle_buffer += "}\n"
        gradle_buffer += "}"
        js_data = gradle_buffer
        write_content_to_file(gradle_file_path, js_data)

        self._write_build_gradle()

    def _write_build_gradle(self):
        build_file_path = os.path.join(os.getcwd(), "app/build.gradle")
        build_gradle_content = read_file_content(build_file_path)
        if "file('app-factory-product.gradle').exists()" not in build_gradle_content:
            logger.debug(" 正在向build.gradle文件追加数据：%s" % build_file_path)
            build_gradle_buffer = "\n//目的是为了多渠道打包。\n"
            build_gradle_buffer += "def hasProduct = file('app-factory-product.gradle').exists()\n"
            build_gradle_buffer += "if (hasProduct) {\n"
            build_gradle_buffer += "  apply from: 'app-factory-product.gradle'\n"
            build_gradle_buffer += "}\n"

            write_content_to_file(build_file_path, build_gradle_buffer)
            logger.debug(" 数据添加完毕：\n%s" % build_gradle_buffer)


if __name__ == "__main__":
    #run_down()
    file_path = 'F:\\config.json'
    mu = MultiChannelBuilder()
    str_config = read_file_content(file_path)
    mu.perform(json.loads(str_config))
