# #!/usr/bin/python3
# # -*- coding: utf-8 -*-


from apf_ci.constant.path_constant import PathConstant
from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class CreateResourceBuilder:
    def __init__(self, page_id_list, env_target, factory_id, storage_host, widget_host, plugin_id_dir, cs_config):
        self.page_id_list = page_id_list
        self.env_target = env_target
        self.factory_id = factory_id
        self.storage_host = storage_host
        self.widget_host = widget_host
        self.plugin_id_dir = plugin_id_dir
        self.cs_config = cs_config

    def perform(self, variables_json):
        logger.info(" 开始创建资源create_resource_builder")
        logger.debug(" page_id_list:%s, envtarget:%s, factoryId:%s storageHost:%s, widget_host:%s, plugin_id_dir:%s" % (
                self.page_id_list, self.env_target, self.factory_id, self.storage_host, self.widget_host,
                self.plugin_id_dir))
        workspace_path = os.getcwd()
        # react_widget_path = os.path.join(workspace_path, "target/react_widget")
        #
        # plugin_id_dir_path = os.path.join(react_widget_path, self.plugin_id_dir)
        languages_json_arr = variables_json["languages"]
        all_languages_json_arr = variables_json["allLanguages"]
        app_language_arr = self.get_app_language_array(languages_json_arr, all_languages_json_arr)
        logger.info(" 【语言资源下载】应用语言【app_language_array】===》: %s" % app_language_arr)

        resource_service_host = variables_json["fac_resource_manage"]
        skin_resource_id = self.get_skin_resource_id(resource_service_host)
        # skin_resource_id为空直接退出
        if not skin_resource_id:
            return False
        logger.info(" 皮肤资源ID【skinResourceId】===》: %s" % skin_resource_id)

        self.create_resource(skin_resource_id, app_language_arr, workspace_path, self.plugin_id_dir,
                             variables_json)
        logger.info(" 结束创建资源create_resource_builder")
        return True

    def get_app_language_array(self, languages_json_arr, all_languages_json_arr):
        logger.info(" 【语言资源下载】应用语言【languages】===》:%s" % languages_json_arr)

        app_language_map = {}
        for language in languages_json_arr:
            if isinstance(language, str):
                logger.debug("【语言资源下载】应用语言 ===》: 【String】:%s" % language)
                app_language_map[language] = language
        logger.info(" 【语言资源下载】应用语言列表 ===》【allLanguagesJson】%s" % all_languages_json_arr)

        all_app_language_map = []
        for all_language in all_languages_json_arr:
            if not isinstance(all_language, dict):
                continue

            logger.info(" 【语言资源下载】应用语言列表 ===》: 【obj.getString('name')】: %s" % all_language.get("name"))
            app_language_name = app_language_map.get(all_language.get("name"))
            if app_language_name:
                all_app_language_map.append(all_language)

        return all_app_language_map

    def get_skin_resource_id(self, resource_service_host):
        # http://fac-resouce-manage.oth.web.sdp.101.com/v0.1/resconfig/skin
        skin_resource_url = resource_service_host + "/v0.1/resconfig/skin"
        skin_resource_config_arr = get_data(skin_resource_url)
        if not skin_resource_config_arr:
            logger.warning("皮肤资源类型未配置，请联系管理员进行配置管理！")
            return ""

        skin_resource_id = skin_resource_config_arr[0].get("id")
        return skin_resource_id

    def create_resource(self, skin_resource_id, app_language_arr, workspace_path, plugin_id_dir, variables_json):
        last_dot_index = plugin_id_dir.rfind(".")
        plugin_ns = plugin_id_dir[0:last_dot_index]
        plugin_name = plugin_id_dir[last_dot_index + 1:]

        # 配置存储内容服务，保存皮肤和语言zip包
        current_time = str(int(round(time.time() * 1000)))

        cs_config = self.cs_config
        storage_cs_path = "/" + self.env_target + "/" + plugin_ns + "/" + plugin_name
        storage_cs_host_path = cs_config.host + "/static/" + cs_config.server_name + storage_cs_path

        # 合并各个页面的skin文件
        skin_path = os.path.join(workspace_path, PathConstant.SKIN_PATH.replace("{PLUGIN_ID_DIR}", plugin_id_dir))
        self.merge_skin_file(workspace_path, skin_path)

        # 更新version.txt文件内容
        try:
            version_content_md5 = self.update_version_txt(workspace_path)
        except Exception as e:
            error_message = "更新version.txt文件内容 错误"
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)
        version_txt_file_path = os.path.join(skin_path, "version.txt")

        # 1、操作皮肤资源文件
        skin_android_cs_path, skin_ios_cs_path = self.upload_skin_zip(workspace_path, current_time, storage_cs_path,
                                                                      storage_cs_host_path, plugin_id_dir,
                                                                      skin_path)
        # 2、操作多语言资源文件
        language_android_cs_path, language_ios_cs_path = self.upload_language_zip(variables_json,
                                                                                  workspace_path,
                                                                                  plugin_id_dir,
                                                                                  current_time,
                                                                                  storage_cs_path,
                                                                                  storage_cs_host_path,
                                                                                  version_txt_file_path)
        # 3、发送皮肤和多语言数据到存储服务上
        post_body = self.get_body_data(plugin_ns, plugin_name, version_content_md5, skin_resource_id,
                                       app_language_arr, skin_android_cs_path, skin_ios_cs_path,
                                       language_android_cs_path, language_ios_cs_path)
        widget_resource_url = self.storage_host + "/v0.8/widget_resources/apps/" + self.factory_id
        post_for_array(widget_resource_url, post_body)
        return True

    def merge_skin_file(self, workspace_path, skin_path):
        for page_id in self.page_id_list:
            page_skin_folder_path = os.path.join(workspace_path,
                                                 PathConstant.MOUDLE_SKIN_FOLDER.replace("{PLUGIN_ID_DIR}",
                                                                                         self.plugin_id_dir).replace(
                                                     "{TAG_MOUDLE}", page_id))

            # 原JAVA代码使用策略模式，过滤version.txt文件。
            sub_files = os.listdir(page_skin_folder_path)
            sub_filter_files = []
            for file_name in sub_files:
                if file_name != "version.txt":
                    sub_filter_files.append(file_name)

            skin_file_size = len(sub_filter_files)
            # 存在皮肤文件，则拷贝
            if skin_file_size > 0:
                page_id_skin_path = os.path.join(skin_path, page_id)
                if not os.path.exists(page_id_skin_path):
                    os.makedirs(page_id_skin_path)

                # 不拷贝version.txt文件
                not_copy_file_path = os.path.join(page_skin_folder_path, "version.txt")
                self.copy_directory_and_filter_file(page_skin_folder_path, page_id_skin_path, not_copy_file_path)

    def copy_directory_and_filter_file(self, source_dir, target_dir, not_copy_file_path):
        """
        拷贝文件目录下的文件到另一个目录，并且会忽略掉不需要拷贝的文件
        :param source_dir:
        :param target_dir:
        :return:
        """
        # 复制一整个文件目录结构以及文件
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if not os.path.isdir(source_dir):
           logger.warning('copy_directory：source_dir参数必须为 目录类型, 路径：%s' % source_dir)
        else:
            # 复制层级结构
            for file in os.listdir(source_dir):
                source_f = os.path.join(source_dir, file)
                target_f = os.path.join(target_dir, file)
                if os.path.isfile(source_f):
                    if source_f == not_copy_file_path:
                        logger.debug(" 忽略掉version.txt文件的拷贝: %s" % not_copy_file_path)
                    else:
                        shutil.copy(source_f, target_f)
                if os.path.isdir(source_f):
                    if not os.path.exists(target_f):
                        os.mkdir(target_f)
                    copy_directory(source_f, target_f)

    def update_version_txt(self, workspace_path):
        # 创建version.txt文件，并写入内容
        version_txt_file_path = os.path.join(workspace_path, PathConstant.SKIN_PATH.replace("{PLUGIN_ID_DIR}",
                                                                                            self.plugin_id_dir),
                                             "version.txt")
        logger.info(" 正在覆盖更新version.txt文件内容：%s" % version_txt_file_path)

        version_parent_file_path = os.path.dirname(version_txt_file_path)
        if not os.path.exists(version_parent_file_path):
            os.makedirs(version_parent_file_path)

        # 筛选widget
        widget_request_arr = []

        package_file_path = os.path.join(workspace_path, PathConstant.PACKAGE_JSON_FILE)
        package_content = read_file_content(package_file_path)
        package_content_json = json.loads(package_content)
        npm_dependencies_json = package_content_json.get(self.plugin_id_dir).get("npmDependencies")
        for npm_dependencies_key in npm_dependencies_json:
            npm_dependencies_value = npm_dependencies_json[npm_dependencies_key]
            if not isinstance(npm_dependencies_value, dict):
                continue
            for widget_name in npm_dependencies_value:
                if widget_name.startswith("@app.react.widget.sdp.nd"):
                    # 取 @app.react.page.sdp.nd/xxxx “/”后面的widget name: xxxx
                    widget_plugin_name = widget_name[widget_name.rfind("/") + 1:]
                    widget_version = npm_dependencies_value[widget_name]
                    widget_json = {
                        "name": widget_plugin_name,
                        "version": widget_version
                    }
                    widget_request_arr.append(widget_json)

        # 获取widget 皮肤信息
        # https://widget-manage-server.sdp.101.com/v0.1/skins/actions/batch-query
        widget_skin_url = self.widget_host + "/v0.1/skins/actions/batch-query"
        skin_arr = post_for_array(widget_skin_url, widget_request_arr)

        # 对widget进行排序
        signatures = {}
        for index in range(0, len(skin_arr) - 1):
            skin_object = skin_arr[index]
            signatures[skin_object.get("name")] = skin_object.get("signature")

        version_content_string_builder = ""
        for value in signatures:
            version_content_string_builder += value
        write_content_to_file(version_txt_file_path, version_content_string_builder)
        logger.info(" 开始写入version_text_file_path: %s" % version_txt_file_path)
        return version_content_string_builder

    def upload_skin_zip(self, workspace_path, current_time, storage_cs_path, storage_cs_host_path, plugin_id_dir,
                        skin_path):
        logger.info(" 开始压缩皮肤包打包上传到CS服务上")
        react_widget_path = os.path.join(workspace_path, PathConstant.REACT_WIDGET)

        skin_android_zip_file_name = "skin_android_" + current_time + ".zip"
        skin_android_zip_cs_path = storage_cs_host_path + "/android/" + skin_android_zip_file_name
        skin_android_zip_cs_path = skin_android_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" skinAndroidZipCsPath: %s" % skin_android_zip_cs_path)

        skin_ios_zip_file_name = "skin_iOS_" + current_time + ".zip"
        skin_ios_zip_cs_path = storage_cs_host_path + "/ios/" + skin_ios_zip_file_name
        skin_ios_zip_cs_path = skin_ios_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" skinIosZipCsPath: %s" % skin_ios_zip_cs_path)

        # 压缩皮肤zip包，并上传到存储CS内容服务上
        android_zip_file_path = os.path.join(react_widget_path, plugin_id_dir, skin_android_zip_file_name)
        ios_zip_file_path = os.path.join(react_widget_path, plugin_id_dir, skin_ios_zip_file_name)

        try:
            skin_file_list = os.listdir(skin_path)
            need_zip_file_list = []
            for file_name in skin_file_list:
                absolute_path = os.path.join(skin_path, file_name)
                need_zip_file_list.append(absolute_path)

            zip_multi_file(android_zip_file_path, need_zip_file_list, False)
            zip_multi_file(ios_zip_file_path, need_zip_file_list, False)
        except Exception as e:
            error_message = "皮肤资源压缩有误 %s " % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)

        # 上传文件到cs上
        logger.debug(" android开始上传皮肤包到cs上： file_path:%s, cs_path:%s, file_name:%s" % (
            android_zip_file_path, storage_cs_path + "/android", skin_android_zip_file_name))
        upload_file_to_cs(android_zip_file_path, storage_cs_path + "/android", skin_android_zip_file_name,
                          self.cs_config)
        logger.debug(" ios开始上传皮肤包到cs上： file_path:%s, cs_path:%s, file_name:%s" % (
            android_zip_file_path, storage_cs_path + "/ios", skin_android_zip_file_name))
        upload_file_to_cs(ios_zip_file_path, storage_cs_path + "/ios", skin_ios_zip_file_name, self.cs_config)
        logger.info(" 结束压缩皮肤包打包上传到CS服务上")
        return skin_android_zip_cs_path, skin_ios_zip_cs_path

    def upload_language_zip(self, variables_json, workspace_path, plugin_id_dir, current_time, storage_cs_path,
                            storage_cs_host_path, version_txt_file_path):
        logger.info(" 开始压缩语言包打包上传到CS服务上")
        react_widget_path = os.path.join(workspace_path, PathConstant.REACT_WIDGET)

        build_tool = variables_json["build_tool"]
        if build_tool:
            language_android_path = os.path.join(react_widget_path, plugin_id_dir, "i18n")
            language_ios_path = os.path.join(react_widget_path, plugin_id_dir, "i18n")
        else:
            plugin_id_dir_path = os.path.join(react_widget_path, plugin_id_dir)
            self.operation_language_files(plugin_id_dir_path)

            language_android_path = os.path.join(react_widget_path, plugin_id_dir, PathConstant.ANDROID_I18N)
            language_ios_path = os.path.join(react_widget_path, plugin_id_dir, PathConstant.IOS_I18N)

        language_android_zip_file_name = "language_android_" + current_time + ".zip"
        language_android_zip_cs_path = storage_cs_host_path + "/android/" + language_android_zip_file_name
        language_android_zip_cs_path = language_android_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" languageAndroidZipCsPath: %s" % language_android_zip_cs_path)

        language_ios_zip_file_name = "language_iOS_" + current_time + ".zip"
        language_ios_zip_cs_path = storage_cs_host_path + "/ios/" + language_ios_zip_file_name
        language_ios_zip_cs_path = language_ios_zip_cs_path.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" languageIosZipCsPath: %s" % language_ios_zip_cs_path)

        # 压缩语言zip包，并上传到存储CS内容服务上
        language_android_file_list = [language_android_path, version_txt_file_path]

        language_ios_file_list = [language_ios_path, version_txt_file_path]

        language_android_zip_file_path = os.path.join(react_widget_path, plugin_id_dir, language_android_zip_file_name)
        language_ios_zip_file_path = os.path.join(react_widget_path, plugin_id_dir, language_ios_zip_file_name)

        try:
            zip_multi_file(language_android_zip_file_path, language_android_file_list, False)
            zip_multi_file(language_ios_zip_file_path, language_ios_file_list, False)
        except Exception as e:
            error_msg = "语言资源压缩有误 %s" % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_msg)
            traceback.print_exc()
            sys.exit(1)

        # 上传文件到cs上
        logger.debug(" android开始上传皮肤包到cs上： file_path:%s, cs_path:%s, file_name:%s" % (
            language_android_zip_file_path, storage_cs_path + "/android", language_android_zip_file_name))
        upload_file_to_cs(language_android_zip_file_path, storage_cs_path + "/android", language_android_zip_file_name,
                          self.cs_config)

        logger.debug(" ios开始上传皮肤包到cs上： file_path:%s, cs_path:%s, file_name:%s" % (
            language_ios_zip_file_path, storage_cs_path + "/ios", language_ios_zip_file_name))
        upload_file_to_cs(language_ios_zip_file_path, storage_cs_path + "/ios", language_ios_zip_file_name,
                          self.cs_config)
        logger.info(" 结束压缩语言包打包上传到CS服务上")
        return language_android_zip_cs_path, language_ios_zip_cs_path

    def operation_language_files(self, plugin_id_dir_path):
        logger.info(" -------------拷贝多语言文件start------------- : %s" % plugin_id_dir_path)
        for page_id in self.page_id_list:
            android_i18n_dest_path = os.path.join(plugin_id_dir_path, PathConstant.ANDROID_I18N, page_id)
            if not os.path.exists(android_i18n_dest_path):
                os.makedirs(android_i18n_dest_path)
            android_i18n_src_path = os.path.join(plugin_id_dir_path,
                                                 PathConstant.MOUDLE_ANDROID_I18N_DIST.replace("{TAG_MOUDLE}", page_id))
            logger.debug(" 从%s路径下拷贝所有文件到%s" % (android_i18n_src_path, android_i18n_dest_path))
            copy_directory(android_i18n_src_path, android_i18n_dest_path)

            ios_i18n_dest_path = os.path.join(plugin_id_dir_path, PathConstant.IOS_I18N, page_id)
            if not os.path.exists(ios_i18n_dest_path):
                # // 创建多级目录
                os.makedirs(ios_i18n_dest_path)

            ios_i18n_src_path = os.path.join(plugin_id_dir_path,
                                             PathConstant.MOUDLE_IOS_I18N_DIST.replace("{TAG_MOUDLE}", page_id))
            logger.debug(" 从%s路径下拷贝所有文件到%s" % (ios_i18n_src_path, ios_i18n_dest_path))
            copy_directory(ios_i18n_src_path, ios_i18n_dest_path)
        logger.info(" -------------拷贝多语言文件end-------------")

    def get_body_data(self, plugin_ns, plugin_name, version_content_md5, skin_resource_id, app_language_arr,
                      skin_android_zip_cs_path, skin_ios_zip_cs_path, language_android_zip_cs_path,
                      language_ios_zip_cs_path):
        # 封装皮肤
        skin_resource_arr = self.get_json_array(version_content_md5, skin_android_zip_cs_path, skin_ios_zip_cs_path)
        resource_json = {
            skin_resource_id: skin_resource_arr
        }

        # 封装语言
        for language_json in app_language_arr:
            if not isinstance(language_json, dict):
                continue
            resource_id = language_json.get("id")
            language_resource_arr = self.get_json_array(version_content_md5, language_android_zip_cs_path,
                                                        language_ios_zip_cs_path)
            resource_json[resource_id] = language_resource_arr
        obj = {
            "namespace": plugin_ns,
            "biz_name": plugin_name,
            "version": "release",
            "resources": resource_json
        }
        return obj

    def get_json_array(self, version_content_md5, android_zip_cs_path, ios_zip_cs_path):
        resource_id_arr = []
        android_resource_json = {
            "os_type": "android",
            "component_type": "react",
            "version": version_content_md5,
            "resource_url": android_zip_cs_path
        }
        ios_resource_json = {
            "os_type": "iOS",
            "component_type": "react",
            "version": version_content_md5,
            "resource_url": ios_zip_cs_path
        }
        resource_id_arr.append(android_resource_json)
        resource_id_arr.append(ios_resource_json)
        return resource_id_arr
