#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.rn_widget.rn_widget import init_rn_widget

#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = '9f5b8d70-8b01-427f-b696-6e80095431d2'
    variable_dict.appType = 'ios'
    variable_dict.envtarget = 'preproduction'
    variable_dict.envJenkins = 8
    variable_dict.buildToolVersion = ""
    variable_dict.commitId = ""
    variable_dict.isDev = ""
    variable_dict.resetCache = "false"
    variable_dict.isLocal = "true"
    return variable_dict


if __name__ == '__main__':
    variable_dict = getparam()
    init_rn_widget(variable_dict)

