#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.cache.factor.react_cache_factor import *
from apf_ci.lite_app.model.template_bo import *
from apf_ci.lite_app.parser.react_parser import *
from apf_ci.lite_app.concurrent.concurrent_build_client import *
from apf_ci.lite_app.rn.template import TemplateService
from apf_ci.util.jenkins_utils import *
from apf_ci.util.property import *
from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
import datetime

class ReactBuilder:
    def __init__(self, git_repository, commit_id, build_tool):
        self.git_repository = git_repository
        self.commit_id = commit_id
        self.build_tool = build_tool

    def perform(self, is_local):
        """
        react轻应用构建插件
        :return:
        """
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, 'target')
        # 从variables.json文件中获取全局变量集合
        variables_path = os.path.join(target_path, 'variables.json')
        variables_data = read_file_content(variables_path)
        variables_json = json.loads(variables_data)

        param_map = self.init_parameter(variables_json)
        logger.debug(" param_map -> %s" % param_map)
        app_type = param_map["build_app_type"]

        #hook_service = HookService(app_type)
        app_type = variables_json['build_app_type']
        #gradle_home = variables_json['gradleHome']
        #hook_service.hook('pre_react_build', gradle_home, is_local)
        try:
            logger.info(" %s 开始react构建" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # 获取轻应用信息
            parser = ReactParser()
            components_json_array = parser.read_components()
            filter_json_array = parser.add_filter(os.getenv("loadComps", ""))
            parser.addParameter(param_map)
            npm_dto_list = parser.parse(filter_json_array, components_json_array, variables_json)

            cache_factor = ReactCacheFactor()
            three_level_cache = CacheFactory.get_cache(CacheEnum.THREE_LEVEL_REACT_CACHE)
            second_level_cache = CacheFactory.get_cache(CacheEnum.SECOND_LEVEL_REACT_CACHE)
            first_level_cache = CacheFactory.get_cache(CacheEnum.FIRST_LEVEL_REACT_CACHE)

            # 缓存集合
            cache_npm_dto_list = []
            # 构建集合
            build_npm_dto_list = []

            close_cache = param_map.get("closeCache")
            if close_cache == "true":
                # 关闭缓存，则全部轻应用都需要构建
                build_npm_dto_list = npm_dto_list
            else:
                for npm_dto in npm_dto_list:
                    # 获取缓存因素
                    cache_factor_bo = cache_factor.get_cache_factor(npm_dto)

                    # 获取各级缓存md5值
                    three_level_cache_md5 = three_level_cache.get_cache_md5(cache_factor_bo)
                    second_level_cache_md5 = second_level_cache.get_cache_md5(cache_factor_bo)
                    first_level_cache_md5 = first_level_cache.get_cache_md5(cache_factor_bo)

                    # 获取各级缓存
                    cache_bo = three_level_cache.get_cache(three_level_cache_md5, param_map)
                    if cache_bo is not None:
                        cache_bo.cache_level = "3"
                    else:
                        # 三级缓存不存在，则查找二级缓存
                        cache_bo = second_level_cache.get_cache(second_level_cache_md5, param_map)
                        if cache_bo is not None:
                            cache_bo.cache_level = "2"
                        else:
                            local_cache_path = "/data/jenkins/.apf"
                            if platform.system() == "Darwin":
                                 local_cache_path = "/usr/local/sdp/jenkins/.apf"
                            local_cache_path += "/"
                            local_cache_path += npm_dto.js_package_name
                            local_cache_path += "/"
                            local_cache_path += npm_dto.js_version
                            local_cache_path += "/"
                            local_cache_path += str(npm_dto.js_publish_time)
                            local_cache_path += "/"
                            local_cache_path += first_level_cache_md5
                            local_cache_path += ".zip"

                            apf_service = ApfService()
                            if apf_service.is_exist(local_cache_path):
                                cache_bo = CacheBO()
                                cache_bo.zip_url = local_cache_path
                                cache_bo.cache_level = "4"
                            else:
                                # 本地缓存不存在，则查找一级缓存
                                cache_bo = first_level_cache.get_cache(first_level_cache_md5, param_map)
                                if cache_bo is not None:
                                    cache_bo.cache_level = "1"
                                else:
                                    cache_bo = CacheBO()
                        cache_bo.three_level_cache_md5 = three_level_cache_md5
                        cache_bo.second_level_cache_md5 = second_level_cache_md5
                        cache_bo.first_level_cache_md5 = first_level_cache_md5
                    npm_dto.cache_bo = cache_bo

                    if cache_bo.cache_level != "":
                        cache_npm_dto_list.append(npm_dto)
                    else:
                        build_npm_dto_list.append(npm_dto)

            # 判断是否有需要构建的轻应用
            # 有则创建components.json文件，然后进行构建
            if len(build_npm_dto_list) > 0:
                component_json_array = []
                for build_npm_dto in build_npm_dto_list:
                    component_info = build_npm_dto.component_info
                    component_json = json.loads(component_info)
                    component_json_array.append(component_json)

                    if close_cache == "true":
                        # 获取缓存因素
                        cache_factor_bo = cache_factor.get_cache_factor(build_npm_dto)

                        # 获取各级缓存Md5值
                        three_level_cache_md5 = three_level_cache.get_cache_md5(cache_factor_bo)
                        second_level_cache_md5 = second_level_cache.get_cache_md5(cache_factor_bo)
                        first_level_cache_md5 = first_level_cache.get_cache_md5(cache_factor_bo)

                        cache_bo = CacheBO()
                        cache_bo.three_level_cache_md5 = three_level_cache_md5
                        cache_bo.second_level_cache_md5 = second_level_cache_md5
                        cache_bo.first_level_cache_md5 = first_level_cache_md5

                        build_npm_dto.cache_bo = cache_bo
                        # 放入到缓存集合中，用于后续发布操作
                    cache_npm_dto_list.append(build_npm_dto)
                self._save_components_file(component_json_array)
                self._execute_npm_build(param_map, variables_json)

            react_app_path = os.path.join(workspace_path, "app/assets/app_factory/react_app")
            if not os.path.exists(react_app_path):
                    os.mkdir(react_app_path)
            # 轻应用组件缓存数据整合
            concurrent_build_client = ConcurrentBuildClient()
            concurrent_build_client.npm_dto_list = cache_npm_dto_list
            concurrent_build_client.start("react")

            size = len(cache_npm_dto_list)
            if size > 0:
                npm_dto = cache_npm_dto_list[0]
                self._copy_base_to_app(npm_dto)
            if app_type.lower() == "android":
                react_value = "false"

                if size > 0:
                    react_value = "true"
                    # 默认开启react功能
                self._write_data_to_local_properties(react_value)
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)

        logger.info(" %s react构建结束" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #return hook_service.hook('post_react_build', gradle_home, is_local)

    def init_parameter(self, variables_json):
        paramMap = {}
        apf_service = ApfService()


        # 是否开启缓存 / 该值是用jenkins全局配置的 业务组件（react轻应用)-构建配置-缓存开关 控制
        close_cache = variables_json["react_builder_close_cache"]
        logger.info("【是否关闭缓存构建】：%s" % close_cache)

          # 这六个应该是从 config_debug(dev/release等) 文件中获取。在ws_init 初始化到variables.json
        react_builder_cs_config = ContentServiceConfig()
        react_builder_cs_config.user_id = variables_json["react_builder_cs_user_id"]
        react_builder_cs_config.host = variables_json["react_builder_cs_host"]
        react_builder_cs_config.server_name = variables_json["react_builder_cs_server_name"]
        react_builder_cs_config.session_id = variables_json["react_builder_cs_session_id"]
        react_builder_cs_config.secret_key = variables_json["react_builder_cs_secret_key"]
        react_builder_cs_config.access_key = variables_json["react_builder_cs_access_key"]

        paramMap["closeCache"] = close_cache
        paramMap["csConfig"] = react_builder_cs_config
        paramMap["templateBO"] = self.get_template(variables_json)
        paramMap["lite_app_server"] = variables_json["lite_app_server"]
        paramMap["cs_offline_host"] = variables_json["cs_offline_host"]
        paramMap["build_app_type"] = variables_json["build_app_type"]
        paramMap["envtarget"] = variables_json["envtarget"]
        paramMap["build_app_name"] = variables_json["build_app_name"]
        paramMap["factoryId"] = variables_json["factoryId"]
        paramMap["build_app_version"] = variables_json["build_app_version"]
        paramMap["lite_app_update_time"] = variables_json["lite_app_update_time"]
        paramMap["build_package"] = variables_json["build_package"]
        paramMap["build_version_code"] = variables_json["build_version_code"]
        paramMap["app_language_array"] = variables_json["app_language_array"]
        if "appVersionId" in os.environ.keys():
            app_version_id = os.environ["appVersionId"]
        else:
            app_version_id = variables_json["build_version_label"].replace(" ", "").replace(":", "")
        paramMap["appVersionId"] = app_version_id
        # 子应用
        factory_app_type = variables_json["factoryAppType"]
        is_sub_app = apf_service.is_sub_app(factory_app_type)
        paramMap["isSubApp"] = is_sub_app
        paramMap["packageName"] = os.getenv("packageName")

        return paramMap

    def get_template(self, variables_json):
        templateBO = TemplateBO()
        workspace_path = os.getcwd()
        variables_script_json = None
        target_variable_scriot_path = os.path.join(workspace_path, "target", 'variables_script.json')
        if os.path.exists(target_variable_scriot_path):
            # 从variables_script.json文件中,获取构建脚本的配置
            variables_script_data = read_file_content(target_variable_scriot_path)
            variables_script_json = json.loads(variables_script_data)

        if self.git_repository != "" and self.commit_id != "" and self.build_tool != "":
            templateBO.git_repository = self.git_repository
            templateBO.commit_id = self.commit_id
            templateBO.build_tool = self.build_tool
        else:
            if variables_script_json is not None:
                templateBO.git_repository = variables_script_json['react_git']
                templateBO.commit_id = variables_script_json['react_git_commitid']
                templateBO.build_tool = variables_script_json['react_build_tool']
            else:
                # 从应用的组件定义中, 获取构建脚本的配置
                template_service = TemplateService(os.path.join(workspace_path), None, None,
                                                   variables_json["factoryId"])
                git_repository, commit_id, build_tool = template_service.get_variables_script_template('react')

                if git_repository == "" and commit_id == "" and build_tool == "":
                    # 从git_templates.json文件中取模板信息 没有的话去 snapshot_templates.json
                    git_templates_file_path = os.path.join(workspace_path, "target", "git_templates.json")
                    if os.path.exists(git_templates_file_path):
                        git_templates = read_file_content(git_templates_file_path)
                        git_templates_json = json.loads(git_templates)
                        if "react" in git_templates_json.keys():
                            node_json = git_templates_json["react"]
                            if "git" in node_json.keys():
                                git_json = node_json["git"]
                                try:
                                    git_repository = git_json["source"]
                                    commit_id = git_json["commit-id"]
                                    build_tool = node_json["build-tool"]
                                    logger.debug(
                                        "git_templates.json的模板信息： git_repository -> %s, commit_id -> %s, build_tool -> %s" % (
                                            git_repository, commit_id, build_tool))
                                except KeyError:
                                    logger.warning(
                                        " git_json缺少source、commit-id的字段 或 react_json缺少 build-tool字段 => %s" % node_json)
                                    traceback.print_exc()

                    if git_repository != "" and git_repository != {} and commit_id != "" and commit_id != {} and build_tool != "" and build_tool != {}:
                        logger.info("xml中配置react模板source: %s, commitId: %s, build-tool: %s" % (
                            git_repository, commit_id, build_tool))
                    else:
                        snapshot_template_file_path = os.path.join(workspace_path, "target", "snapshot_template.json")
                        if os.path.exists(snapshot_template_file_path):
                            snapshot_templates = read_file_content(snapshot_template_file_path)
                            if snapshot_templates != "":
                                snapshot_templates_json_arr = json.load(snapshot_templates)
                                for object in snapshot_templates_json_arr:
                                    if isinstance(object, dict):
                                        if "type" in object.keys():
                                            type_str = object["type"]
                                            if type_str.lower() == "react":
                                                try:
                                                    git_repository = object["template"]
                                                    commit_id = object["commitId"]
                                                    build_tool = object["buildTool"]
                                                    logger.info(
                                                        "snapshot的模板信息： git_repository -> %s, commit_id -> %s, build_tool -> %s" % (
                                                            git_repository, commit_id, build_tool))
                                                except KeyError:
                                                    logger.warning(
                                                        " snapshot_templates 缺少source、commit-id、build-tool的字段  git_josn => %s" % object)

                    if git_repository != "" and commit_id != "" and build_tool != "":
                        logger.info(" snapshot中配置react模板template: %s, commitId: %s, buildTool: %s" % (
                            git_repository, commit_id, build_tool))
                    else:
                        storage_host = variables_json["app_native_storage"]
                        appTemplate_url = storage_host + "/v0.8/template/react"
                        app_template_json = get_data(appTemplate_url)

                        try:
                            git_repository = app_template_json["template"]
                            commit_id = app_template_json["commit_id"]
                            build_tool = app_template_json["build_tool"]
                            logger.info(
                                "apptemplate.json的模板信息： git_repository -> %s, commit_id -> %s, build_tool -> %s" % (
                                    git_repository, commit_id, build_tool))
                        except KeyError:
                            logger.warning(
                                " app_template缺少source、commit-id、build-tool的字段  app_template_json => %s" % app_template_json)
                            # 取到模板信息，重新封装templateBO
                templateBO.git_repository = git_repository
                templateBO.commit_id = commit_id
                templateBO.build_tool = build_tool

        env_target = variables_json["envtarget"]
        dev = variables_json["rn_debug_mode"]
        templateBO.dev = dev
        logger.debug(" %s" % templateBO.tostring_format())

        return templateBO

    def _save_components_file(self, data):
        workspace_path = os.getcwd()

        # 生成components.json文件
        components_file_path = os.path.join(workspace_path, "target/react/config/components.json")
        data_str = json.dumps(data)
        write_content_to_file(components_file_path, data_str)

    def _execute_npm_build(self, param_map, variables_json):
        npm_registry = variables_json["npm_registry"]
        is_sub_app = param_map["isSubApp"]
        app_type = param_map["build_app_type"]
        template = param_map["templateBO"]

        is_dev = template.dev
        git_repository = template.git_repository
        commit_id = template.commit_id
        build_tool = template.build_tool

        reset_cache = self._last_time_build_result()
        logger.debug("[reset_cache] %s" % reset_cache)
        workspace_path = os.getcwd()
        react_widget_path = os.path.join(workspace_path, "target/react")
        if not os.path.exists(react_widget_path):
            os.makedirs(react_widget_path)
            # 使用subprocess.call在window和linux环境下，需要做区分。
        platform_name = platform.system()
        if platform_name == 'Windows':
            logger.info(' npm config set registry="%s"' % npm_registry)
            execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=react_widget_path)
            if app_type == "android":
                # 设置npm构建缓存地址到/tmp下
                logger.info(' npm config set unsafe-perm true')
                execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'], chdir=react_widget_path)

            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            logger.info(" npm install %s" % build_tool)
            logger.debug("开始执行npm install,执行目录 %s" % os.getcwd())
            execute_command(['npm', 'install', build_tool], chdir=react_widget_path)

        else:
            logger.info(' npm config set registry="%s"' % npm_registry)
            execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=react_widget_path)
            if app_type == "android":
                # 设置npm构建缓存地址到/tmp下
                logger.info(' npm config set unsafe-perm true')
                execute_command(['npm', 'config', 'set', 'unsafe-perm', 'true'], chdir=react_widget_path)

            logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            logger.info(" npm install %s" % build_tool)
            logger.debug("开始执行npm install,执行目录 %s" % os.getcwd())
            execute_command(['npm', 'install', build_tool], chdir=react_widget_path)

        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        js_name = "node_modules/@sdp.nd/react-native-component-builder/index.js"
        logger.info('node %s --gitRepository %s --commitId %s --platform %s --dev %s --reset-cache %s' %
                    (js_name, git_repository, commit_id, app_type.lower(), is_dev, reset_cache))
        execute_command(['node', js_name,
                         '--gitRepository', git_repository,
                         '--commitId', commit_id,
                         '--platform', app_type.lower(),
                         '--dev', is_dev,
                         '--reset-cache', reset_cache], chdir=react_widget_path)

        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _last_time_build_result(self):
        """
        判断上一次rn构建是否成功
        :return: 构建成功返回false
        """
        # 使用Python获取jenkins的内置环境变量
        build_url = os.getenv("BUILD_URL")
        build_number = os.getenv("BUILD_NUMBER")
        job_name = os.getenv("JOB_NAME")
        logger.debug("build_number %s" % build_number)
        if build_number == "1":
            return "false"

        jenkins_url = build_url[0:build_url.find("/job/")]
        jenkins_url = jenkins_url + "/job/" + job_name + "/" + str(int(build_number) - 1) + "/consoleText"
        logger.debug(" jenkins_url : %s ,build_number:%s" % (jenkins_url, build_number))
        job_content = get_jenkins_job_console_text(jenkins_url)
        compare_str = "==============【ReactBuilder】步骤构建结果【成功】====="
        # 上一次成功返回false
        if compare_str in job_content:
            return "false"
        else:
            return "true"

    def _copy_base_to_app(self, npm_dto):
        module_name = npm_dto.module_name
        app_type = npm_dto.param_map.get("build_app_type", "")

        workspace_path = os.getcwd()
        react_app_path = os.path.join(workspace_path, "app/assets/app_factory/react_app")
        component_path = os.path.join(react_app_path, "base", "component")
        main_bundle_file_path = os.path.join(component_path, "main.bundle")

        if os.path.exists(main_bundle_file_path):
            module_path = os.path.join(workspace_path, "target/react", module_name)
            platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))
            base_path = os.path.join(platform_path, "base")
            copy_directory(base_path, component_path)
            logger.debug(" 拷贝 %s 下所有文件到 %s" % (base_path, component_path))

    def _write_data_to_local_properties(self, react_value):
        local_file_path = os.path.join(os.getcwd(), "local.properties")
        try:
            properties_str = "#\n#" + time.asctime(time.localtime(time.time()))
            properties_str += "\n" + "react=%s\n" % react_value
            logger.info(" 将react=%s 键值对写入到 %s 文件中" % (react_value, local_file_path))
            write_content_to_file(local_file_path, properties_str)
            logger.info(" 写入成功")
        except Exception as e:
            error_message = "严格模式写入异常: %s" % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()

