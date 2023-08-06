#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Check whether the project has the build conditions
"""

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import get_data, get_data_with_env_headers
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class ValidateService:
    def check_project(self, validate_host, factory_id, app_type):
        """
        通过调用校验服务API校验应用是否满足条件
        :param validate_host: 校验服务地址
        :param factory_id:
        :param app_type:
        :return:
        """
        validate_url = "%s/v0.3/validate/%s/%s" % (validate_host, factory_id, app_type)
        validate_json = get_data(validate_url)

        result = validate_json['result']
        logger.info("validate result: %s" % result)

        if result is False:
            error_message = 'validate failure: %s ' % validate_json['message']
            logger.error(LoggerErrorEnum.VALIDATE_FAILURE, error_message)
            raise Exception()

    def check_sign_cert_app(self, codesign_host, factory_id, envtarget):
        """
        通过调用iOS签名证书服务API校验应用iOS签名证书
        :param codesign_host: iOS签名证书服务
        :param app_id: 应用ID
        :param package_name: 应用包名
        :return:
        """
        sign_cert_url = "%s/v0.1/ios/codesign/%s/verify" % (codesign_host, factory_id)

        sign_cert_json = get_data_with_env_headers(sign_cert_url, envtarget)

        result = sign_cert_json['message']
        logger.info("check sign cert result: %s" % result)

    def check_sign_cert(self, codesign_host, package_name, envtarget):
        """
        通过调用iOS签名证书服务API校验应用iOS签名证书
        :param codesign_host: iOS签名证书服务
        :param app_id: 应用ID
        :param package_name: 应用包名
        :return:
        """
        sign_cert_url = "%s/v0.1/ios/codesign/debug/%s/verify" % (codesign_host, package_name)

        sign_cert_json = get_data_with_env_headers(sign_cert_url, envtarget)

        result = sign_cert_json['message']
        logger.info("check sign cert result: %s" % result)