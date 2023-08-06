#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.h5_grain_config.h5_grain_init import *
from apf_ci.app_res.app_res import main as app_res
#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam1():
    variable_dict = ArgDict()
    variable_dict.factoryId = 'd90e89dd-8e6c-4184-989d-4c6491a2d31f'
    variable_dict.appName = 'jsfun_anenfn'
    variable_dict.appType = 'android'
    variable_dict.envtarget = 'product'
    variable_dict.appVersionId = '0.0.4'
    variable_dict.componentType = 'h5'
    variable_dict.envJenkins = 8
    variable_dict.isLocal = 'true'
    variable_dict.comTestType = ''
    variable_dict.packageName = ''
    variable_dict.buildVersion = ''
    variable_dict.versionCode = ''
    variable_dict.liteAppUpdateTime = ''

    return variable_dict

def getparam2():
    variable_dict = ArgDict()
    variable_dict.factoryId = '1140bd28-c1ab-4ae2-b70a-fc9920305110'
    variable_dict.appName = 'ap1547040105369'
    variable_dict.appType = 'ios'
    variable_dict.envtarget = 'preproduction'
    variable_dict.appVersionId = '1.1'
    variable_dict.componentType = 'none'
    variable_dict.envJenkins = 5
    variable_dict.isLocal = 'true'
    variable_dict.comTestType = ''
    variable_dict.packageName = 'com.nd.sdp.component.debug.ap1547040105369'
    variable_dict.buildVersion = 'development'
    variable_dict.versionCode = 'componentDeploy'
    variable_dict.liteAppUpdateTime = '1557902095059'

    return variable_dict
#  子应用配置生成测试
def main_test():
    variable_dict = getparam1()
    main(variable_dict)

def app_res_test():
    app_res()

if __name__ == '__main__':
    app_res_test()
    #main_test()
    #subapp_config_script_test()


