#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.tab.build.tab_init import main as tab_init
from apf_ci.tab.build.tab_build import main as tab_build

#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = '448d7412-23ac-4ffe-baee-ad05c749a4c6'
    variable_dict.envtarget = 'test'
    variable_dict.appType = 'android'
    variable_dict.versionCode = '100'
    variable_dict.versionName = "test"
    variable_dict.versionDesc = "测试"
    variable_dict.envJenkins = 2
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.isLocal = "true"
    variable_dict.appVersionId = "5e8bf640ff49c400100cce67"

    return variable_dict

def getparam2():
    variable_dict = ArgDict()
    variable_dict.factoryId = 'ecda9465-461f-43fa-b863-760e46203638'
    variable_dict.envtarget = 'development'
    variable_dict.appName = 'ap1577154284902'
    variable_dict.appType = 'android'
    variable_dict.versionCode = '3355970'
    variable_dict.versionName = "0.0.4"
    variable_dict.versionDesc = "0.0.4"
    variable_dict.envJenkins = 2
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.isLocal = "true"
    variable_dict.appVersionId = "5ea8298f857b360010465942"
    variable_dict.tabVersionId = "5ea8f3fc857b3600104659cf"
    variable_dict.packageName = "com.nd.app.factory.ap1577154284902"

    return variable_dict
if __name__ == '__main__':
    variable_dict = getparam2()
    tab_init(variable_dict)
    #tab_build()


