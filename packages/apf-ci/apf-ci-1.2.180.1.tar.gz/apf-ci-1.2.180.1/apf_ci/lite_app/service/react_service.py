#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.cache.cache_factory import *
from apf_ci.lite_app.service.apf_service import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.parse_utils import parse_str_to_int


class ReactService(ApfService):
    def build(self, npm_dto):
        cache_bo = npm_dto.cache_bo
        cache_level = cache_bo.cache_level

        data_json = {}

        if cache_level != "":
            module_name = npm_dto.module_name
            module_file_path = os.path.join(os.getcwd(), "target/react", module_name)
            # 如果module_name的位置不存在，则创建
            if not os.path.exists(module_name):
                os.mkdir(module_name)

            module_relative_path = os.path.join("target/react", module_name)
            cache_path = cache_bo.zip_url
            logger.debug(" 缓存级别为: %s" % cache_level)
            # 走缓存操作
            if cache_level == "3":
                logger.debug(" 存在三级缓存 %s" % cache_path)
                self.download_cache_from_cs(module_relative_path, cache_path, "three_level_cache.zip")
            else:
                if cache_level == "2":
                    logger.debug(" 存在二级缓存 %s" % cache_path)
                    self.download_cache_from_cs(module_relative_path, cache_path, "second_level_cache.zip")
                else:
                    if cache_level == "4":
                        logger.debug(" 存在本地缓存 %s" % cache_path)
                        self.download_cache_from_local(module_relative_path, cache_path)
                    elif cache_level == "1":
                        logger.debug(" 存在一级缓存 %s" % cache_path)
                        self.download_cache_from_cs(module_relative_path, cache_path, "first_level_cache.zip")
                    self._save_second_level_cache(npm_dto, cache_bo)
                    # 发布：计算文件md5值,生成md5.json、version.json，压缩zip包
                data_json = self._cache_publish(npm_dto)
        else:
            # 构建完，进行发布操作
            data_json = self._build_publish(npm_dto, cache_bo)

        if data_json is not None and data_json != {}:
            cache_bo.zip_url = data_json["zip_url"]
            cache_bo.host = data_json["host"]
            cache_bo.version_url = data_json["version_url"]
            cache_bo.dependencies = data_json["dependencies"]

        logger.debug(" %s " % cache_bo.tostring_format())
        self._copy_resource_to_app(npm_dto)
        self._append_file_data(npm_dto, cache_bo)
        self.send_lite_app_data(npm_dto, cache_bo)

    def _save_second_level_cache(self, npm_dto, cache_bo):
        is_exits_resources = self._replace_resources(npm_dto)
        if is_exits_resources:
            second_level_cache_md5 = cache_bo.second_level_cache_md5
            logger.debug("正在保存二级缓存: %s" % second_level_cache_md5)

            second_level_cache = CacheFactory.get_cache(CacheEnum.SECOND_LEVEL_REACT_CACHE)
            second_level_cache.save_cache(npm_dto, second_level_cache_md5)

    def _cache_publish(self, npm_dto):
        data_json_object = {}
        param_map = npm_dto.param_map
        module_name = npm_dto.module_name
        app_type = param_map.get("build_app_type", "")
        component_type = ComponentTypeEnum.get_component_type_by_app_type(app_type)

        cs_path_buffer = "/" + param_map.get("build_app_name", "") + "/"
        cs_path_buffer += param_map.get("build_app_type", "").lower() + "/"
        cs_path_buffer += param_map.get("envtarget", "") + "/"
        cs_path_buffer += npm_dto.namespace + "/"
        cs_path_buffer += npm_dto.biz_name + "/"
        cs_path_buffer += component_type + "/"
        cs_path_buffer += str(param_map.get("lite_app_update_time", "")) + "/"
        cs_path_buffer += "test"

        cs_path = cs_path_buffer
        cs_config = param_map.get("csConfig")
        host_path = cs_config.host + "/static/" + cs_config.server_name + cs_path
        version_path = host_path + "/version.json"

        package_file_name = "package" + str(int(round(time.time() * 1000))) + ".zip"
        zip_cs_path = host_path.replace("http://cs.101.com", "https://gcdncs.101.com") + "/" + package_file_name

        data_json_object["zip_url"] = zip_cs_path
        data_json_object["version_url"] = version_path
        data_json_object["host"] = host_path

        module_relative_path = "target/react" + "/" + module_name
        nd_dependencies = self.get_nd_dependencies(module_relative_path)
        data_json_object["dependencies"] = nd_dependencies

        # 拷贝应用所需的配置文件
        self._copy_config_file(module_name, app_type)

        module_path = os.path.join(os.getcwd(), module_relative_path)
        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))

        self.create_md5_file(module_path, platform_path)
        self._operate_zip_file(module_path, platform_path, cs_path, package_file_name, cs_config)
        self.create_version_file(module_path, zip_cs_path, npm_dto, cs_path)

        cs_offline_host = param_map.get("cs_offline_host")
        self.cs_offline_unzip(cs_path, cs_offline_host, package_file_name, cs_config)
        return data_json_object

    def _replace_resources(self, npm_dto):
        """
        替换国际化资源
        :param npm_dto:
        :return:
        """
        module_name = npm_dto.module_name
        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        # 没有该键值对，默认给空字符串
        app_type = npm_dto.param_map.get("build_app_type", "")

        languages_array = npm_dto.param_map.get("app_language_array", "")
        languages_array_str = json.dumps(languages_array)
        language_array_json = json.loads(str(languages_array_str))

        workspace_path = os.getcwd()
        react_path = os.path.join(workspace_path, "target/react")
        module_path = os.path.join(react_path, module_name)
        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))
        i18n_folder_path = os.path.join(platform_path, "main", "i18n")

        flag = False
        for language_json in language_array_json:
            if not isinstance(language_json, dict):
                continue
            language_name = language_json["name"]
            alias_json = language_json["build_alias"]

            language_alias = alias_json.get(app_type.lower())
            zip_file_name = namespace + "###" + biz_name + "###" + language_alias + ".zip"
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/react", zip_file_name)
            if os.path.exists(zip_file_path):
                unzip_flag = self._unzip_language(zip_file_path, i18n_folder_path, language_name)
                if unzip_flag:
                    logger.debug(" 解压语言包完毕： %s" % zip_file_path)
                    flag = True
                else:
                    logger.debug(" 解压失败：zip包中i18n目录下不存在default.json文件")
            else:
                logger.debug(" 解压语言包文件找不到：%s" % zip_file_path)
        return flag

    def _unzip_language(self, source_file, dir_path, language_name):
        flag = False
        file_zip = zipfile.ZipFile(source_file, "r")
        for file in file_zip.namelist():
            if file.startswith("i18n/"):
                # 要读的文件先存一下
                read_zip_file = file
                file = file.replace("i18n/", "")
                # 如果是文件夹路径方式，本方法内暂时不提供操作
                if os.path.isdir(file):
                    continue

                # 如果是文件且文件名为default.json，则直接在对应路径下生成
                if file == "default.json":
                    path = os.path.join(dir_path, language_name + ".json")
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)

                    data = file_zip.read(read_zip_file)
                    self._create_file(path, data)
                    logger.debug("解压后的文件路径： %s" % path)
                    flag = True
        return flag

    def _create_file(self, file_name_path, data):
        if not file_name_path.endswith('/'):
            index = file_name_path.rfind('/')
            parent_file_path = file_name_path[0:index]

            if not os.path.exists(parent_file_path):
                os.makedirs(parent_file_path)

            with open(file_name_path, 'wb') as code:
                code.write(data)

    def _build_publish(self, npm_dto, cache_bo):
        data_json = {}
        param_map = npm_dto.param_map
        module_name = npm_dto.module_name
        app_type = param_map.get("build_app_type", "")

        # 调整目录结构
        self._adjust_struct(module_name, app_type)

        # 保存一级缓存和本地缓存
        first_level_cache_md5 = cache_bo.first_level_cache_md5
        logger.debug(" 正在保存一级缓存: %s" % first_level_cache_md5)
        first_level_cache = CacheFactory.get_cache(CacheEnum.FIRST_LEVEL_REACT_CACHE)
        first_level_cache.save_cache(npm_dto, first_level_cache_md5)

        # 替换国际化资源，并保存二级缓存
        self._save_second_level_cache(npm_dto, cache_bo)
        # 拷贝应用所需的配置文件
        self._copy_config_file(module_name, app_type)

        component_type = ComponentTypeEnum.get_component_type_by_app_type(app_type)
        cs_path = "/" + param_map.get("build_app_name", "") + "/"
        cs_path += param_map.get("build_app_type", "").lower() + "/"
        cs_path += param_map.get("envtarget", "") + "/" + npm_dto.namespace + "/"
        cs_path += npm_dto.biz_name + "/" + component_type + "/"
        cs_path += str(param_map.get("lite_app_update_time", "")) + "/" + "test"

        cs_config = param_map.get("csConfig")
        host_path = ""
        if cs_config is not None:
            host_path = cs_config.host + "/static/" + cs_config.server_name + "/" + cs_path
        version_path = host_path + "/version.json"
        package_file_name = "package" + str(int(round(time.time() * 1000))) + ".zip"
        zip_cs_path = host_path.replace("http://cs.101.com", "https://gcdncs.101.com") + "/" + package_file_name

        data_json["zip_url"] = zip_cs_path
        data_json["version_url"] = version_path
        data_json["host"] = host_path

        module_relative_path = os.path.join("target/react", module_name)
        nd_dependencies = self.get_nd_dependencies(module_relative_path)
        data_json["dependencies"] = nd_dependencies

        module_path = os.path.join(os.getcwd(), module_relative_path)
        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))
        self.create_md5_file(module_path, platform_path)
        self._operate_zip_file(module_path, platform_path, cs_path, package_file_name, cs_config)
        self.create_version_file(module_path, zip_cs_path, npm_dto, cs_path)

        cs_offline_host = param_map.get("cs_offline_host", "")
        self.cs_offline_unzip(cs_path, cs_offline_host, package_file_name, cs_config)
        return data_json

    def _adjust_struct(self, module_name, app_type):
        """
        调整目录结构，即将构建出来的dist移到模块下
        :param module_name:
        :param app_type:
        :return:
        """
        workspace_path = os.getcwd()
        logger.debug("workspace_path:%s, module_name: %s" % (workspace_path, module_name))
        module_path = os.path.join(workspace_path, "target/react", module_name)
        if not os.path.exists(module_path):
            os.mkdir(module_path)
        split_path = os.path.join(module_path, "dist/split")

        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))
        copy_directory(split_path, platform_path)
        logger.debug(" 拷贝 %s 下所有文件到 %s" % (split_path, platform_path))

    def _copy_config_file(self, module_name, app_type):
        """
        拷贝应用所需的配置文件，比如build.json、pages.json及子应用特有的service.json、components.json
        :param module_name:
        :param app_type:
        :return:
        """
        workspace_path = os.getcwd()

        config_path = os.path.join(workspace_path,
                                   "target/react/config/{TAG_MODULE}".replace("{TAG_MODULE}", module_name))
        module_path = os.path.join(workspace_path, "target/react", module_name)
        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))

        components_path = os.path.join(workspace_path, "app/assets/app_factory/app/", "components.json")
        react_module_components_path = os.path.join(module_path, "android/app", "components.json")
        copy_file(components_path, react_module_components_path)
        logger.debug(" 拷贝 %s 到 %s" % (components_path, react_module_components_path))

        service_path = os.path.join(workspace_path, "app/assets/app_factory/app/", "service.json")
        react_module_service_path = os.path.join(module_path, "android/app", "service.json")
        copy_file(service_path, react_module_service_path)
        logger.debug(" 拷贝 %s 到 %s" % (service_path, react_module_service_path))

        copy_directory(config_path, platform_path)
        logger.debug(" 拷贝 %s 下所有文件到 %s" % (config_path, platform_path))

    def _operate_zip_file(self, module_path, platform_path, cs_path, package_file_name, cs_config):
        """
        压缩ZIP包并上传到CS上
        :param module_path:
        :param platform_path:
        :param cs_path:
        :param package_file_name:
        :param cs_config:
        :return:
        """
        logger.debug(" module_path: %s , platform_path: %s ,cs_path: %s , package_file_name: %s " % (
            module_path, platform_path, cs_path, package_file_name))
        md5_file_path = os.path.join(module_path, "md5.json")
        nd_dependencies_file_path = os.path.join(module_path, "ndDependencies.version")

        files_list = []
        files_list.append(platform_path)
        files_list.append(md5_file_path)
        files_list.append(nd_dependencies_file_path)

        zip_file_path = os.path.join(module_path, package_file_name)
        zip_multi_file(zip_file_path, files_list, False)

        upload_file_to_cs(zip_file_path, cs_path, package_file_name, cs_config)

    def _copy_resource_to_app(self, npm_dto):
        module_name = npm_dto.module_name
        app_type = npm_dto.param_map.get("build_app_type", "")

        workspace = os.getcwd()
        module_path = os.path.join(workspace, "target/react", module_name)
        platform_path = os.path.join(module_path, AppTypeEnum.get_platform_by_apptype(app_type))
        src_path = os.path.join(platform_path, "main")

        react_app_path = os.path.join(workspace, "app/assets/app_factory/react_app")
        #if not os.path.exists(react_app_path):
        #    os.mkdir(react_app_path)
        module_name_path = os.path.join(react_app_path, module_name)
        if not os.path.exists(module_name_path):
            os.mkdir(module_name_path)
        dest_path = os.path.join(module_name_path, "main")

        copy_directory(src_path, dest_path)
        logger.debug(" 拷贝 %s 下所有文件到 %s" % (src_path, dest_path))

    def _append_file_data(self, npm_dto, cache_bo):
        workspace = os.getcwd()
        # 向components.json文件填充数据
        self._append_components_file_data(workspace, npm_dto, cache_bo)

    def _append_components_file_data(self, workspace_path, npm_dto, cache_bo):
        components_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/components.json")
        update_time = cache_bo.snapshot_time
        if not update_time:
            update_time = npm_dto.param_map.get("lite_app_update_time", "")
        logger.debug(" _append_components_file_data update_time string ：%s" % update_time)
        update_time = parse_str_to_int(update_time)
        app_type = npm_dto.param_map.get("build_app_type", "")
        if os.path.exists(components_file_path):
            # 这里看看需不需要加文件锁
            # 文件锁 linux fcnfl
            try:
                components_file_content = read_file_content(components_file_path)
                # 解析数据,偶发会获取到NONE ,这里捕获下，再次加载
                components_json_arr = json.loads(components_file_content)
            except Exception as e:
                try:
                    components_file_content = read_file_content(components_file_path)
                    # 解析数据,偶发会获取到NONE ,这里再次加载还是异常的话，报错
                    components_json_arr = json.loads(components_file_content)
                except Exception as e:
                    error_message = "app/assets/app_factory/app/components.json 加载异常，尝试重新打包后，联系开发人员"
                    logger.error(LoggerErrorEnum.JENKINS_BUILD_ERROR_00002, error_message)
                    traceback.print_exc()
                    sys.exit(1)

            for components_json in components_json_arr:
                if not isinstance(components_json, dict):
                    continue

                comp_json = components_json["component"]
                name_space = comp_json["namespace"]
                name = comp_json["name"]

                if npm_dto.namespace == name_space and npm_dto.biz_name == name:
                    if app_type.lower() == "ios":
                        if "react-ios" in components_json.keys():
                            react_ios = components_json["react-ios"]
                            react_ios["build_time"] = update_time
                    elif app_type.lower() == "android":
                        if "react-android" in components_json.keys():
                            react_android = components_json["react-android"]
                            react_android["build_time"] = update_time
                    break

            # 清空文件
            # 写入数据
            write_content_to_file(components_file_path, json.dumps(components_json_arr))
            logger.debug(" 向components.json文件[component] %s ： %s 组件添加【build_time】： %s" % (
                npm_dto.namespace, npm_dto.biz_name, update_time))
