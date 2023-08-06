#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
子应用配置初始化业务处理模块
"""

__author__ = '370418'

from  apf_ci.app_init.update_variable_json import *
from apf_ci.init.git_template_service import *
from apf_ci.util.file_utils import *
from apf_ci.app_init.app_config import main as app_config
from apf_ci.app_init.app_resource import main as app_resource
from apf_ci.app_res.app_res import main as app_res


def main(args):
    #----  获取传入参数
    factory_id = args.factoryId
    envtarget = args.envtarget
    app_type = args.appType
    version_id = args.versionId
    env_jenkins = args.envJenkins
    version_code = "componentDeploy"
    app_version_id = args.appVersionId
    com_test_type = args.comTestType
    app_name = args.appName
    is_local = args.isLocal == 'true'
    component_type = ''
    is_send = ''

    is_light_app = False
    cache_switch = False

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
    variable_dict['versionId'] = version_id
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
        #logger.info(' variables_script.json existed')
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
    factory_app_type = "sub"
    logger.info('--------------子应用和主应用相应信息--------------')
    app_info_url = "%s/v0.8/appinfo/%s" % (storage_host, factory_id)
    logger.debug(' 获取应用的统一信息，url = %s' % app_info_url)
    app_info_json = get_data(app_info_url)
    logger.debug(' 获取应用的统一信息，result = %s' % app_info_json)

    parent_id = app_info_json['parent_id']
    parent_app_info_url = "%s/v0.8/appinfo/%s" % (storage_host, parent_id)
    logger.debug(' 获取主应用的统一信息，url = %s' % parent_app_info_url)
    parent_info_json = get_data(parent_app_info_url)
    logger.debug(' 获取主应用的统一信息，result = %s' % parent_info_json)
    main_app_mame = ''
    if app_type.lower() == 'android':
        main_app_mame = parent_info_json['package_name']
    else:
        main_app_mame = parent_info_json['package_name_ios']


    # 子应用轻应用构建配置生成
    logger.info('--------------获取轻应用构建配置--------------')
    #biz_mng_host = variable_dict['biz_component_mng']
    #script_build = update_variables_script(storage_host, biz_mng_host, parent_info_json)
    #script_json = json.dumps(script_build)
    #write_content_to_file(os.path.join(target_path, 'variables_script.json'), script_json)
    #logger.info('保存到/target/variables_script.json文件中')

    variable_dict["isWriteAnnounceFile"] = 'false'
    variable_dict["build_app_name"] = app_name
    variable_dict["build_version_label"] = app_version_id
    variable_dict["build_app_type"] = app_type
    variable_dict["build_app_version"] = build_app_version
    variable_dict["build_package"] = main_app_mame
    variable_dict["subVersionCode"] = variable_dict["build_version_code"]
    variable_dict["build_version_code"] = version_code
    variable_dict["build_component_type"] = component_type
    variable_dict["factoryAppType"] = factory_app_type
    variable_dict["comTestType"] = com_test_type
    # 这个gradleHome 参数值暂时没有意义，在后续hook构建会读取
    variable_dict["gradleHome"] = ''
    #---- validate


    #---- download git template

    #---- target/variables_script.json

    #  这块内容是从java代码迁移过来，从代码逻辑判断，属于冗余代码，暂且保留，后期看下要不要移除
    logger.info(" 否发送到轻应用服务： %s" % is_send)
    if is_send and not is_send == '':
        lite_body = {}
        lite_body['factory_id'] = factory_id
        lite_body['component_type'] = component_type
        lite_body['app_type'] = app_type
        lite_body['env_target'] = envtarget
        lite_body['build_status'] = 'BUILDING'
        lite_body['build_desc'] = '构建中'

        lite_app_url = variable_dict["lite_app_server"] + "/v0.1/widget_resources"
        # 这里要判断返回值？
        lite_json = post_for_array(lite_app_url, lite_body)

    #---- 写入target/variables.json
    #init_gradle_home(variable_dict)
    variable.write_variable_json(variable_dict)
    build_config.write_build_config(build_config_json_encrypt)
    app_info.write_app_info(app_json)
    if variables_script_json is not None:
        logger.info(' variables_script_json is not null and write into file again')
        write_content_to_file(target_variable_scriot_path, json.dumps(variables_script_json, ensure_ascii=False))

    #------------  旧的  ws_init  流程结束 ------------
    app_config(variable_dict)
    app_resource(variable_dict)
    app_res()
