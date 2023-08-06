#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
构建空间初始化业务处理模块--轻应用
"""

__author__ = '370418'

from  apf_ci.app_init.update_variable_json import *
from apf_ci.util.file_utils import *
from apf_ci.app_init.app_config import main as app_config
from apf_ci.app_init.app_resource import main as app_resource
from apf_ci.app_res.app_res import main as app_res
from apf_ci.util.parse_utils import parse_str_to_int

def main(args):
    #----  获取传入参数
    factory_id = args.factoryId
    envtarget = args.envtarget
    app_type = args.appType
    env_jenkins = args.envJenkins
    com_test_type = args.comTestType
    app_name = args.appName
    is_local = args.isLocal == 'true'
    is_light_app = False
    cache_switch = False
    component_type = get_true_param(args.componentType)
    app_version_id = get_true_param(args.appVersionId)
    package_name = get_true_param(args.packageName)
    version_code = get_true_param(args.versionCode)
    build_app_version = get_true_param(args.buildVersion)
    update_time = get_true_param(args.liteAppUpdateTime)

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    #if not os.path.exists(target_path):
    #    os.makedirs(target_path)

    #----   初始化传入参数及路径
    variable_dict = {}
    # 非主应用打包，is_app都为False
    variable_dict['is_app'] = False
    variable_dict['factoryId'] = factory_id
    variable_dict['envtarget'] = envtarget
    variable_dict['build_app_type'] = app_type
    variable_dict['envJenkins'] = env_jenkins
    variable_dict['is_local'] = is_local
    variable_dict['is_light_app'] = is_light_app
    variable_dict['cache_switch'] = cache_switch

    variable_dict['workspace_path'] = workspace_path
    variable_dict['target_path'] = target_path



    #---- target/variables_script.json 读取，必须在清除工作空间之前执行
    variables_script_json = None
    target_variable_scriot_path = os.path.join(target_path, 'variables_script.json')
    if os.path.exists(target_variable_scriot_path):
        #logger.debug(' variables_script.json existed')
        variables_script_data = read_file_content(target_variable_scriot_path)
        variables_script_json = json.loads(variables_script_data)

    #logger.info(' clean workspace start')
    clean_dir(workspace_path)
    logger.info(' clean workspace end')

    #----  下载target/build_config.json
    #utils(variable_dict)
    build_config = BuildConfig(target_path)
    build_config_json_encrypt = build_config.get_build_config(variable_dict['envJenkins'], variable_dict['is_local'])
    build_config_json = build_config.decrypy_build_config(build_config_json_encrypt)

    #----  初始化 target/variables.json
    variable = Variable(target_path)
    variable.init_variable_json(variable_dict, build_config_json)
    #update_variable_json(variable_dict)

    #----  初始化 target/app_info.json
    storage_host = variable_dict['app_native_storage']
    app_info = Apps(target_path)
    app_json = app_info.get_app_info(storage_host, factory_id)
    build_app_version = app_json['version']
    logger.debug(' 构建应用版本：%s' % build_app_version)


    # 轻应用构建配置生成

    # 这个factory_app_type 参数值暂时没有意义，在后续react构建会读取
    factory_app_type = 'h5'
    variable_dict["isWriteAnnounceFile"] = 'false'
    variable_dict["build_app_name"] = app_name
    variable_dict["build_version_label"] = app_version_id
    variable_dict["build_app_type"] = app_type
    variable_dict["build_app_version"] = build_app_version
    variable_dict["build_package"] = package_name
    variable_dict["build_version_code"] = version_code
    variable_dict["build_component_type"] = component_type
    variable_dict["factoryAppType"] = factory_app_type
    variable_dict["comTestType"] = com_test_type
    # 这个gradleHome 参数值暂时没有意义，在后续hook构建会读取
    variable_dict["gradleHome"] = ''
    if not update_time == '':
        variable_dict['lite_app_update_time'] = parse_str_to_int(update_time)
    variable_dict['liteAppUpdateTime'] = variable_dict['lite_app_update_time']
    #---- validate


    #---- download git template

    #---- target/variables_script.json

    #---- 写入target/variables.json
    variable.write_variable_json(variable_dict)
    build_config.write_build_config(build_config_json_encrypt)
    app_info.write_app_info(app_json)
    if variables_script_json is not None:
        logger.debug(' variables_script_json is not null and write into file again')
        write_content_to_file(target_variable_scriot_path, json.dumps(variables_script_json, ensure_ascii=False))
    #------------  旧的  ws_init  流程结束 ------------
    app_config(variable_dict)
    app_resource(variable_dict)
    app_res()

def get_true_param(param):
    """
    按照约定，当参数为none 替换为 ‘’值
    """
    if param.lower() == 'none':
        return ''
    return param