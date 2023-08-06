#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum


class LoggerErrorEnum(Enum):
    """
    Logger错误类型枚举，后续必须用 JENKINS_BUILD_ERROR_xxxxxx  定义，保证服务端能够正常匹配
    文档地址：http://reference.doc.101.com/appfactory/userguide/faq/jenkins/jenkins_error_faq.html
    """
    ## 未知错误
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    ## 下载失败
    DOWNLOAD_ERROR = 'DOWNLOAD_ERROR'
    # 缺少必要参数
    REQUIRE_ARGUMENT = 'REQUIRE_ARGUMENT'
    # 非法返回数据
    INVALID_SERVER_RESPONSE = 'INVALID_SERVER_RESPONSE'
    # 无效参数(格式不对,长度过长或过短等)
    INVALID_ARGUMENT = 'INVALID_ARGUMENT'
    # 文件不存在
    FILE_NOT_EXIST = 'FILE_NOT_EXIST'
    # 文件已存在
    FILE_ALREADY_EXIST = 'FILE_ALREADY_EXIST'
    # 校验失败
    VALIDATE_FAILURE = 'VALIDATE_FAILURE'
    # 超时
    TIME_OUT = 'TIME_OUT'
    # 网络连接异常
    NETWORK_CONNECT_LOST = 'NETWORK_CONNECT_LOST'

    # ------------------未知错误类似系列报错 000xxx------------------------
    # 测试用错误类型
    JENKINS_BUILD_ERROR_999999 = 'JENKINS_BUILD_ERROR_999999'

    JENKINS_BUILD_ERROR_000001 = 'JENKINS_BUILD_ERROR_000001'

    JENKINS_BUILD_ERROR_00002 = 'JENKINS_BUILD_ERROR_000002'

    # ------------------无效参数系列报错 001xxx------------------------

    JENKINS_BUILD_ERROR_001001 = 'JENKINS_BUILD_ERROR_001001'

    JENKINS_BUILD_ERROR_001002 = 'JENKINS_BUILD_ERROR_001002'

     # ------------------非法返回数据 002xxx------------------------

    JENKINS_BUILD_ERROR_002001 = 'JENKINS_BUILD_ERROR_002001'


    # ------------------非法返回数据 003xxx------------------------

    JENKINS_BUILD_ERROR_003001 = 'JENKINS_BUILD_ERROR_003001'

  # ------------------缺少必要参数系列报错 001xxx------------------------

    JENKINS_BUILD_ERROR_004001 = 'JENKINS_BUILD_ERROR_004001'
