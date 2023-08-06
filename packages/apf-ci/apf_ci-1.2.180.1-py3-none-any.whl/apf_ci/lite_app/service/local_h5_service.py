#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
离线H5轻应用构建业务逻辑处理类
"""
import re

import threading
from apf_ci.util.execute_command_utils import *
from apf_ci.lite_app.service.apf_service import *
from apf_ci.lite_app.cache.factor.local_h5_cache_factor import *
from apf_ci.lite_app.cache.cache_factory import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.lite_app.service.config_service import *
import datetime
# 创建全局文件锁
component_file_lock = threading.Lock()


class LocalH5Service(ApfService):
    def build(self, npm_dto):
        param_map = npm_dto.param_map
        workspace = os.getcwd()
        logger.debug("[INFO] 当前路径为 %s" % workspace)

        close_cache = param_map.get("closeCache") == 'true'
        module_name = npm_dto.module_name

        localh5_module_name_path = os.path.join(os.getcwd(), "target/local_h5", module_name)
        if not os.path.exists(localh5_module_name_path):
            os.mkdir(localh5_module_name_path)

        logger.info("[INFO] 开始初始化轻应用资源文件")
        config_service = ConfigService()
        config_service.copy_lite_app_json(npm_dto)

        # 获取缓存因素
        cache_factor = LocalH5CacheFactor()
        cache_factor_bo = cache_factor.get_cache_factor(npm_dto)
        logger.info("[INFO] 获取缓存因素 %s" % cache_factor_bo.tostring_format)


        # 获取各级缓存Md5值
        three_level_cache = CacheFactory.get_cache(CacheEnum.THREE_LEVEL_LOCAL_H5_CACHE)
        second_level_cache = CacheFactory.get_cache(CacheEnum.SECOND_LEVEL_LOCAL_H5_CACHE)
        first_level_cache = CacheFactory.get_cache(CacheEnum.FIRST_LEVEL_LOCAL_H5_CACHE)

        three_level_cache_md5 = three_level_cache.get_cache_md5(cache_factor_bo)
        second_level_cache_md5 = second_level_cache.get_cache_md5(cache_factor_bo)
        first_level_cache_md5 = first_level_cache.get_cache_md5(cache_factor_bo)

        # 获取各级缓存
        cache_bo = three_level_cache.get_cache(three_level_cache_md5, param_map)
        if not close_cache and cache_bo:
            logger.info(" 存在三级缓存: %s" % cache_bo.zip_url)
        else:
            # 三级缓存不存在，则查找二级缓存
            module_relative_path = os.path.join("target/local_h5", module_name)

            cache_bo = second_level_cache.get_cache(second_level_cache_md5, param_map)
            if not close_cache and cache_bo:
                logger.info(" 存在二级缓存: %s" % cache_bo.zip_url)
                self.download_cache_from_cs(module_relative_path, cache_bo.zip_url, "second_level_cache.zip")
            else:
                # 二级缓存不存在，则查找本地缓存
                jenkins_apf_path = "data/jenkins/.apf"
                local_cache_path = os.path.join(jenkins_apf_path, npm_dto.js_package_name, npm_dto.js_version,
                                                str(npm_dto.js_publish_time), first_level_cache_md5 + ".zip")

                if not close_cache and self.is_exist(local_cache_path):
                    logger.info(" 存在本地缓存: %s" % local_cache_path)
                    self.download_cache_from_local(module_relative_path, local_cache_path)
                else:
                    # 本地缓存不存在，则查找一级缓存
                    cache_bo = first_level_cache.get_cache(first_level_cache_md5, param_map)
                    if not close_cache and cache_bo:
                        logger.info(" 存在一级缓存: %s" % cache_bo.zip_url)
                        self.download_cache_from_cs(module_relative_path, cache_bo.zip_url, "first_level_cache.zip")
                    else:
                        # 一级缓存不存在，则进行构建
                        logger.info(" 离线H5是否使用缓存: false")
                        npm_value = npm_dto.js_package_name + "@" + npm_dto.js_version
                        self.__execute_npm_command(npm_value, localh5_module_name_path)

                        # 调整目录结构
                        self.__adjust_struct(module_name)

                        # 保存一级缓存和本地缓存
                        logger.info(" 正在保存一级缓存: %s" % first_level_cache_md5)
                        first_level_cache.save_cache(npm_dto, first_level_cache_md5)

                # 替换皮肤和国际化资源
                is_exits_resources = self.__replace_resources(npm_dto)
                if is_exits_resources:
                    # 保存二级缓存
                    logger.info(" 正在保存二级缓存: %s" % second_level_cache_md5)
                    second_level_cache.save_cache(npm_dto, second_level_cache_md5)
                    # 发布：计算文件md5值,生成md5.json、version.json，压缩zip包
            cache_bo = self.__publish(npm_dto)
            cache_bo.three_level_cache_md5 = three_level_cache_md5
            cache_bo.second_level_cache_md5 = second_level_cache_md5
            cache_bo.first_level_cache_md5 = first_level_cache_md5

        self.__append_file_data(npm_dto, cache_bo)
        self.send_lite_app_data(npm_dto, cache_bo)

    def __execute_npm_command(self, npm_value, localh5_module_name_path):
        """
        执行npm构建相关命令
        :param npm_value:
        :return:
        """
        logger.info(" %s execute npm command start" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令： npm config set tmp=%s" % localh5_module_name_path)
        execute_command(['npm', 'config', 'set', 'tmp=%s' % localh5_module_name_path], chdir=localh5_module_name_path)
        
        logger.info(" 执行命令： npm config set registry='http://registry.npm.sdp.nd/'")
        execute_command(['npm', 'config', 'set', 'registry="http://registry.npm.sdp.nd/"'], chdir=localh5_module_name_path)
        logger.info(" 执行命令: npm install %s" % npm_value)
        # 切换到target/h5/{module_name}目录下  chdir 控制subprocess切到某个目录执行命令
        execute_command(['npm', 'install', npm_value], chdir=localh5_module_name_path)

        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令: npm install @sdp.nd/light-app-build")
        execute_command(['npm', 'install', '@sdp.nd/light-app-build'], chdir=localh5_module_name_path)

        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        platform_name = platform.system()
        # windows环境下，需要用 node xxx.js {参数} 才能执行nodejs
        if platform_name == 'Windows':
            logger.info(" 执行命令 node node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js .")
            execute_command(['node', 'node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.'],
                            chdir=localh5_module_name_path)
        else:
            logger.info(" 执行命令 node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js .")
            execute_command(['node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.'],
                            chdir=localh5_module_name_path)
        logger.info(" %s execute npm command end" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __adjust_struct(self, module_name):
        """
        调整目录结构，即将构建出来的dist移到模块下
        :param module_name:
        :param app_type:
        :return:
        """
        workspace_path = os.getcwd()
        logger.debug("workspace_path:%s, module_name: %s" % (workspace_path, module_name))
        module_path = os.path.join(workspace_path, "target/local_h5", module_name)
        if not os.path.exists(module_path):
            os.mkdir(module_path)

        dist_path = os.path.join(module_path,
                                 "node_modules/@sdp.nd/{TAG_MODULE}/dist".replace("{TAG_MODULE}", module_name))
        module_dist_path = os.path.join(module_path, "dist")
        copy_directory(dist_path, module_dist_path)
        logger.debug(" 正在拷贝文件 %s 到 %s" % (dist_path, module_dist_path))

    def __replace_resources(self, npm_dto):
        """
        替换资源
        :param npm_dto:
        :return:
        """
        module_name = npm_dto.module_name
        namespace = npm_dto.namespace
        biz_name = npm_dto.biz_name
        app_type = npm_dto.param_map.get("build_app_type")

        languages_array = npm_dto.param_map.get("app_language_array")

        workspace_path = os.getcwd()
        local_h5_path = os.path.join(workspace_path, "target/local_h5")
        module_path = os.path.join(local_h5_path, module_name)
        module_dist_path = os.path.join(module_path, "dist")

        skin_zip_file_name = namespace + "###" + biz_name + ".zip"
        skin_zip_file_path = os.path.join(workspace_path, "target/skinTemp/h5", skin_zip_file_name)

        flag = False
        if os.path.exists(skin_zip_file_path):
            key = namespace + "." + biz_name
            key = key.replace("-", "_").replace(".", "_")

            if not os.path.exists(module_dist_path):
                os.mkdir(module_dist_path)

            if app_type.lower() == "android":
                self.unzip_android_skin(module_dist_path, skin_zip_file_path, key)
            elif app_type.lower() == "ios":
                unzip(skin_zip_file_path, module_dist_path)

            logger.info(" 解压皮肤包完毕: %s" % skin_zip_file_path)
            flag = True
        else:
            logger.warning(" 解压皮肤包文件找不到: %s" % skin_zip_file_path)

        for languages_object in languages_array:
            if not isinstance(languages_object, dict):
                continue

            language_name = languages_object.get("name")
            alias_json = languages_object.get("build_alias")

            unzip_root = os.path.join(module_dist_path, "i18n", language_name)
            if not os.path.exists(unzip_root):
                os.makedirs(unzip_root)
            language_alias = alias_json.get(app_type.lower())
            zip_file_name = namespace + "###" + biz_name + "###" + language_alias + ".zip"
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/h5", zip_file_name)
            if os.path.exists(zip_file_path):
                logger.info(" 正在解压语言包文件: %s" % zip_file_path)
                logger.info("解压到: %s" % unzip_root)
                self.unzip_language(unzip_root, zip_file_path)
                logger.info(" 解压语言包完毕")
                flag = True
            else:
                logger.warning(" 解压语言包文件找不到: %s" % zip_file_path)
        return flag

    def unzip_android_skin(self, dir_path, source_file, com_name):
        temp_xml_path = os.path.join(dir_path, str(int(round(time.time() * 1000))) + ".xml")
        if not os.path.exists(source_file):
            logger.warning(" replaceResource source 文件不存在")
            return
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_zip = zipfile.ZipFile(source_file, 'r')
        source_parent_file = os.path.dirname(source_file)
        for file_name in file_zip.namelist():
            # 如果是文件夹路径方式，本方法内暂时不提供操作
            if file_name[-1] == '/':
                file_name = file_name[:len(file_name) - 1]
                unzip_dir_file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(unzip_dir_file_path):
                    os.mkdir(unzip_dir_file_path)
            else:
                # 如果是文件，则直接在对应路径下生成
                path = os.path.join(dir_path, file_name)
                if path.endswith(".xml"):
                    if re.match("res/values", path):
                        # 改判断文件不能重复
                        logger.debug(" unzip_android_skin %s " % path)
                        # 解压文件，从zipfile中读出，写入文件 path
                        self.__extra_zipfile_write(file_zip, file_name, path)
                    else:
                        temp_path = os.path.join(dir_path, file_name.replace(".xml", "_" + com_name + ".xml").lower())
                        logger.debug(" unzip_android_skin path  -----  temp_path: %s ---- %s" % (path, temp_path))
                        # 解压文件，从zipfile中读出，写入文件 temp_path
                        self.__extra_zipfile_write(file_zip, file_name, temp_path)
                else:
                    # 解压文件，从zipfile中读出，写入文件path
                    self.__extra_zipfile_write(file_zip, file_name, path)
        file_zip.close()
        if os.path.exists(temp_xml_path):
            os.remove(temp_xml_path)

    def unzip_language(self, dir_path, source_file):
        if not os.path.exists(source_file):
            logger.warning(" unzip_language: %s" % source_file)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_zip = zipfile.ZipFile(source_file, 'r')
        source_parent_file = os.path.dirname(source_file)
        for file_name in file_zip.namelist():
            if file_name.startswith("i18n/"):
                name = file_name.replace("i18n/", "")
                # 如果是文件夹路径方式，本方法内暂时不提供操作
                if file_name[-1] == '/':
                    dir_path_name = os.path.join(dir_path, name)
                    if not os.path.exists(dir_path_name):
                        os.mkdir(dir_path_name)
                else:
                    # 如果是文件，则直接在对应路径下生成
                    path = os.path.join(dir_path, name)
                    self.__extra_zipfile_write(file_zip, file_name, path)

    def __publish(self, npm_dto):
        cache_bo = CacheBO()
        param_map = npm_dto.param_map
        module_name = npm_dto.module_name
        is_sub_app = param_map.get("isSubApp", "false")

        cs_path_buffer = param_map.get("build_app_name", "") + "/"
        cs_path_buffer += param_map.get("build_app_type", "").lower() + "/"
        cs_path_buffer += param_map.get("envtarget", "") + "/"
        cs_path_buffer += npm_dto.namespace + "/"
        cs_path_buffer += npm_dto.biz_name + "/"
        cs_path_buffer += "local-h5" + "/"
        cs_path_buffer += str(param_map.get("lite_app_update_time", "")) + "/"
        cs_path_buffer += "test"

        cs_path = cs_path_buffer
        cs_config = param_map.get("csConfig")
        host_path = cs_config.host + "/static/" + cs_config.server_name + "/" + cs_path
        version_path = host_path + "/version.json"

        package_file_name = "package" + str(int(round(time.time() * 1000))) + ".zip"
        zip_cs_path = host_path.replace("http://cs.101.com", "https://gcdncs.101.com") + "/" + package_file_name

        cache_bo.zip_url = zip_cs_path
        cache_bo.version_url = version_path
        cache_bo.host = host_path

        module_relative_path = "target/local_h5" + "/" + module_name
        nd_dependencies = self.get_nd_dependencies(module_relative_path)
        cache_bo.dependencies = nd_dependencies

        workspace_path = os.getcwd()
        local_h5_path = os.path.join(workspace_path, "target/local_h5")
        module_path = os.path.join(local_h5_path, module_name)
        module_dist_path = os.path.join(module_path, "dist")
        module_i18n_path = os.path.join(module_path, "i18n")
        module_dist_i18n_path = os.path.join(module_dist_path, "i18n")
        copy_directory(module_i18n_path, module_dist_i18n_path)
        # 拷贝app相关配置
        module_app_config_path = os.path.join(module_path, "app")
        module_dist_app_config_path = os.path.join(module_dist_path, "app")
        copy_directory(module_app_config_path, module_dist_app_config_path)
        logger.debug(" 拷贝 %s 到 %s" % (module_i18n_path, module_dist_i18n_path))

        if is_sub_app == "true":
            module_app_path = os.path.join(module_path, "app")
            module_dist_app_path = os.path.join(module_dist_path, "app")
            copy_directory(module_app_path, module_dist_app_path)

        self.create_md5_file(module_path, module_dist_path)
        # cs 上传的路径 前面不加 /
        self.__operate_zip_file(module_path, cs_path, package_file_name, cs_config)
        self.create_version_file(module_path, zip_cs_path, npm_dto, cs_path)

        # 离线解压，将zip包中的内容解压
        cs_offline_host = param_map.get("cs_offline_host")
        unzip_package_file_name = "unzip_" + package_file_name
        self.cs_offline_unzip(cs_path, cs_offline_host, unzip_package_file_name, cs_config)
        return cache_bo

    def __operate_zip_file(self, module_path, cs_path, package_file_name, cs_config):
        """
        压缩ZIP包并上传到CS上
        :param module_path:
        :param platform_path:
        :param cs_path:
        :param package_file_name:
        :param cs_config:
        :return:
        """
        logger.debug(
            " module_path: %s ,cs_path: %s ,package_file_name: %s " % (module_path, cs_path, package_file_name))
        module_dist_path = os.path.join(module_path, "dist")
        md5_file_path = os.path.join(module_path, "md5.json")
        nd_dependencies_file_path = os.path.join(module_path, "ndDependencies.version")

        files_list = []
        files_list.append(module_dist_path)
        files_list.append(md5_file_path)
        files_list.append(nd_dependencies_file_path)

        unzip_package_file_name = "unzip_" + package_file_name
        zip_file_path = os.path.join(module_path, package_file_name)
        unzip_file_path = os.path.join(module_path, unzip_package_file_name)

        zip_multi_file(zip_file_path, files_list, False)
        zip_multi_file(unzip_file_path, files_list, True)
        # 上传zip包
        upload_file_to_cs(zip_file_path, cs_path, package_file_name, cs_config)
        # 上传离线解压的zip包
        upload_file_to_cs(unzip_file_path, cs_path, unzip_package_file_name, cs_config)

    def __append_file_data(self, npm_dto, cache_bo):
        # 向components.json文件填充数据
        self.__append_components_file_data(npm_dto, cache_bo)

    def __append_components_file_data(self, npm_dto, cache_bo):
        host_path = cache_bo.host
        host_path = host_path.replace("http://cs.101.com", "https://cs.101.com")

        workspace_path = os.getcwd()
        components_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/components.json")
        update_time = cache_bo.snapshot_time
        if not update_time:
            update_time = npm_dto.param_map.get("lite_app_update_time", "")
        if os.path.exists(components_file_path):
            try:
                # 使用锁将写入component文件的资源锁起来
                component_file_lock.acquire()

                # 读取数据
                components_file_content = read_file_content(components_file_path)
                # 解析数据
                components_json_arr = json.loads(components_file_content)
                for components_json in components_json_arr:
                    if not isinstance(components_json, dict):
                        continue

                    comp_json = components_json.get("component")
                    name_space = comp_json.get("namespace")
                    name = comp_json.get("name")

                    if npm_dto.namespace == name_space and npm_dto.biz_name == name:
                        local_h5_json = components_json.get("local-h5")
                        local_h5_json["host"] = host_path
                        local_h5_json["build_time"] = update_time
                        self.preassign_local_h5(local_h5_json, npm_dto, cache_bo, workspace_path)

                # 写入数据
                write_content_to_file(components_file_path, json.dumps(components_json_arr, ensure_ascii=False))
                logger.debug(" 向components.json文件[component] %s ： %s 组件添加【host】： %s 组件添加【build_time】： %s" % (
                    npm_dto.namespace, npm_dto.biz_name, host_path, update_time))

                #解锁
                component_file_lock.release()
            except Exception as e:
                error_message = "写入component文件有误: %s" % e
                logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
                traceback.print_exc()
                sys.exit(1)

    def preassign_local_h5(self, local_h5_json, npm_dto, cache_bo, workspace_path):
        preassign = local_h5_json['preassign']
        if preassign == 'true':
            logger.debug("离线h5组件 %s 预置到应用 " % npm_dto.module_name)
            zip_url = cache_bo.zip_url
            local_h5_path = os.path.join(workspace_path, "target/temp/local_h5")
            local_h5_zip_path = os.path.join(local_h5_path, npm_dto.module_name + '.zip')
            local_h5_temp_path = os.path.join(local_h5_path, npm_dto.module_name)
            download_cs_file(zip_url, local_h5_zip_path, 3)
            unzip(local_h5_zip_path, local_h5_temp_path)
            local_h5_dist_path = os.path.join(local_h5_temp_path, 'dist')
            local_h5_name = npm_dto.namespace + "." + npm_dto.biz_name
            local_h5_preassign_path = os.path.join(workspace_path, "app/assets/app_factory/local_h5", local_h5_name)

            logger.debug("拷贝 %s 到 %s" % (local_h5_dist_path, local_h5_preassign_path))
            copy_directory(local_h5_dist_path, local_h5_preassign_path)


    def __extra_zipfile_write(self, zipfile_obj, file_name, dist_path):
        file_output_stream = zipfile_obj.read(file_name)
        try:
            # 若不能使用utf-8写入的话，使用Byte写入
            file_output_stream = file_output_stream.decode("utf-8")
            write_content_to_file(dist_path, file_output_stream)
        except Exception as e:
            with open(dist_path, "wb") as file:
                file.write(file_output_stream)
