#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
构建空间初始化业务处理模块
"""

__author__ = '370418'

from  apf_ci.app_init.update_variable_json import *
from apf_ci.init.validate_service import ValidateService
from apf_ci.init.git_template_service import *
from apf_ci.util.file_utils import *
from apf_ci.app_init.app_config import main as app_config
from apf_ci.app_init.app_resource import main as app_resource


def main(args):
    #----  获取传入参数
    factory_id = args.factoryId
    envtarget = args.envtarget
    app_type = args.appType
    version_id = args.versionId
    env_jenkins = args.envJenkins
    git_template = args.gitTemplate
    commit_id = args.commitId
    version2_app_factory = args.version2AppFactory
    is_local = args.isLocal == 'true'
    is_light_app = args.isLightApp == 'true'
    cache_switch = args.resourceCacheSwitch == 'true'

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    #if not os.path.exists(target_path):
    #    os.makedirs(target_path)

    #----   初始化传入参数及路径
    variable_dict = {}
    variable_dict['is_app'] = True
    variable_dict['factoryId'] = factory_id
    variable_dict['envtarget'] = envtarget
    variable_dict['build_app_type'] = app_type
    variable_dict['versionId'] = version_id
    variable_dict['envJenkins'] = env_jenkins
    variable_dict['version2AppFactory'] = version2_app_factory

    variable_dict['git_template'] = git_template
    variable_dict['commit_id'] = commit_id
    variable_dict['is_local'] = is_local
    #variable_dict['versionInfo'] = versionInfo
    variable_dict['is_light_app'] = is_light_app
    variable_dict['cache_switch'] = cache_switch

    variable_dict['workspace_path'] = workspace_path
    variable_dict['target_path'] = target_path

    # 针对 git  clone 需要空目录才能正常，日志文件生成延后到，clone步骤之后
    logger.delay_init(True)
    #---- target/variables_script.json 读取，必须在清除工作空间之前执行
    variables_script_json = None
    target_variable_scriot_path = os.path.join(target_path, 'variables_script.json')
    if os.path.exists(target_variable_scriot_path):
        logger.info(' variables_script.json existed')
        variables_script_data = read_file_content(target_variable_scriot_path)
        variables_script_json = json.loads(variables_script_data)

    # ---- python_install.sh 读取，必须在清除工作空间之前执行
    python_install_content = ''
    target_python_install_path = os.path.join(target_path, 'python_install.sh')
    if os.path.exists(target_python_install_path):
        python_install_content = read_file_content(target_python_install_path)

    logger.info(' clean workspace start')
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
    update_variable_json(variable_dict)

    #----  初始化 target/app.json
    storage_host = variable_dict['app_native_storage']
    apps_single = Apps(target_path)
    app_json = apps_single.get_app_info(storage_host, factory_id)

    validate_host = variable_dict['app_factory_validate']
    sign_cert_host = variable_dict['codesign']
    build_app_id = variable_dict['build_app_id']
    build_package = variable_dict['build_package']
    #---- validate
    validate_service = ValidateService()
    validate_service.check_project(validate_host, factory_id, app_type)
    if app_type.lower() == 'ios':
        version_info = get_versionInfo(env_jenkins, is_local)
        logger.debug(" versionInfo: %s" % version_info)
        # 通过有无 version_info 参数来判断是 应用构建 还是功能/集成测试
        if version_info == '':# 功能/集成测试
            validate_service.check_sign_cert(sign_cert_host, build_package, envtarget)
        else: # 应用构建
            validate_service.check_sign_cert_app(sign_cert_host, factory_id, envtarget)


    #---- download git template
    apf_ci_biz_version = variables_script_json['apf-ci-version']
    git_template_service = GitTemplateService(git_template, commit_id)
    git_templates = git_template_service.get_git_template_info(storage_host, factory_id, app_type, apf_ci_biz_version)
    git_template_service.clone_template()

    # 写入 target/git_templates.json
    if git_templates:
        git_templates_path = os.path.join(target_path, 'git_templates.json')
        write_content_to_file(git_templates_path, json.dumps(git_templates))


    logger.delay_init(False)
    logger.info('由于git clone 需要空目录，延迟初始化日志文件')
    logger.info('注意！！！后续大部分调试日志将不再打印出来！！！如有需要，请查看工作空间下jenkins_build_debug.log文件！！！')
    #---- 写入target/variables.json

    init_gradle_home(variable_dict)
    variable.write_variable_json(variable_dict)
    build_config.write_build_config(build_config_json_encrypt)
    apps_single.write_app_info(app_json)
    app_info = AppInfo(target_path)
    app_info_json = app_info.get_app_info(storage_host, factory_id)
    app_info.write_app_info(app_info_json)
    if variables_script_json is not None:
        logger.info(' variables_script_json is not null and write into file again')
        write_content_to_file(target_variable_scriot_path, json.dumps(variables_script_json, ensure_ascii=False))
        #------------  旧的  ws_init  流程结束 ------------
    app_config(variable_dict)
    app_resource(variable_dict)

    # ---- 写入target/python_install.sh
    if len(python_install_content) > 0:
        write_content_to_file(target_python_install_path, python_install_content)
