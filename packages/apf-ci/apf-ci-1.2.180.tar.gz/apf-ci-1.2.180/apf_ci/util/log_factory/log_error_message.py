#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json


class LogErrorMessage:
    '''
    用于提供更加详细的错误情况给服务端分析，暂时保留代码，不接入使用
    '''
    CONTACT_APPFACTORY = "应用快速集成受理号(10005015)"
    CONTACT_ANDROID = "苏昌骏(606198)"
    CONTACT_IOS = "颜志炜(734819)"
    CONTACT_REACT = "蔡睦堃(505459)"
    CONTACT_PLUGIN = "管培源(370418)"

    def __init__(self):
        # 异常关键字
        self.fingerprint = ""
        # 具体的原因
        self.reason = ""
        # 问题分类（比如外部/内部）
        self.questionClassify = ""
        # 解决方案连接地址
        self.resolve = ""
        # 可联系人(99u)
        self.contact = self.CONTACT_APPFACTORY
        # 原始异常消息，主要是堆栈（设为空）
        self.original = ""
        # 是否匹配正则，python脚本这都默认为False
        self.matcherRegular = False
        # 服务分类（比如应用工厂-jenkins）
        self.category = "应用工厂-jenkins-python脚本"


    def set_message(self, fingerprint, reason):
        pass


    def __str__(self):
        return json.dumps(obj=self.__dict__, ensure_ascii=False)
