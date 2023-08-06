#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.app_component_compare.build.app_component_compare import main as app_component_compare

#  用于本地测试脚本，这里用于备份，不在这里运行，因为初始化文件夹下所有文件
class ArgDict():
    pass



def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = '6f43ae45-0c7f-4a0f-9a1e-a725ce9e991c'
    variable_dict.appId = ''
    variable_dict.compareId = "5ea8298f857b360010465942"
    variable_dict.versionFrom = "release"
    variable_dict.versionTo = "stable"
    variable_dict.envJenkins = 8
    variable_dict.appType = "android"
    variable_dict.isLocal = "true"
    return variable_dict


def getparam2():
    variable_dict = ArgDict()
    variable_dict.factoryId = 'b5480464-171d-48b8-ab20-3763a0f7624a'
    variable_dict.appId = 'c9d2485c-37f7-4a48-9893-3db627dd416f'
    variable_dict.compareId = "5ea8298f857b360010465942"
    variable_dict.versionFrom = "release"
    variable_dict.versionTo = "stable"
    variable_dict.envJenkins = 2
    variable_dict.appType = "android"
    variable_dict.isLocal = "true"

    return variable_dict
if __name__ == '__main__':
    variable_dict = getparam2()
    app_component_compare(variable_dict)
    #tab_build()


