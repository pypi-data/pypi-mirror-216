#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.app_init.app_init import main

#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = 'b5ee0dda-0752-4050-a8d3-5c868ffb1620'
    variable_dict.envtarget = 'preproduction'
    variable_dict.appType = 'android'
    variable_dict.versionId = '60c3269f96ea9f00112c2432'
    variable_dict.branch = "lite"
    variable_dict.bizName = "apf-ci"
    variable_dict.namespace = "com.nd.sdp.app.factory.build"
    variable_dict.envJenkins = 8
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"
    variable_dict.isLightApp = "false"
    variable_dict.resourceCacheSwitch = "true"

    return variable_dict
   # Application_Android_Factory  构建流程
def getparam2():
    variable_dict = ArgDict()
    variable_dict.factoryId = '7dfae060-3856-4632-9d26-35c80f3f7520'
    variable_dict.envtarget = 'hk'
    variable_dict.appType = 'android'
    variable_dict.versionId = '60b8b854b98c09001183ebe0'
    variable_dict.versionInfo = ''''''
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
    variable_dict.versionId = '5fc8856d6751870011d9fc3a'
    variable_dict.force = 0
    variable_dict.envtarget = 'test'
    variable_dict.factoryId = 'bb920ceb-c4c0-424b-a6bc-249a724e0735'
    variable_dict.versionInfo = '''{"app":{"chinese_name":"testforsign2","ico_url":"http://cs.101.com/v0.1/static/biz_comp_mng/default-icon/icon.png","launchImg":"http://gcdncs.101.com/v0.1/static/portal_app_skin/640-960.png","welcomeImg":"http://gcdncs.101.com/v0.1/static/portal_app_skin/1242-2208.png","name":"ap1591349307097","package_name_android":"com.nd.app.factory.testforsign2","launchImgByAndroid":"http://gcdncs.101.com/v0.1/static/portal_app_skin/1080-1920-new.9.png","oid":"6e508e37-c5ee-4854-ba6d-ac4b7382631e","package_name_ios":"com.nd.app.factory.testforsign2","trial_period":30,"build_type":"production"},"version":{"publisher_id":"","app_name":"ap1591349307097","version_white_name":[],"version_name":"1203","version_desc":"123","create_time":1606976876867,"oid":"5fc8856d6751870011d9fc3a","app_id":"6e508e37-c5ee-4854-ba6d-ac4b7382631e"}}'''
    variable_dict.callbackQueue = "app-portal-build-result-package-callback-queue"
    variable_dict.envJenkins = 2
    variable_dict.buildId = '5fc8856de4b09eb0d3c5b6cd'
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"
    variable_dict.isLightApp = "false"
    variable_dict.resourceCacheSwitch = "true"

    return variable_dict
if __name__ == '__main__':
    variable_dict = getparam()
    main(variable_dict)


