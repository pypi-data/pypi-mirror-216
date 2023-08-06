#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.app_init.app_init import main

#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = '17a78f18-d6d5-4829-9c6a-5f5712887444'
    variable_dict.envtarget = 'prod-eduyun'
    variable_dict.appType = 'android'
    variable_dict.versionId = '5e8585d5adbc8bda1650de6a'
    variable_dict.envJenkins = 8
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"
    variable_dict.isLightApp = "false"
    variable_dict.resourceCacheSwitch = "true"

    return variable_dict

def getparam2():
    variable_dict = ArgDict()
    variable_dict.factoryId = '653b1f55-adef-41ad-97b4-c500c13b9415'
    variable_dict.envtarget = 'preproduction'
    variable_dict.appType = 'android'
    variable_dict.versionId = '5f62fe153da2ce00106b232c'
    variable_dict.envJenkins = 8
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"
    variable_dict.isLightApp = "false"
    variable_dict.resourceCacheSwitch = "true"

    return variable_dict

def getparam3():
    # A_I_F  构建流程
    variable_dict = ArgDict()
    variable_dict.appType = 'ios'
    variable_dict.versionId = '5fc590f2a79c640011677e7e'
    variable_dict.force = 0
    variable_dict.envtarget = 'product'
    variable_dict.factoryId = '1e418860-26b0-44f3-827d-e14f5e01474a'
    variable_dict.versionInfo = '''{"app":{"chinese_name":"智慧学伴-教师","ico_url":"http://cs.101.com/v0.1/static/cs_app_native_storage/1551930378609-ico_u6n81dq0.png","launchImg":"http://cdncs.101.com/v0.1/static/portal_app_skin/640-960.png","welcomeImg":"http://cdncs.101.com/v0.1/static/portal_app_skin/1242-2208.png","name":"slp-app-teacher","description":"开发者门户导入应用","package_name_android":"com.nd.app.factory.slp.teacher","launchImgByAndroid":"http://cdncs.101.com/v0.1/static/portal_app_skin/1080-1920-new.9.png","oid":"588c882d-4171-4ab7-aba2-05a6499cb2b1","package_name_ios":"com.slpiosteacher.nd","trial_period":30,"build_type":"production"},"version":{"publisher_id":"","app_name":"slp-app-teacher","version_white_name":[],"version_name":"1.8.6","version_desc":"1.测评优化\n2.聊天优化\n3.增加网络诊断功能","create_time":1606783218135,"oid":"5fc590f2a79c640011677e7e","app_id":"588c882d-4171-4ab7-aba2-05a6499cb2b1"}}'''
    variable_dict.callbackQueue = "app-portal-build-result-package-callback-queue"
    variable_dict.envJenkins = "5fc590f2e4b06982b90809a0"
    variable_dict.buildId = 5
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"
    variable_dict.isLightApp = "false"
    variable_dict.resourceCacheSwitch = "true"

    return variable_dict
if __name__ == '__main__':
    variable_dict = getparam3()
    main(variable_dict)


