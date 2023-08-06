#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
React Native颗粒本地调试工具
"""

__author__ = 'LianGuoQing'

import argparse
from apf_ci.init.init_global_variable_service import main as init_variable
from apf_ci.config.app_config import main as init_app_config
from apf_ci.resource.skin import SkinResource
from apf_ci.resource.language import LanguageResource
from apf_ci.rn_widget.widget import ReactWidgetLocalBuilder
from apf_ci.rn_widget.builder.react_widget_builder import *
from apf_ci.app_init.utils.variables_script_utils import *


def init_rn_widget(args):
    """
    执行RN颗粒本地调试构建工具
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

    # 是否本地构建
    is_local = args.isLocal == "true"
    build_tool = ''
    git_repository = 'git@git.sdp.nd:app-factory/react-native-main-template.git'

    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')

    if is_local:
        # 初始化全局变量
        init_variable_args = argparse.Namespace()
        init_variable_args.factoryId = factory_id
        init_variable_args.envtarget = envtarget
        init_variable_args.appType = app_type
        init_variable_args.envJenkins = env_jenkins
        init_variable_args.versionId = ''
        init_variable_args.isLocal = 'true'
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
            build_tool = '@sdp.nd/react-native-widget-builder@%s' % build_tool_version

        if commit_id == '' and build_tool == '':
            if variables_script_json is not None:
                git_repository = variables_script_json['react-widget_git']
                commit_id = variables_script_json['react-widget_git_commitid']
                build_tool = variables_script_json['react-widget_build_tool']
            else:
                # 从应用的组件定义中, 获取构建脚本的配置
                template_service = TemplateService(os.path.join(workspace_path), storage_host, biz_mng_host, factory_id)
                git_repository, commit_id, build_tool = template_service.get_variables_script_template('react-widget')

        if commit_id == '' and build_tool == '':
            template_service = TemplateService(target_path, storage_host, biz_mng_host, factory_id)
            git_repository, commit_id, build_tool = template_service.get_template('react-widget')

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
        app_language_info_path = os.path.join(target_path, 'react_widget', 'config', 'appLanguageInfo.json')
        write_content_to_file(app_language_info_path, json.dumps(app_language_info, ensure_ascii=False))

        # 解析是否含有RN颗粒
        default_language = variables_json['defaultLang']
        lifecycle_host = variables_json['lifecycle_manage']
        react_widget_builder = ReactWidgetLocalBuilder(app_factory_path, target_path, app_type.lower(),
                                                       default_language, lifecycle_host)
        is_build = react_widget_builder.analysis_pages()
        if is_build:
            # 存在则执行npm相关构建
            # react_path = os.path.join(target_path, 'react_widget')
            # os.chdir(react_path)
            # react_widget_builder.execute_build(build_tool, git_repository, commit_id, is_dev, reset_cache)
            pages_info_path = os.path.join(target_path, 'react_widget', 'config', 'pagesInfo.json')
            pages_info_data = read_file_content(pages_info_path)
            pages_info_json = json.loads(pages_info_data)
            for each_plugin_info in pages_info_json:
                react_path = os.path.join(target_path, 'react_widget')
                if not os.path.exists(react_path):
                    os.makedirs(react_path)
                os.chdir(react_path)
                react_widget_builder.execute_build(build_tool, git_repository, commit_id, is_dev, reset_cache,
                                                   each_plugin_info)
    else:
        try:
            variable_script = VariableScript(target_path)
            variable_script_json = variable_script.read_variable_json()
            js_build_tool_version = ''
            if 'js-build-tool-version' in variable_script_json:
                js_build_tool_version = variable_script_json['js-build-tool-version']

            if js_build_tool_version == '':
                logger.warning('应用不包含react支持组件，不进行rn颗粒构建')
            else:
                git_repository = os.getenv("reactWidgetTemplateUrl", "")
                commit_id = os.getenv("reactWidgetCommitId", "")
                build_tool = os.getenv("reactWidgetBuildTool", "")
                react_widget_builder = ReactWidgetBuilder(git_repository, commit_id, build_tool)

                variables_path = os.path.join(target_path, 'variables.json')
                variables_data = read_file_content(variables_path)
                variables_json = json.loads(variables_data)
                react_widget_builder.perform(variables_json, is_local)
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)


def get_assemble_mode(app_factory_path):
    """
    从config.json文件获取assemble_mode属性值
    :param app_factory_path: 路径值/app/assets/app_factory
    :return:
    """
    config_path = os.path.join(app_factory_path, 'app', 'config.json')
    config_data = read_file_content(config_path)
    config_json = json.loads(config_data)

    assemble_mode = config_json.get("assemble_mode", "")
    return assemble_mode