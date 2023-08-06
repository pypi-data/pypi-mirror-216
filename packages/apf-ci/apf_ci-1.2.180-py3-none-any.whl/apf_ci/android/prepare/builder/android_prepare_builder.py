#!/usr/bin/python3
# -*- coding: utf-8 -*-



from apf_ci.util.hook_service import *
from apf_ci.android.prepare.builder.generate_dependency_builder import *
from apf_ci.android.prepare.builder.android_injections_builder import *
from apf_ci.app_res.app_res import main as app_res
from apf_ci.util.routes_to_json import RouteToJson

class AndroidPrepareBuilder:
    '''
     android 初始化准备
    '''

    def __init__(self):
        pass

    def perform(self, args):
        is_local = args.isLocal == "true"

        workspace = os.getcwd()
        # 取全局变量
        variables_path = os.path.join(workspace, "target", "variables.json")
        variables_content = read_file_content(variables_path)
        variables_dict = json.loads(variables_content)
        app_type = variables_dict["build_app_type"]
        gradle_home = variables_dict["gradleHome"]
        hook_service = HookService(app_type)
        hook_service.hook('pre_android_prepare', gradle_home, is_local)

        app_res()
        factory_id = variables_dict["factoryId"]

        # do generate dependency
        generate_dependency_builder = GenerateDependencyBuilder(factory_id, variables_dict)
        generate_dependency_builder.perform()

        # 添加生成app/routes.json
        reoutes_to_json_builder = RouteToJson()
        reoutes_to_json_builder.perform()

        android_injections_builder = AndroidInjectionsBuilder(app_type)
        android_injections_builder.perform(variables_dict)
        return hook_service.hook('post_android_prepare', gradle_home, is_local)
