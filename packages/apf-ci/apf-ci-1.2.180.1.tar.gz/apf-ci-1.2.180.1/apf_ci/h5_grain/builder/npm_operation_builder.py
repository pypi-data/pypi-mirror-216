#!/usr/bin/python3
# -*- coding:utf-8 -*-

import datetime
import platform
import re

from apf_ci.h5_grain.builder.create_package_builder import CreatePackageBuilder
from apf_ci.h5_grain.builder.ensure_template_builder import EnsureTemplateBuilder
from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.rsa_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class NpmOperationBuilder:
    def __init__(self, close_cache, build_command, commands_url, cs_config, storage_cs):
        self.close_cache = close_cache
        self.build_command = build_command
        self.commands_url = commands_url
        self.cs_config = cs_config
        self.storage_cs = storage_cs

    def perform(self, variables_json):
        workspace_path = os.getcwd()
        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")
        env_target = variables_json["envtarget"]
        app_type = variables_json["build_app_type"]

        build_app_version = variables_json["build_app_version"]
        build_app_name = variables_json["build_app_name"]
        package_name = variables_json["build_package"]
        version_code = variables_json["build_version_code"]
        languages = variables_json["app_language_array"]
        skin_resource_id = variables_json["skinResourceId"]
        logger.info(" 构建应用版本build_app_version：%s" % build_app_version)
        logger.info(" 应用包名build_package：%s" % package_name)
        logger.info(" 应用版本build_version_code：%s" % version_code)
        logger.info(" 应用语言【app_language_array】===》: %s" % languages)
        logger.info(" 皮肤资源ID【skinResourceId】===》: %s" % skin_resource_id)

        result_obj = variables_json.get("resultObj")
        widgets_arr = result_obj.get("widgets", [])
        pages_arr = result_obj.get("pages", [])

        # 判断是否使用缓存
        logger.info(" 【H5颗粒是否关闭缓存构建】：%s" % self.close_cache)

        cache = False
        host = ""
        zip_url = ""
        version_url = ""
        nd_dependencies = ""

        is_use_cache = True
        dependencies_json = result_obj.get("npmDependencies", "")
        for dependencies_key in dependencies_json:
            dependencies_value = dependencies_json[dependencies_key]
            if dependencies_value.endswith("-dev"):
                # 存在-dev版本时，不走缓存
                is_use_cache = False
                break
        logger.info(" 【是否存在dev版本】：%s" % (not is_use_cache))

        lite_app_host = variables_json["lite_app_server"]
        git_repository = variables_json["h5_grain"]["git_repository"]
        commit_id = variables_json["h5_grain"]["commit_id"]

        pages = json.dumps(result_obj.get("pages"), ensure_ascii=False)
        npm_dependencies = json.dumps(dependencies_json)

        project = git_repository + commit_id + npm_dependencies + pages
        project_md5 = get_md5(project)
        logger.debug(" 【project】= %s" % project)
        logger.debug(" 【projectMd5】= %s" % project_md5)

        lite_app_skin_json = variables_json["liteAppSkinJson"]
        lite_app_language_json = variables_json["liteAppLanguageJson"]

        lite_app_json_object = {}
        lite_app_json_object.update(lite_app_skin_json)
        lite_app_json_object.update(lite_app_language_json)

        resource_md5 = self.__get_resource_md5(lite_app_json_object, widgets_arr, pages_arr, languages, app_type)
        logger.debug(" 【resourceMd5】= %s" % resource_md5)

        if (not self.close_cache) and is_use_cache:
            url = lite_app_host + "/v0.1/app/" + build_app_name + "/" + app_type + "/" + env_target + "/latest?componentType=local-h5&packageName=" + package_name + "&namespace=com.nd.apf.h5&bizName=widget"
            response_body = get_data(url)
            cache_data = self.__get_cache_data(response_body, project_md5, resource_md5)
            if cache_data:
                host = cache_data.get("host")
                zip_url = cache_data.get("zip_url")
                version_url = cache_data.get("version_url")
                nd_dependencies = cache_data.get("dependencies")
                cache = True
        is_cache = cache
        logger.info(" 【H5颗粒是否使用缓存】：%s" % is_cache)

        update_time = variables_json["lite_app_update_time"]
        logger.info(" 升级更新时间lite_app_update_time： %s" % update_time)
        snapshot_time = ""

        npm_registry = variables_json["npm_registry"]
        logger.info(" npmRegistry: %s" % npm_registry)
        if is_cache:
            host_path = host
            logger.info(" hostPath: %s" % host_path)

            snapshot_time = host[host.find("/com.nd.apf.h5/widget/widget/") + 39: host.rfind("/test")]
            logger.info(" 快照升级更新时间: %s" % snapshot_time)
            self.__append_data_to_file(workspace_path, host_path, languages, snapshot_time)
        else:
            ensure_template = EnsureTemplateBuilder(git_repository, commit_id)
            flag = ensure_template.perform()
            if not flag:
                return False
            create_package = CreatePackageBuilder(pages, npm_dependencies)
            is_create_package = create_package.perform(workspace_path)
            if not is_create_package:
                return False
            self.__npm_build(h5_grain_path, npm_registry)

            # 解压皮肤资源，编译CSS文件构建
            self.build_css_file(workspace_path, app_type)
            current_time = str(int(round(time.time() * 1000)))
            cs_path = "/" + build_app_name + "/" + app_type.lower() + "/" + env_target + "/com.nd.apf.h5/widget/widget/" + str(
                update_time) + "/test"
            package_file_name = "package" + current_time + ".zip"
            unzip_package_file_name = "unzip_" + package_file_name

            version_path = self.cs_config.host + "/static/" + self.cs_config.server_name + cs_path + "/version.json"
            hos_path = self.cs_config.host + "/static/" + self.cs_config.server_name + cs_path

            zip_cs_path_str = self.cs_config.host + "/static/" + self.cs_config.server_name + cs_path + "/" + package_file_name
            zip_cs_path = zip_cs_path_str.replace("http://cs.101.com", "https://gcdncs.101.com")

            zip_url = zip_cs_path
            version_url = version_path
            host = hos_path
            logger.debug(" versionPath: %s" % version_path)
            logger.debug(" hosPath: %s" % hos_path)
            logger.debug(" zipCsPath: %s" % zip_cs_path)

            nd_dependencies = self.__read_nd_dependencies_file(workspace_path)

            # 压缩文件，发布
            result = self.__upload_operation(workspace_path, project_md5, widgets_arr, languages, skin_resource_id,
                                             update_time, current_time, package_file_name, unzip_package_file_name,
                                             zip_cs_path, cs_path, hos_path, variables_json, lite_app_json_object)

            if result == "FAILTURE":
                logger.error(LoggerErrorEnum.JENKINS_BUILD_ERROR_002001, "构建失败，原因：如上【ERROR】日志内容↑↑↑")
                sys.exit(1)

            session = get_cs_session(self.cs_config)
            cs_offline_host = variables_json["cs_offline_host"]
            cs_offline_url = cs_offline_host + "/v0.1/offline/unpack?session=" + session
            unzip_path = self.cs_config.server_name + cs_path
            unzip_file_path = unzip_path + "/" + unzip_package_file_name
            self.__offline_unzip(cs_offline_url, unzip_file_path, unzip_path)
             # 重新计算一遍要上传的md5
            self.__update_lite_app_json(lite_app_json_object, languages, app_type, result)
            resource_md5 = self.__get_resource_md5(lite_app_json_object, widgets_arr, pages_arr, languages, app_type)


        # 发送消息到轻应用服务上
        self.__send_into_lite_server(workspace_path, nd_dependencies, widgets_arr, project_md5, resource_md5,
                                     snapshot_time, host, zip_url, version_url, variables_json)
        return True

    def __get_resource_md5(self, lite_app_json, widgets_arr, pages_arr, languages, app_type):
        workspace_path = os.getcwd()
        # 保存资源的源路径
        resource_buffer = ""
        skin_zip_file_name = "com.nd.apf.h5###widget.zip"
        skin_zip_file_path = os.path.join(workspace_path, "target/skinTemp/h5", skin_zip_file_name)
        if os.path.exists(skin_zip_file_path):
            value = lite_app_json.get(skin_zip_file_path, "")
            resource_buffer += value

        for language_json in languages:
            if not isinstance(language_json, dict):
                continue
            language_name = language_json.get("name")
            alias_json = language_json.get("build_alias")

            language = alias_json.get(app_type.lower())
            zip_file_name = "com.nd.apf.h5###widget###" + language + ".zip"
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/h5", zip_file_name)
            if os.path.exists(zip_file_path):
                value = lite_app_json.get(zip_file_path, "")
                resource_buffer += value

            h5_widgettemp_path = os.path.join(workspace_path, "target/h5WidgetTemp")
            if not os.path.exists(h5_widgettemp_path):
                os.makedirs(h5_widgettemp_path)
            i18n_file_path = os.path.join(workspace_path, "target/h5WidgetTemp", "i18n", language_name)
            if not os.path.exists(i18n_file_path):
                os.makedirs(i18n_file_path)

            # 取build.json文件中对应的组件内容json信息，放到新建的build.json文件中
            new_build_json_arr = []
            build_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            if os.path.exists(build_file_path):
                build_json_str = read_file_content(build_file_path)
                if build_json_str:
                    build_json_arr = json.loads(build_json_str)
                    for build_json_obj in build_json_arr:
                        if not isinstance(build_json_obj, dict):
                            continue
                        component_json = build_json_obj.get("component")
                        biz_name = component_json.get("name")
                        name_space = component_json.get("namespace")

                        for widgets_obj in widgets_arr:
                            if not isinstance(widgets_obj, dict):
                                continue
                            widget_biz_name = widgets_obj.get("biz_name")
                            widget_name_space = widgets_obj.get("namespace")

                            if biz_name == widget_biz_name and name_space == widget_name_space:
                                new_build_json_arr.append(build_json_obj)
                                break
            else:
                error_message = 'build.json文件不存在：%s ' % build_file_path
                logger.error(LoggerErrorEnum.FILE_NOT_EXIST, error_message)
                raise Exception(error_message)

            new_build_file_path = os.path.join(i18n_file_path, "build.json")
            write_content_to_file(new_build_file_path, json.dumps(new_build_json_arr, ensure_ascii=False))
            logger.info(" 成功创建【build.json】文件：%s" % new_build_file_path)

            # 取build.json文件的MD5值
            new_build_file_md5 = get_md5(json.dumps(new_build_json_arr, ensure_ascii=False))
            logger.debug("newBuildFileMd5: %s" % new_build_file_md5)
            resource_buffer += new_build_file_md5

            # 取pages.json文件中对应的组件内容json信息，放到新建的pages.json文件中
            new_pages_json_obj = {}
            pages_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            if os.path.exists(pages_file_path):
                pages_json_str = read_file_content(pages_file_path)
                if pages_json_str:
                    pages_json_obj = json.loads(pages_json_str)
                    # 解析page.json文件中满足条件的节点，循环节点
                    for pages_json_key in pages_json_obj:
                        node_json_obj = pages_json_obj[pages_json_key]
                        if node_json_obj:
                            for pages_obj in pages_arr:
                                if not isinstance(pages_obj, dict):
                                    continue
                                page_id_name = pages_obj.get("id")
                                if pages_json_key == page_id_name:
                                    new_pages_json_obj[pages_json_key] = node_json_obj
            else:
                error_message = 'pages.json文件不存在：%s' % pages_file_path
                logger.error(LoggerErrorEnum.FILE_NOT_EXIST, error_message)
                raise Exception(error_message)

            new_pages_file_path = os.path.join(i18n_file_path, "pages.json")
            write_content_to_file(new_pages_file_path, json.dumps(new_pages_json_obj, ensure_ascii=False))
            logger.info("成功创建【pages.json】文件：%s" % new_pages_file_path)

            # 计算pages.json文件的MD5值
            new_pages_file_md5 = get_md5(json.dumps(new_pages_json_obj, ensure_ascii=False))
            logger.debug("newPagesFileMd5: %s" % new_pages_file_md5)
            resource_buffer += new_pages_file_md5

            # 取widget.json文件中对应的组件内容json信息，放到新建的widget.json文件中
            new_widgets_json_obj = {}
            widget_file_path = os.path.join(workspace_path,
                                            "app/assets/app_factory/${TAG_LANGUAGE}/pages/widgets.json".replace(
                                                "${TAG_LANGUAGE}", language_name))
            if os.path.exists(widget_file_path):
                widget_json_str = read_file_content(widget_file_path)
                new_widgets_json_obj = json.loads(widget_json_str)
            else:
                error_message = 'widgets.json文件不存在：%s' % widget_file_path
                logger.error(LoggerErrorEnum.FILE_NOT_EXIST, error_message)
                raise Exception(error_message)

            new_widget_file_path = os.path.join(i18n_file_path, "widgets.json")
            write_content_to_file(new_widget_file_path, json.dumps(new_widgets_json_obj, ensure_ascii=False))

            # 计算Widgets.json文件的MD5值
            new_widget_file_md5 = get_md5(json.dumps(new_widgets_json_obj, ensure_ascii=False))
            logger.debug("newWidgetFileMd5: %s" % new_widget_file_md5)
            resource_buffer += new_widget_file_md5
        logger.debug("resource_buffer: %s" % resource_buffer)
        resource_md5 = resource_buffer
        # 计算所有文件的md5值的 md5 用于判断文件是否被修改过。
        if resource_md5:
            resource_md5 = get_md5(resource_md5)
        return resource_md5

    def __upload_operation(self, workspace_path, project_md5, widgets_arr, languages, skin_resource_id, update_time,
                           current_time, package_file_name, unzip_package_file_name, zip_cs_path, cs_path, hos_path,
                           variables_json, lite_app_json_object):
        env_target = variables_json["envtarget"]
        factory_id = variables_json["factoryId"]
        app_type = variables_json["build_app_type"]
        storage_host = variables_json["app_native_storage"]
        build_app_name = variables_json["build_app_name"]

        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")
        h5_grain_dist_path = os.path.join(h5_grain_path, "dist")
        if not os.path.exists(h5_grain_dist_path):
            logger.warning(" 构建失败， %s 目录找不到" % h5_grain_dist_path)
            return "FAILTURE"
        version_txt_file_path = os.path.join(workspace_path, "target/h5_grain/version.txt")
        logger.info(" 正在创建version.txt文件：%s" % version_txt_file_path)
        write_content_to_file(version_txt_file_path, project_md5)

        # 压缩皮肤和语言zip包，并上传到存储CS内容服务上
        lite_app_update_time = int(update_time)
        storage_cs_path = "/" + env_target + "/com.nd.apf.h5/widget/all"
        storage_cs_host_path = self.storage_cs.host + "/static/" + self.storage_cs.server_name + storage_cs_path

        skin_zip_file_name = "skin_" + current_time + ".zip"
        language_zip_file_name = "language_" + current_time + ".zip"
        skin_zip_cs_path_str = storage_cs_host_path + "/" + skin_zip_file_name
        skin_zip_cs_path = skin_zip_cs_path_str.replace("http://cs.101.com", "https://gcdncs.101.com")
        language_zip_cs_path_str = storage_cs_host_path + "/" + language_zip_file_name
        language_zip_cs_path = language_zip_cs_path_str.replace("http://cs.101.com", "https://gcdncs.101.com")
        logger.debug(" skinZipCsPath: %s" % skin_zip_cs_path)
        logger.debug(" languageZipCsPath: %s" % language_zip_cs_path)

        self.__unzip_skin_and_language_upload(h5_grain_dist_path, h5_grain_path, skin_zip_file_name,
                                              language_zip_file_name, version_txt_file_path, storage_cs_path)

        # 1、获取皮肤包和语言包，并解压到相应路径下；2、新建build.json文件、widget.json文件
        param_map = {
            "widgetsArr": widgets_arr,
            "versionMd5Str": project_md5,
            "langauges": languages,
            "app_type": app_type,
            "skinResourceId": skin_resource_id,
            "skinZipCsPath": skin_zip_cs_path,
            "": language_zip_cs_path,
            "factoryId": factory_id,
            "storageHost": storage_host
        }
        self.__get_resources(workspace_path, param_map)

        source_i18n_path = os.path.join(workspace_path, "target/h5WidgetTemp", "i18n")
        dest_i18n_path = os.path.join(h5_grain_dist_path, "i18n")
        logger.debug(" 拷贝 %s 下文件到 %s" % (source_i18n_path, dest_i18n_path))
        copy_directory(source_i18n_path, dest_i18n_path)
        logger.debug(" 计算md5值路径：%s" % h5_grain_dist_path)
        json_map = {}
        if os.path.isdir(h5_grain_dist_path):
            files = os.listdir(h5_grain_dist_path)
            if files:
                for file_name in files:
                    try:
                        file_abs_path = h5_grain_dist_path + "/" + file_name
                        upload_and_calc_md5(file_abs_path, json_map, h5_grain_path)
                    except Exception as e:
                        logger.warning(" 计算md5出错， %s" % e)
                        traceback.print_exc()
                        return "FAILTURE"
        md5_file_md5 = ""
        md5_file_path = os.path.join(h5_grain_path, "md5.json")
        inputstram = json.dumps(json_map)
        logger.info(" 生成md5.json：%s" % md5_file_path)
        with open(md5_file_path, "wb") as file:
            file.write(inputstram.encode())
        md5_file_md5 = get_md5(inputstram.encode())
        # 压缩上传
        try:
            self.__package_and_uploadcs(workspace_path, h5_grain_dist_path, h5_grain_path,
                                        package_file_name, unzip_package_file_name, env_target, zip_cs_path,
                                        md5_file_md5, lite_app_update_time, cs_path)
        except Exception as e:
            traceback.print_exc()
            logger.warning("【ERROR】  上传异常")
            return "FAILTURE"

        # 向announce.json、components.json文件回写数据
        self.__append_data_to_file(workspace_path, hos_path, languages, lite_app_update_time)
        return param_map

    def __update_lite_app_json(self, lite_app_json, languages, app_type, param_map):
        skin_zip_cs_path = ''
        language_zip_cs_path = ''
        logger.debug('更新前的lite_app_json：' + json.dumps(lite_app_json))
        if 'skinZipCsPath' in param_map:
            skin_zip_cs_path = param_map['skinZipCsPath']
        if 'languageZipCsPath' in param_map:
            language_zip_cs_path = param_map['languageZipCsPath']
        workspace_path = os.getcwd()
        # 保存资源的源路径
        resource_buffer = ""
        skin_zip_file_name = "com.nd.apf.h5###widget.zip"
        skin_zip_file_path = os.path.join(workspace_path, "target/skinTemp/h5", skin_zip_file_name)
        if os.path.exists(skin_zip_file_path) and skin_zip_file_path in lite_app_json:
            logger.debug('update_lite_app_json更新前：' + lite_app_json[skin_zip_file_path])
            lite_app_json[skin_zip_file_path] = skin_zip_cs_path
            logger.debug('update_lite_app_json更新后：' + lite_app_json[skin_zip_file_path])

        for language_json in languages:
            if not isinstance(language_json, dict):
                continue
            alias_json = language_json.get("build_alias")

            language = alias_json.get(app_type.lower())
            zip_file_name = "com.nd.apf.h5###widget###" + language + ".zip"
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/h5", zip_file_name)
            if os.path.exists(zip_file_path) and zip_file_path in lite_app_json:
                logger.debug('update_lite_app_json更新前：' + lite_app_json[zip_file_path])
                lite_app_json[zip_file_path] = language_zip_cs_path
                logger.debug('update_lite_app_json更新后：' + lite_app_json[zip_file_path])

        logger.debug('更新后的lite_app_json：' + json.dumps(lite_app_json))

    def __offline_unzip(self, url, unzip_file_path, unzip_path):
        logger.info(" %s 离线解压zip包： %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), unzip_file_path))
        request_body = {
            "dentry_id": "",
            "file_path": unzip_file_path,
            "parent_path": unzip_path,
            "scope": 1,
            "expire_days": 0
        }
        post_for_array(url, request_body, True)

    def __send_into_lite_server(self, workspace, dependencies, widgets_arr, project_md5, resource_md5, snapshot_time,
                                host, zip_url, version_url, variables_dict):
        logger.debug('上传前nd_dependencies：' +json.dumps(dependencies))
        #dependencies = json.loads(nd_dependencies)

        env_target = variables_dict["envtarget"]
        factory_id = variables_dict["factoryId"]
        app_type = variables_dict["build_app_type"]
        version_code = variables_dict["build_version_code"]
        update_time = variables_dict["lite_app_update_time"]
        package_name = variables_dict["build_package"]
        build_app_name = variables_dict["build_app_name"]
        build_app_version = variables_dict["build_app_version"]
        lite_app_host = variables_dict["lite_app_server"]
        app_version_id = variables_dict.get("appVersionId", "")
        if not app_version_id:
            app_version_id = variables_dict.get("build_version_label").replace(" ", "").replace(":", "")
        logger.debug(" appVersionId：%s" % app_version_id)

        obj = {
            "version": env_target,
            "app_type": app_type,
            "component_type": "local-h5",
            "update_time": int(update_time),
            "factory_id": factory_id,
            "build_status": "SUCCESS"
        }
        factory_app_type = variables_dict.get("factoryAppType")
        logger.debug(" factoryAppType：%s" % factory_app_type)
        if factory_app_type and factory_app_type.lower() == "sub":
            sub_app_package_name = variables_dict.get("packageName")
            logger.debug(" 子应用的包名：%s" % sub_app_package_name)
            obj["sub_app_package_name"] = sub_app_package_name
            obj["namespace"] = "com.nd.apf.h5." + sub_app_package_name
        else:
            obj["namespace"] = "com.nd.apf.h5"
        obj["biz_name"] = "widget"
        obj["widgets"] = widgets_arr
        obj["dependencies"] = dependencies
        obj["version_code"] = version_code
        obj["package_name"] = package_name
        obj["project_md5"] = project_md5
        obj["resource_md5"] = resource_md5
        if snapshot_time:
            obj["snapshot_time"] = int(snapshot_time)

        item_json = {
            "env": "test",
            "host": host,
            "zip_url": zip_url,
            "version_url": version_url
        }
        items_arr = []
        items_arr.append(item_json)
        obj["items"] = items_arr
        if factory_app_type and factory_app_type.lower() == "sub":
            zips_str = variables_dict.get("zips")
            if not zips_str:
                zips_arr = []
            else:
                zips_arr = json.loads(zips_str)
            zips_arr.append(obj)
            variables_dict["zips"] = json.dumps(zips_arr)
            variables_path = os.path.join(workspace, "target/variables.json")
            write_content_to_file(variables_path, json.dumps(variables_dict, ensure_ascii=False))

        lite_app_url = lite_app_host + "/v0.1/app/" + build_app_name + "/" + env_target + "/" + build_app_version + "/" + app_version_id
        post_for_array(lite_app_url, obj, False)

    def __package_and_uploadcs(self, workspace_path, h5_grain_dist_path, h5_grain_path,
                               package_file_name, unzip_package_file_name, env_target, zip_cs_path, md5_file_md5,
                               lite_app_update_time, cs_path):
        md5_file_path = os.path.join(h5_grain_path, "md5.json")
        logger.info(" 生成md5.json：%s" % md5_file_path)
        if not os.path.exists(md5_file_path):
            logger.warning("【ERROR】 打包有误， %s 文件找不到" % md5_file_path)
            raise Exception()
        files_list = []
        files_list.append(h5_grain_dist_path)
        files_list.append(md5_file_path)

        nd_dependencies_file_path = os.path.join(workspace_path, "target/h5_grain/ndDependencies.version")
        files_list.append(nd_dependencies_file_path)
        zip_file_path = os.path.join(h5_grain_path, package_file_name)
        unzip_file_path = os.path.join(h5_grain_path, unzip_package_file_name)
        try:
            zip_multi_file(zip_file_path, files_list, False)
            zip_multi_file(unzip_file_path, files_list, True)
        except Exception:
            raise Exception()

        upload_file_to_cs(zip_file_path, cs_path, package_file_name, self.cs_config)
        upload_file_to_cs(unzip_file_path, cs_path, unzip_package_file_name, self.cs_config)

        # 计算md5FileMd5的RSA值
        logger.debug(" RSA签名前数据为: %s" % md5_file_md5)
        md5_file_rsa = rsa_util_jar_encryptMd5(md5_file_md5)
        logger.debug(" RSA签名后数据为: %s" % md5_file_rsa)

        version_object = {
            "namespace": "com.nd.apf.h5",
            "bizName": "widget",
            "version": env_target,
            "zip": zip_cs_path,
            "md5FileRSA": md5_file_rsa,
            "updateTime": lite_app_update_time
        }
        version_file_path = os.path.join(workspace_path, "target/h5_grain", "version.json")

        logger.info(" 生成version.json：%s" % version_file_path)
        version_inputstram = json.dumps(version_object)
        with open(version_file_path, "wb") as file:
            file.write(version_inputstram.encode())
        logger.info(" 上传version.json")
        if upload_file_to_cs(version_file_path, cs_path, "version.json",
                             self.cs_config):
            logger.info("上传成功")
        else:
            logger.warning("【ERROR】 上传失败")
            raise Exception()

    def __get_cache_data(self, response_body, project_md5, resource_md5):
        data = {}
        if response_body:
            resp_project_md5 = response_body.get("project_md5")
            resp_resource_md5 = response_body.get("resource_md5")

            if project_md5 == resp_project_md5 and resource_md5 == resp_resource_md5:
                items_json_arr = response_body.get("items", [])
                if items_json_arr:
                    for item_json_object in items_json_arr:
                        if isinstance(item_json_object, dict):
                            zip_url = item_json_object.get("zip_url")
                            if zip_url:
                                host = item_json_object.get("host")
                                version_url = item_json_object.get("version_url")
                                dependencies = response_body.get("dependencies")
                                data = {
                                    "host": host,
                                    "zip_url": zip_url,
                                    "version_url": version_url,
                                    "dependencies": dependencies
                                }
                                break
        return data

    def __append_data_to_file(self, workspace_path, host_path, languages, update_time):
        # 向announce.json、components.json文件回写数据
        component_json = {
            "namespace": "com.nd.apf.h5",
            "name": "widget"
        }

        announce_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/announce.json")
        try:
            self.__append_data_to_announce_file(announce_file_path, host_path, component_json)
        except Exception as e:
            error_message = '向 %s 文件追加数据出错: %s' % (announce_file_path, e)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            return "FAILTURE"

        components_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/components.json")
        try:
            self.__append_data_to_components_file(components_file_path, host_path, update_time, component_json)
        except Exception as e:
            error_message = '向 %s 文件追加数据出错: %s' % (components_file_path, e)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            return "FAILTURE"

        # 向各语言下build.json文件中追加widget内容
        try:
            self.__append_data_to_build_file(workspace_path, languages, component_json)
        except Exception as e:
            error_message = '向 %s 文件追加数据出错: %s' % (
                'app/assets/app_factory/${TAG_LANGUAGE}/components/build.json'.replace(languages), e)
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            return "FAILTURE"

        return "SUCCESS"

    def __append_data_to_announce_file(self, announce_file_path, host_path, component_json):
        if os.path.exists(announce_file_path):
            announce_content = read_file_content(announce_file_path)
            logger.info(" 正在读取announce.json文件：%s" % announce_file_path)
            announce_json_obj = json.loads(announce_content)

            local_h5_json_arr = []
            local_h5_content = announce_json_obj.get("local-h5")
            if local_h5_content:
                if "local-h5" in announce_json_obj.keys():
                    announce_json_obj.pop("local-h5")
                    # // 向local-h5节点追加数组内容
                local_h5_json_arr = local_h5_content

            local_h5_json = {
                "component": component_json,
                "host": host_path,
                "version": "1.0.0"
            }
            local_h5_json_arr.append(local_h5_json)
            announce_json_obj["local-h5"] = local_h5_json_arr

            announce_data = json.dumps(announce_json_obj)
            logger.info(" 正在向announce.json文件中新增local-h5节点内容")
            write_content_to_file(announce_file_path, announce_data)

    def __append_data_to_components_file(self, component_file_path, host_path, update_time, component_json):
        if os.path.exists(component_file_path):
            components_content = read_file_content(component_file_path)
            logger.info(" 正在读取components.json文件：%s" % component_file_path)
            components_arr = json.loads(components_content)

            type_list = []
            type_list.append("local-h5")
            widget_json = {
                "host": host_path,
                "build_time": update_time,
                "version": str(update_time)
            }

            json_object = {
                "component": component_json,
                "type": type_list,
                "local-h5": widget_json
            }

            components_arr.append(json_object)
            components_data = json.dumps(components_arr, ensure_ascii=False)
            logger.info(" 正在向components.json文件中新增widget内容")
            write_content_to_file(component_file_path, components_data)

    def __append_data_to_build_file(self, workspace_path, languages, component_json):
        for language_json in languages:
            if not isinstance(language_json, dict):
                continue

            language_name = language_json.get("name")
            build_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            build_content = read_file_content(build_file_path)
            components_arr = json.loads(build_content)

            json_object = {
                "component": component_json,
                "event": {},
                "properties": {},
                "version": "release"
            }
            components_arr.append(json_object)

            components_data = json.dumps(components_arr, ensure_ascii=False)
            logger.info(" 正在向build.json文件中新增widget内容：%s" % build_file_path)
            write_content_to_file(build_file_path, components_data)

    def __npm_build(self, path, npm_registry):
        logger.debug(" build_command: %s" % self.build_command)
        if not self.build_command:
            try:
                logger.debug(" commandsUrl: %s" % self.commands_url)
                # 使用爬虫获取build_command.json的内容
                resp = requests.get(self.commands_url)
                command_list = resp.content.decode("utf-8").split('\n')

                for command in command_list:
                    line = command.replace('\r', '')
                    if line.startswith("widget="):
                        self.build_command = line[7:]
            except Exception as e:
                logger.debug(" 下载构建命令模板文件失败，设置为默认值npm run build")
                self.build_command = "npm run build"

        logger.info(" %s execute npm command start" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令： npm config set tmp=%s" % path)
        execute_command(['npm', 'config', 'set', 'tmp=%s' % path], chdir=path)

        logger.info(" 执行命令： npm config set registry='%s'" % npm_registry)
        execute_command(['npm', 'config', 'set', 'registry="%s"' % npm_registry], chdir=path)

        logger.info("开始 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info(" 执行命令： npm install")
        execute_command(['npm', 'install'], chdir=path)
        logger.info("结束 %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        commands = self.build_command.split(" ")
        logger.info(" 执行命令： npm run build")
        run_build_result = execute_command(commands, chdir=path)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.info(" 执行命令： npm install @sdp.nd/light-app-build")
        execute_command(['npm', 'install', '@sdp.nd/light-app-build'], chdir=path)
        logger.info("执行js 开始：%s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if platform.system() == 'Windows':
            logger.info(" 执行命令 node node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js .")
            execute_command(['node', 'node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.'], chdir=path)
        else:
            logger.info(" 执行命令 node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js .")
            execute_command(['node_modules/@sdp.nd/light-app-build/NdDependenciesBuild.js', '.'], chdir=path)
        logger.info(" %s execute npm command end" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __unzip_skin_and_language_upload(self, h5_grain_dist_path, h5_grain_path, skin_zip_file_name,
                                         language_zip_file_name, version_txt_file_path, storage_cs_path):
        """
        压缩皮肤和语言zip包，并上传到存储CS内容服务上
        :param h5_grain_dist_path:
        :param h5_grain_path:
        :param skin_zip_file_name:
        :param language_zip_file_name:
        :param version_txt_file_path:
        :param storage_cs_path:
        :return:
        """
        skin_path = os.path.join(h5_grain_dist_path, "style")
        language_path = os.path.join(h5_grain_dist_path, "i18n")
        skin_zip_file_path = os.path.join(h5_grain_path, skin_zip_file_name)
        language_zip_file_path = os.path.join(h5_grain_path, language_zip_file_name)

        skin_files_list = []
        skin_files_list.append(skin_path)
        skin_files_list.append(version_txt_file_path)
        language_files_list = []
        language_files_list.append(language_path)
        language_files_list.append(version_txt_file_path)
        zip_multi_file(skin_zip_file_path, skin_files_list, False)
        zip_multi_file(language_zip_file_path, language_files_list, False)

        # 上传 zip 文件
        upload_file_to_cs(skin_zip_file_path, storage_cs_path, skin_zip_file_name, self.storage_cs)
        upload_file_to_cs(language_zip_file_path, storage_cs_path, language_zip_file_name, self.storage_cs)

    def __get_resources(self, workspace_path, param_map):
        """
        1、获取皮肤包和语言包，并解压到相应路径下；2、新建build.json文件
        :param workspace_path:
        :param param_map:
        :return:
        """
        widgets_arr = param_map.get("widgetsArr")
        version_md5_str = param_map.get("versionMd5Str")
        languages = param_map.get("langauges")
        app_type = param_map.get("app_type")
        skin_resource_id = param_map.get("skinResourceId")
        skin_zip_cs_path = param_map.get("skinZipCsPath")
        language_zip_cs_path = param_map.get("languageZipCsPath")
        factory_id = param_map.get("factoryId")
        storage_host = param_map.get("storageHost")
        skin_resource_arr = self.__get_json_array(version_md5_str, skin_zip_cs_path)
        resource_json = {
            skin_resource_id: skin_resource_arr
        }
        h5_dist_path = os.path.join(workspace_path, "target/h5_grain", "dist")
        namespace = "com.nd.apf.h5"
        biz_name = "widget"

        style_dest_file_path = os.path.join(h5_dist_path, "style")
        style_file_path = os.path.join(workspace_path, "target/h5_grain", "skinTemp", "style")
        if os.path.exists(style_file_path):
            logger.debug(" 拷贝 %s 皮肤资源到 %s" % (style_file_path, style_dest_file_path))
            copy_directory(style_file_path, style_dest_file_path)

        i18n_path = os.path.join(h5_dist_path, "i18n")
        i18n_page_id_list = os.listdir(i18n_path)
        for i18n_page_id_name in i18n_page_id_list:
            logger.debug("i18nPageIdName=%s" % i18n_page_id_name)
            i18n_page_id_path = os.path.join(i18n_path, i18n_page_id_name)
            i18n_page_id_file_list = os.listdir(i18n_page_id_path)
            for language_json in languages:
                if not isinstance(language_json, dict):
                    continue
                resource_id = language_json.get("id")
                language_name = language_json.get("name")
                alias_json = language_json.get("build_alias")
                language_path = os.path.join(i18n_path, i18n_page_id_name, language_name)
                if not os.path.exists(language_path):
                    os.mkdir(language_path)
                for i18n_page_id_file_name in i18n_page_id_file_list:
                    file_path = os.path.join(i18n_page_id_path, i18n_page_id_file_name)
                    dest_file_path = os.path.join(language_path, i18n_page_id_file_name)
                    logger.debug(" 拷贝文件：%s 到 %s" % (file_path, dest_file_path))
                    copy_file(file_path, dest_file_path)
                language_resource_arr = self.__get_json_array(version_md5_str, language_zip_cs_path)
                resource_json[resource_id] = language_resource_arr

                # 取build.json文件中对应的组件内容json信息，放到新建的build.json文件中
                new_build_json_arr = []
                build_file_path = os.path.join(workspace_path,
                                               "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace(
                                                   "${TAG_LANGUAGE}", language_name))
                logger.info(" 正在读取build.json文件：%s" % build_file_path)
                if os.path.exists(build_file_path):
                    build_json_str = read_file_content(build_file_path)
                    if build_json_str:
                        build_json_arr = json.loads(build_json_str)
                        for build_json in build_json_arr:
                            if not isinstance(build_json, dict):
                                continue
                            component_json = build_json.get("component", "")
                            build_biz_name = component_json.get("name", "")
                            build_name_space = component_json.get("namespace", "")

                            for widgets_obj in widgets_arr:
                                if not isinstance(widgets_obj, dict):
                                    continue
                                build_bizname = widgets_obj.get("biz_name", "")
                                build_namespace = widgets_obj.get("namespace", "")
                                if build_biz_name == build_bizname and build_name_space == build_namespace:
                                    new_build_json_arr.append(build_json)
                                    break
                else:
                    logger.warning(" build.json文件不存在： %s" % build_file_path)

                old_build_file_path = os.path.join(language_path, "build.json")
                write_content_to_file(old_build_file_path, json.dumps(new_build_json_arr, ensure_ascii=False))
                logger.info("成功创建【build.json】文件：%s" % old_build_file_path)

                # 取pages.json文件中对应的组件内容json信息，放到新建的pages.json文件中
                new_pages_json_obj = {}
                pages_file_path = os.path.join(workspace_path,
                                               "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace(
                                                   "${TAG_LANGUAGE}", language_name))
                logger.info(" 正在读取pages.json文件：%s" % pages_file_path)
                if os.path.exists(pages_file_path):
                    pages_json_str = read_file_content(pages_file_path)
                    if pages_json_str:
                        pages_json_obj = json.loads(pages_json_str)
                        for pages_json_key in pages_json_obj:
                            node_json_obj = pages_json_obj[pages_json_key]
                            if node_json_obj:
                                if pages_json_key == i18n_page_id_name:
                                    new_pages_json_obj[pages_json_key] = node_json_obj
                else:
                    logger.warning(" pages.json文件不存在：%s" % pages_file_path)

                new_pages_file_path = os.path.join(language_path, "pages.json")
                write_content_to_file(new_pages_file_path, json.dumps(new_pages_json_obj, ensure_ascii=False))
                logger.info("成功创建【pages.json】文件：%s" % new_pages_file_path)

                # 取widget.json文件中对应的组件内容json信息，放到新建的widget.json文件中
                new_widgets_json_object = {}
                widget_file_path = os.path.join(workspace_path,
                                                "app/assets/app_factory/${TAG_LANGUAGE}/pages/widgets.json".replace(
                                                    "${TAG_LANGUAGE}", language_name))
                if os.path.exists(widget_file_path):
                    widget_json_str = read_file_content(widget_file_path)
                    new_widgets_json_object = json.loads(widget_json_str)
                else:
                    logger.warning(" widgets.json文件不存在： %s" % widget_file_path)

                new_widget_file_path = os.path.join(language_path, "widgets.json")
                write_content_to_file(new_widget_file_path, json.dumps(new_widgets_json_object, ensure_ascii=False))
                logger.info("成功创建【widgets.json】文件：%s" % new_widget_file_path)

                # 语言包资源替换
                language = alias_json.get(app_type.lower())
                # 待解压的语言包路径
                language_temp_path = os.path.join(workspace_path, "target/h5_grain", "languageTemp", language)
                zip_file_name = namespace + "###" + biz_name + "###" + language + ".zip"
                zip_file_path = os.path.join(workspace_path, "target/languageTemp/h5", zip_file_name)
                if os.path.exists(zip_file_path):
                    logger.info(" 开始语言包解压文件：%s" % zip_file_path)

                    if app_type.lower() == "android":
                        self.unzip_android_language(language_temp_path, zip_file_path, namespace, biz_name, language)
                    elif app_type.lower() == "ios":
                        self.unzip_ios_language(language_temp_path, zip_file_path)

                    logger.info(" 解压语言包完毕")

                    language_temp_file_path = os.path.join(language_temp_path, "i18n", i18n_page_id_name)
                    logger.info(" 从 %s 拷贝语言资源到 %s" % (language_temp_file_path, language_path))
                    copy_directory(language_temp_file_path, language_path)
                else:
                    logger.warning(" 解压语言包文件找不到：%s" % zip_file_path)
        obj = {
            "namespace": namespace,
            "biz_name": biz_name,
            "version": "release",
            "resources": resource_json
        }
        url = storage_host + "/v0.8/widget_resources/apps/" + factory_id
        post_for_array(url, obj, False)

    def __get_json_array(self, version, resource_url):
        resource_id_arr = []
        resource_id_json = {
            "os_type": "all",
            "component_type": "h5",
            "version": version,
            "resource_url": resource_url
        }
        resource_id_arr.append(resource_id_json)
        return resource_id_arr

    def build_css_file(self, workspace_path, app_type):
        h5_grain_path = os.path.join(workspace_path, "target/h5_grain")
        skin_zip_file_name = "com.nd.apf.h5###widget.zip"
        skin_zip_file_path = os.path.join(workspace_path, "target/skinTemp/h5", skin_zip_file_name)
        if os.path.exists(skin_zip_file_path):
            key = "com.nd.apf.h5.widget"
            key = key.replace("-", "_").replace(".", "_")

            unzip_root = os.path.join(h5_grain_path, "skinTemp")
            if not os.path.exists(unzip_root):
                os.mkdir(unzip_root)
            if app_type.lower() == "android":
                # 安卓皮肤解压
                self.unzip_android_skin(unzip_root, skin_zip_file_path, key)
            elif app_type.lower() == "ios":
                # ios皮肤解压
                self.unzip_ios_skin(unzip_root, skin_zip_file_path)

            logger.info(" 解压皮肤包完毕：%s" % skin_zip_file_path)
        else:
            logger.warning(" 解压皮肤包文件找不到：%s" % skin_zip_file_path)

            # 拷贝默认生成皮肤资源进行预编译操作
            style_dest_file_path = os.path.join(h5_grain_path, "skinTemp", "style")
            style_file_path = os.path.join(h5_grain_path, "dist", "style")
            if os.path.exists(style_file_path):
                logger.info(" 从 %s 拷贝皮肤资源到 %s" % (style_file_path, style_dest_file_path))
                copy_directory(style_file_path, style_dest_file_path)
                logger.info(" 皮肤资源拷贝完毕")
        template_file_path = os.path.join(workspace_path, "target/h5_grain", "packageTemplate.json")
        template_content = read_file_content(template_file_path)

        package_file_path = os.path.join(h5_grain_path, "skinTemp", "package.json")
        logger.info(" 正在创建package.json文件：%s" % package_file_path)
        write_content_to_file(package_file_path, template_content)

        skin_temp_path = os.path.join(workspace_path, "target/h5_grain/skinTemp")
        node_modules_path = os.path.join(h5_grain_path, "node_modules")
        skintemp_node_modules_path = os.path.join(skin_temp_path, "node_modules")
        if os.path.exists(node_modules_path):
            # 将 h5_grain/node_modules 拷贝到h5_grain/skinTemp/node_modules下
            copy_directory(node_modules_path, skintemp_node_modules_path)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        execute_command(['npm', 'run', 'optimize'], chdir=skin_temp_path)
        logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return True

    def __read_nd_dependencies_file(self, workspace_path):
        nd_dependencies_file_path = os.path.join(workspace_path, "target/h5_grain/ndDependencies.version")
        if not os.path.exists(nd_dependencies_file_path):
            logger.info("ndDependencies.version文件不存在：%s" % nd_dependencies_file_path)
            nd_dependencies_content = "{}"
        else:
            logger.info(" 正在读取ndDependencies.version文件：%s" % nd_dependencies_file_path)
            nd_dependencies_content = read_file_content(nd_dependencies_file_path)
        return json.loads(nd_dependencies_content)

    def unzip_android_skin(self, dir_path, source_file, com_name):
        temp_xml_path = os.path.join(dir_path, str(int(round(time.time() * 1000))) + ".xml")
        if not os.path.exists(source_file) or not zipfile.is_zipfile(source_file):
            error_message = " %s 文件不存在,或者不是有效的压缩文件" % source_file
            logger.error(LoggerErrorEnum.JENKINS_BUILD_ERROR_001001, error_message)
            sys.exit(1)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_zip = zipfile.ZipFile(source_file, 'r')
        for file_name in file_zip.namelist():
            # 如果是文件夹路径方式，本方法内暂时不提供操作
            if file_name[-1] == '/':
                file_name = file_name[:len(file_name) - 1]
                unzip_dir_file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(unzip_dir_file_path):
                    os.makedirs(unzip_dir_file_path)
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

    def unzip_ios_skin(self, dir_path, source_file):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_zip = zipfile.ZipFile(source_file)
        for file_name in file_zip.namelist():
            # 如果是文件夹路径方式，本方法内暂时不提供操作
            if file_name[-1] == '/':
                file_name = file_name[:len(file_name) - 1]
                unzip_dir_file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(unzip_dir_file_path):
                    os.makedirs(unzip_dir_file_path)
            else:
                # 如果是文件，则直接在对应路径下生成
                path = os.path.join(dir_path, file_name)
                self.__extra_zipfile_write(file_zip, file_name, path)

    def __extra_zipfile_write(self, zipfile_obj, file_name, dist_path):
        if not os.path.exists(os.path.dirname(dist_path)):
            os.makedirs(os.path.dirname(dist_path))
        file_output_stream = zipfile_obj.read(file_name)
        try:
            # 若不能使用utf-8写入的话，使用Byte写入
            file_output_stream = file_output_stream.decode("utf-8")
            write_content_to_file(dist_path, file_output_stream)
        except Exception as e:
            with open(dist_path, "wb") as file:
                file.write(file_output_stream)

    def unzip_android_language(self, dir_path, source_file, namespace, biz_name, language_name):
        if not os.path.exists(source_file):
            logger.warning(" unzip_language %s" % source_file)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        key = namespace + "." + biz_name
        key = key.replace("-", "_").replace(".", "_").lower()

        file_zip = zipfile.ZipFile(source_file, 'r')
        for file_name in file_zip.namelist():
            # 如果是文件夹路径方式，本方法内暂时不提供操作
            if file_name[-1] == '/':
                continue
            else:
                # 如果是文件，则直接在对应路径下生成
                names = self.__get_package_name(language_name, file_name)
                name_path = ""
                for s in names:
                    name_path += os.sep + s
                path = dir_path + name_path
                if path.startswith(".xml"):
                    temp_path = path.replace(".xml", "_" + key + ".xml")
                    logger.debug("%s ---- %s" % (path, temp_path))
                    if not os.path.exists(os.path.dirname(temp_path)):
                        os.makedirs(os.path.dirname(temp_path))
                    self.__extra_zipfile_write(file_zip, file_name, temp_path)
                else:
                    parent_file = os.path.dirname(path)
                    if not os.path.exists(parent_file):
                        os.makedirs(parent_file)
                    self.__extra_zipfile_write(file_zip, file_name, path)

    def unzip_ios_language(self, dir_path, source_file):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_zip = zipfile.ZipFile(source_file)
        for file_name in file_zip.namelist():
            # 如果是文件夹路径方式，本方法内暂时不提供操作
            if file_name[-1] == '/':
                file_name = file_name[:len(file_name) - 1]
                unzip_dir_file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(unzip_dir_file_path):
                    os.makedirs(unzip_dir_file_path)
            else:
                # 如果是文件，则直接在对应路径下生成
                path = os.path.join(dir_path, file_name)
                self.__extra_zipfile_write(file_zip, file_name, path)

    def __get_package_name(self, language_name, name):
        logger.debug("【zipEntry.name】 ===> %s 【languageName】 ===>  %s" % (name, language_name))
        separator = os.sep
        if separator == "\\":
            separator = "\\\\"
        names = name.replace("/", os.sep).replace("\\", os.sep).split(separator)

        if language_name != "en" and len(names) >= 2 and names[1].startswith("values"):
            names[1] = "values-%s" + language_name
        if language_name == "en" and len(names) >= 2 and names[1].startswith("values"):
            names[1] = "values"

        # 判断drawable-xxx 中间插入 languageName
        if language_name != "en" and len(names) >= 2 and names[1].startswith("drawable"):
            drawables = names[1].split("-")
            logger.debug("【drawable.pakgName】 ===> %s 【drawables.length】 ===> %s 【languageName】 ===> %s" % (
                names[1], len(drawables), language_name))
            if len(drawables) == 1:
                names[1] = drawables[0] + "-" + language_name
            else:
                names[1] = names[1].replace("-", "-" + language_name + "-", 1)
            logger.debug("替换后【drawable.pakgName】 ===> %s 【languageName】 ===> %s" % (names[1], language_name))
        return names
