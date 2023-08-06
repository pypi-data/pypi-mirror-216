#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
React Native组件本地调试工具
"""

__author__ = 'LianGuoQing'
import argparse
from apf_ci.init.init_global_variable_service import main as init_variable
from apf_ci.config.app_config import main as init_app_config
from apf_ci.resource.skin import SkinResource
from apf_ci.resource.language import LanguageResource
from apf_ci.lite_app.rn.component import ReactLocalBuilder
from apf_ci.lite_app.rn.builder.react_builder import *
from apf_ci.app_init.utils.build_config_utils import *
from apf_ci.app_init.utils.variables_script_utils import *


def init_rn(args):
    """
    执行RN组件本地调试构建工具 / React_Builder 轻应用构建插件
    :param args:
    :return:
    """
    factory_id = args.factoryId
    envtarget = args.envtarget
    app_type = args.appType
    env_jenkins = args.envJenkins
    build_tool_version = args.buildToolVersion
    commit_id = args.commitId
    is_dev = args.isDev
    reset_cache = args.resetCache

    #是否本地构建
    is_local = args.isLocal == "true"

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')
    logger.debug(" is_local : %s" % is_local)
    if is_local:
        build_tool = ''
        git_repository = 'git@git.sdp.nd:app-factory/react-native-main-module.git'
        # 初始化全局变量
        init_variable_args = argparse.Namespace()
        init_variable_args.factoryId = factory_id
        init_variable_args.envtarget = envtarget
        init_variable_args.appType = app_type
        init_variable_args.envJenkins = env_jenkins
        init_variable_args.versionId = ''
        init_variable_args.isLocal = is_local
        init_variable_args.version2AppFactory = ''
        init_variable(init_variable_args)

        # 初始化应用配置
        init_app_config_args = argparse.Namespace()
        init_app_config_args.isLocal = 'true'
        init_app_config_args.isLightApp = 'true'
        init_app_config_args.envJenkins = env_jenkins
        init_app_config(init_app_config_args)

        # 从variables.json文件中获取全局变量集合
        variables_path = os.path.join(target_path, 'variables.json')
        variables_data = read_file_content(variables_path)
        variables_json = json.loads(variables_data)

        build_config = BuildConfig(target_path)
        build_config_json = build_config.read_build_config()

        storage_host = variables_json['app_native_storage']
        biz_mng_host = variables_json['biz_component_mng']

        # 从variables_script.json文件中/组件定义中,获取构建脚本的配置
        variables_script_json = None
        target_variable_scriot_path = os.path.join(target_path, 'variables_script.json')
        if os.path.exists(target_variable_scriot_path):
            # 从variables_script.json文件中,获取构建脚本的配置
            variables_script_data = read_file_content(target_variable_scriot_path)
            variables_script_json = json.loads(variables_script_data)

        if build_tool_version:
            build_tool = '@sdp.nd/react-native-component-builder@%s' % build_tool_version

        if commit_id == '' and build_tool == '':
            if variables_script_json is not None:
                git_repository = variables_script_json['react_git']
                commit_id = variables_script_json['react_git_commitid']
                build_tool = variables_script_json['react_build_tool']
            else:
                # 从应用的组件定义中, 获取构建脚本的配置
                template_service = TemplateService(os.path.join(workspace_path), storage_host, biz_mng_host, factory_id)
                git_repository, commit_id, build_tool = template_service.get_variables_script_template('react')

        if commit_id == '' and build_tool == '':
            template_service = TemplateService(target_path, storage_host, biz_mng_host, factory_id)
            git_repository, commit_id, build_tool = template_service.get_template('react')

            if is_dev == '':
                assemble_mode = get_assemble_mode(app_factory_path)
                if assemble_mode == '':
                    assemble_mode = get_environment_name(build_config_json, envtarget)

                if assemble_mode.lower() == 'debug':
                    is_dev = 'true'
                else:
                    is_dev = 'false'

        # 获取react皮肤资源
        skin_resource = SkinResource(target_path, variables_json)
        skin_resources_array = skin_resource.get_skin_resources('react')
        skin_resource.download_skin(skin_resources_array, 'react')

        # 获取react国际化资源
        language_resource = LanguageResource(target_path, variables_json)
        download_language_array = language_resource.get_language_resources('react')
        for language_name in download_language_array:
            language_resources_array = download_language_array[language_name]
            language_resource.download_language(app_type, language_name, language_resources_array, 'react',
                                                language_temp_path=None)

        # 生成构建所需的appLanguageInfo.json文件
        app_language_info = variables_json['app_language_array']
        app_language_info_path = os.path.join(target_path, 'react', 'config', 'appLanguageInfo.json')
        write_content_to_file(app_language_info_path, json.dumps(app_language_info, ensure_ascii=False))

        # 解析是否含有RN组件
        react_builder = ReactLocalBuilder(app_factory_path, target_path, app_type.lower())
        is_build = react_builder.parse_components()
        if is_build:
            # 存在则执行npm相关构建
            react_path = os.path.join(target_path, 'react')
            os.chdir(react_path)
            react_builder.execute_build(build_tool, git_repository, commit_id, is_dev, reset_cache)
    else:
        variable_script = VariableScript(target_path)
        variable_script_json = variable_script.read_variable_json()
        js_build_tool_version = ''
        if 'js-build-tool-version' in variable_script_json :
            js_build_tool_version = variable_script_json['js-build-tool-version']

        if not js_build_tool_version == '':
            git_repository = os.getenv("reactTemplateUrl", "")
            commit_id = os.getenv("reactCommitId", "")
            build_tool = os.getenv("reactBuildTool", "")
            react_builder = ReactBuilder(git_repository, commit_id, build_tool)
            react_builder.perform(is_local)
        else:
            logger.warning('应用不包含react支持组件，不进行react构建')



def get_assemble_mode(app_factory_path):
    """
    从config.json文件获取assemble_mode属性值
    :param app_factory_path: 路径值/app/assets/app_factory
    :return:
    """
    config_path = os.path.join(app_factory_path, 'app', 'config.json')
    config_data = read_file_content(config_path)
    config_json = json.loads(config_data)

    assemble_mode = config_json['assemble_mode']
    return assemble_mode