#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.app_init.app_config import main
from  apf_ci.app_init.utils import *
#  用于本地测试脚本，这里用于备份，不在这里运行，因为子应用配置会删除文件夹下所有文件
class ArgDict():
    pass


def getparam():
    variable_dict = ArgDict()
    variable_dict.factoryId = 'e87f84f6-4a53-411f-92c6-8ba69cbff214'
    variable_dict.envtarget = 'development'
    variable_dict.appType = 'android'
    variable_dict.versionId = '5c9c5f1927686b9b59aeeb80'
    variable_dict.envJenkins = 5
    variable_dict.gitTemplate = ""
    variable_dict.commitId = ""
    variable_dict.version2AppFactory = ""
    variable_dict.isLocal = "true"

    return variable_dict


if __name__ == '__main__':
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    variable = Variable(target_path)
    variable_dict = variable.read_variable_json()
    main(variable_dict)


