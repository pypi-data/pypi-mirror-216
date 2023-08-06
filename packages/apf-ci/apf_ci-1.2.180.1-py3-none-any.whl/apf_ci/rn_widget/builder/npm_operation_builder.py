#!/usr/bin/python3
# -*- coding: utf-8 -*-
from apf_ci.android.build_prepare.builder.clean_config_file_builder import CleanConfigFileBuilder
from apf_ci.rn_widget.builder.build_tool_builder import *
from apf_ci.rn_widget.builder.check_env_name_builder import *
from apf_ci.rn_widget.builder.multi_language_resource_builder import MultiLanguageResourceBuilder
from apf_ci.util.rsa_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.util.http_utils import *


class NpmOperationBuilder:
    def __init__(self, plugin_component_id, pages_result_json, close_cache, component_type, cs_config):
        self.plugin_component_id = plugin_component_id
        self.pages_result_json = pages_result_json
        self.close_cache = close_cache
        self.component_type = component_type
        self.cs_config = cs_config

    def perform(self, variables_json, widget_module_json):
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, "target")

        react_widget_path = os.path.join(target_path, "react_widget")
        if not os.path.exists(react_widget_path):
            os.mkdir(react_widget_path)
        react_widget_path = os.path.join(target_path, "react_widget")

        plugin_component_id_dir = self.plugin_component_id
        plugin_component_path = os.path.join(react_widget_path, plugin_component_id_dir)
        if not os.path.exists(plugin_component_path):
            os.mkdir(plugin_component_path)
        plugin_component_id_dir_path = os.path.join(react_widget_path, plugin_component_id_dir)

        languages_array = variables_json["app_language_array"]

        package_name = variables_json["build_package"]
        build_app_name = variables_json["build_app_name"]
        app_type = variables_json["build_app_type"]
        env_target = variables_json["envtarget"]
        factory_id = variables_json["factoryId"]

        lite_app_host = variables_json["lite_app_server"]
        git_repository = variables_json["react_widget"]["git_repository"]
        commit_id = variables_json["react_widget"]["commit_id"]
        build_tool = variables_json["react_widget"]["build_tool"]
        # 兼容快照版本，不使用构建工具，commitId统一换成e27ce7f3，即RN颗粒版本控制规则的功能进行构建
        is_use_build_tool = True if build_tool != "" else False
        logger.debug(" isUseBuildTool： %s" % is_use_build_tool)

        factory_app_type = variables_json["factoryAppType"]
        logger.debug(" factoryAppType： %s" % factory_app_type)

        pages_json_array = self.pages_result_json.get("pages", "")
        npm_dependencies_json = self.pages_result_json.get("npmDependencies", {})
        widgets_json_arr = self.pages_result_json.get("widgets", {})

        # 记录page id归属那个插件提供
        page_id_and_plugin_keymap = {}
        plugin_keymap = {}
        for pages_json in pages_json_array:
            pages_json_id = pages_json.get("id", "")
            plugin_key = pages_json.get("pluginKey", "")
            page_id_and_plugin_keymap[pages_json_id] = plugin_key
            page_id_list = plugin_keymap.get(plugin_key, [])
            page_id_list.append(pages_json_id)
            plugin_keymap[plugin_key] = page_id_list

        pages = json.dumps(pages_json_array)
        npm_dependencies = json.dumps(npm_dependencies_json)
        check_env_name_builder = CheckEnvNameBuilder(env_target)
        check_env_name_builder.perform(variables_json)
        rn_debug_mode = variables_json["rn_debug_mode"]

        project = git_repository + commit_id + build_tool + npm_dependencies + pages
        project_md5 = get_md5(project)
        logger.debug(" 【project】= %s" % project)
        logger.debug(" 【projectMd5】= %s" % project_md5)

        # App颗粒控件对接翻译门户。
        # 需求来源：redmine #9940 移动端：cmk
        multi_language_resource_builder = MultiLanguageResourceBuilder()
        multi_language_resource_builder.widget_language_resource_perform(widgets_json_arr, languages_array, factory_id,
                                                                         widget_module_json, self.cs_config,
                                                                         plugin_component_id_dir, variables_json)


        lite_app_skin_json = variables_json["liteAppSkinJson"]
        lite_app_language_json = variables_json["liteAppLanguageJson"]

        lite_app_json_object = {}
        lite_app_json_object.update(lite_app_skin_json)
        lite_app_json_object.update(lite_app_language_json)

        resource_md5 = self._get_resource_md5(lite_app_json_object, widgets_json_arr, pages_json_array, languages_array,
                                              app_type, plugin_component_id_dir, factory_app_type)
        logger.debug(" 【resourceMd5】= %s" % resource_md5)

        dev_version = self._is_dev_version(npm_dependencies_json)
        logger.debug(" 【是否关闭缓存构建】： %s ，【是否存在dev版本】：%s " % (self.close_cache, dev_version))

        is_use_cache = False
        nd_dependencies = ""
        record_arr = []
        all_cache_data = {}

        plugin_component_id = self.plugin_component_id
        plugin_component_ids = plugin_component_id.split(":")
        last_dot = plugin_component_id.rfind(".")
        ns = plugin_component_id[:last_dot]
        name = plugin_component_id[last_dot + 1:]

        if not self.close_cache and not dev_version:
            url = lite_app_host + "/v0.1/app/" + build_app_name + "/" + app_type + "/" + env_target + "/latest?componentType=" + self.component_type + "&packageName=" + package_name + "&namespace=" + ns + "&bizName=" + name + "&dev=" + rn_debug_mode
            respone_body = get_data(url)
            logger.debug("缓存responeBody = %s" % respone_body)
            logger.debug("projectMd5 = %s" % project_md5)
            logger.debug("resourceMd5 = %s" % resource_md5)
            cache_data = self._get_cache_data(respone_body, project_md5, resource_md5, plugin_component_id)
            logger.debug("缓存cacheData = %s" % cache_data)
            if cache_data != {}:
                all_cache_data[plugin_component_id] = cache_data
                nd_dependencies = json.dumps(cache_data.get("dependencies"))
                is_use_cache = True
        logger.info(" 【判断是否使用缓存】：%s" % is_use_cache)

        update_time = variables_json["lite_app_update_time"]
        logger.info(" 升级更新时间lite_app_update_time：%s" % update_time)
        snapshot_time = ""

        if is_use_cache:
            # 使用缓存
            self._use_cache_build(record_arr, all_cache_data, is_use_build_tool, app_type, languages_array,
                                  plugin_component_id_dir)
            nd_dependencies = self._get_nd_dependencies(plugin_component_id_dir)
        else:
            # 子应用要先把appendData，才能压倒zip包里去， 后的就不要append了
            if factory_app_type != "" and factory_app_type.lower() == "sub":
                self._sub_app_append_components_data(build_app_name, app_type, env_target, ns, name, languages_array,
                                                     update_time)
            page_id_list = []
            self._unuse_cache_build(is_use_build_tool, pages_json_array, page_id_list, plugin_component_id_dir,
                                    variables_json)
            self._unuse_cache_result_handle(record_arr, is_use_build_tool, app_type, build_app_name, env_target,
                                            update_time, languages_array, page_id_list, plugin_keymap,
                                            plugin_component_id_dir, factory_app_type, variables_json)
            nd_dependencies = self._get_nd_dependencies(plugin_component_id_dir)

        version_code = variables_json["build_version_code"]
        logger.debug(" 应用版本：%s" % version_code)

        build_app_version = variables_json["build_app_version"]
        logger.debug(" 构建应用版本：%s" % build_app_version)

        if "appVersionId" in os.environ.keys():
            app_version_id = os.environ["appVersionId"]
            if app_version_id is None or app_version_id == "":
                app_version_id = variables_json["build_version_label"].replace(" ", "").replace(":", "")
        else:
            app_version_id = variables_json["build_version_label"].replace(" ", "").replace(":", "")
        logger.debug(" appVersionId：%s" % app_version_id)
        is_dev = rn_debug_mode.lower() == str(True).lower()
        # 发送消息到轻应用服务上
        dependencies_json_object = json.loads(nd_dependencies)
        for each_record in record_arr:
            obj = {
                "version": env_target,
                "app_type": app_type,
                "component_type": self.component_type,
                "update_time": update_time,
                "factory_id": factory_id,
                "build_status": "SUCCESS",
                "biz_name": each_record.get("bizName"),
                "widgets": widgets_json_arr,
                "dependencies": dependencies_json_object,
                "version_code": version_code,
                "package_name": package_name,
                "project_md5": project_md5,
                "resource_md5": resource_md5,
                "dev": is_dev
            }
            if snapshot_time != "":
                obj["snapshot_time"] = snapshot_time
            item_json = {
                "env": "test",
                "host": each_record.get("host"),
                "zip_url": each_record.get("zip_url"),
                "version_url": each_record.get("version_url")
            }
            items_arr = []
            items_arr.append(item_json)
            obj["items"] = items_arr

            if factory_app_type != "" and factory_app_type.lower() == "sub":
                sub_app_package_name = variables_json["packageName"]
                logger.debug(" 子应用的包名：%s" % sub_app_package_name)
                obj["sub_app_package_name"] = sub_app_package_name
                obj["namespace"] = each_record.get("namespace")

                zips_str = os.getenv("zips")
                zips_arr = None
                if zips_str is None and zips_str == "":
                    zips_arr = []
                else:
                    zips_arr = json.loads(zips_str)
                zips_arr.append(obj)
                variables_json["zips"] = json.dumps(zips_arr)
                variables_path = os.path.join(workspace_path, "target", "variables.json")
                write_content_to_file(variables_path, json.dumps(variables_json, ensure_ascii=False))
            else:
                obj["namespace"] = each_record.get("namespace")
            lite_app_url = lite_app_host + "/v0.1/app/" + build_app_name + "/" + env_target + "/" + build_app_version + "/" + app_version_id
            post_for_array(lite_app_url, obj, True)
        return True

    def _get_resource_md5(self, lite_app_json_object, widgets_json_array, pages_json_array, languages, app_type,
                          plugin_component_id_dir, factory_app_type):
        workspace_path = os.getcwd()
        resource_buffer = ""

        last_dot = plugin_component_id_dir.rfind(".")
        plugin_ns = plugin_component_id_dir[:last_dot]
        plugin_name = plugin_component_id_dir[last_dot + 1:]
        plugin_component_id = plugin_ns + "###" + plugin_name

        skin_zip_file_name = plugin_component_id + ".zip"
        skin_zip_file_path = os.path.join(workspace_path, "target/skinTemp/react", skin_zip_file_name)
        if os.path.exists(skin_zip_file_path):
            value = lite_app_json_object.get(skin_zip_file_path, "")
            resource_buffer += value

        for language_json in languages:
            if not isinstance(language_json, dict):
                continue
            language_name = language_json.get("name", "")
            alias_json = language_json.get("build_alias", {})

            language = alias_json.get(app_type.lower())
            zip_file_name = plugin_component_id + "###" + language + ".zip"
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/react", zip_file_name)
            if os.path.exists(zip_file_path):
                value = lite_app_json_object.get(zip_file_path, "")
                resource_buffer += value

            i18n_file_config_path = os.path.join(workspace_path,
                                                 "target/react_widget/{PLUGIN_COMPONENT_ID}/config".replace(
                                                     "{PLUGIN_COMPONENT_ID}", plugin_component_id_dir))
            if not os.path.exists(i18n_file_config_path):
                os.mkdir(i18n_file_config_path)
            i18n_dir_path = os.path.join(i18n_file_config_path, "i18n")
            if not os.path.exists(i18n_dir_path):
                os.mkdir(i18n_dir_path)
            i18n_platform_path = os.path.join(i18n_dir_path, language_name)
            if not os.path.exists(i18n_platform_path):
                os.mkdir(i18n_platform_path)

            # 取build.json文件中对应的组件内容json信息，放到新建的build.json文件中
            new_build_json_arr = []
            build_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            if os.path.exists(build_file_path):
                build_json_str = read_file_content(build_file_path)
                if build_json_str != "":
                    build_json_arr = json.loads(build_json_str)
                    for build_json in build_json_arr:
                        if not isinstance(build_json, dict):
                            continue
                        component_json = build_json.get("component", "")
                        biz_name = component_json.get("name", "")
                        name_space = component_json.get("namespace", "")

                        for widgets_obj in widgets_json_array:
                            if not isinstance(widgets_obj, dict):
                                continue
                            bizname = widgets_obj.get("biz_name", "")
                            namespace = widgets_obj.get("namespace", "")
                            if biz_name == bizname and name_space == namespace:
                                new_build_json_arr.append(build_json)
                                break
            else:
                logger.debug(" build.json文件不存在： %s" % build_file_path)

            if factory_app_type != "" and factory_app_type.lower() == "sub":
                # 子应用要写进去，然后子应用zip包才有
                component_json = {
                    "namespace", plugin_ns,
                    "name", plugin_name
                }

                json_object = {
                    "component", component_json,
                    "event", {},
                    "properties", {}
                }
                new_build_json_arr.append(json_object)
            new_build_file_path = os.path.join(i18n_platform_path, "build.json")
            write_content_to_file(new_build_file_path, json.dumps(new_build_json_arr, ensure_ascii=False))
            logger.info("成功创建【build.json】文件： %s" % new_build_file_path)

            # 写入的数据就是要加密的
            new_build_file_md5 = get_md5(json.dumps(new_build_json_arr, ensure_ascii=False))
            logger.debug("newBuildFileMd5： %s" % new_build_file_md5)
            resource_buffer += new_build_file_md5

            # 取pages.json文件中对应的组件内容json信息，放到新建的pages.json文件中
            new_pages_json_obj = {}
            pages_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/pages/pages.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            if os.path.exists(pages_file_path):
                pages_json_str = read_file_content(pages_file_path)
                if pages_json_str != "":
                    pages_json_obj = json.loads(pages_json_str)
                    for pages_json_key in pages_json_obj:
                        node_json_obj = pages_json_obj[pages_json_key]
                        if node_json_obj != {}:
                            for pages_obj in pages_json_array:
                                if not isinstance(pages_obj, dict):
                                    continue
                                page_id_name = pages_obj.get("id", "")
                                if pages_json_key == page_id_name:
                                    new_pages_json_obj[pages_json_key] = node_json_obj
            else:
                logger.debug(" pages.json文件不存在：%s" % pages_file_path)

            new_pages_file_path = os.path.join(i18n_platform_path, "pages.json")
            write_content_to_file(new_pages_file_path, json.dumps(new_pages_json_obj, ensure_ascii=False))
            logger.info("成功创建【pages.json】文件：%s" % new_pages_file_path)

            new_pages_file_md5 = get_md5(json.dumps(new_pages_json_obj, ensure_ascii=False))
            logger.debug("newPagesFileMd5: %s" % new_pages_file_md5)
            resource_buffer += new_pages_file_md5

            # 取widget.json文件中对应的组件内容json信息，放到新建的widget.json文件中
            new_widgets_json_object = {}
            widget_file_path = os.path.join(workspace_path,
                                            "app/assets/app_factory/${TAG_LANGUAGE}/pages/widgets.json".replace(
                                                "${TAG_LANGUAGE}", language_name))
            if os.path.exists(widget_file_path):
                widget_json_str = read_file_content(widget_file_path)
                if widget_json_str != "":
                    widget_json_object = json.loads(widget_json_str)
                    for widget_json_key in widget_json_object:
                        node_json_obj = widget_json_object[widget_json_key]
                        if node_json_obj != {} and node_json_obj.get("__top", "").startswith(
                                "react://" + plugin_component_id_dir + "/"):
                            new_widgets_json_object[widget_json_key] = node_json_obj
            else:
                logger.debug(" widgets.json文件不存在： %s" % widget_file_path)

            new_widget_file_path = os.path.join(i18n_platform_path, "widgets.json")
            write_content_to_file(new_widget_file_path, json.dumps(new_widgets_json_object, ensure_ascii=False))
            logger.info("成功创建【widgets.json】文件：%s" % new_widget_file_path)

            new_widget_file_md5 = get_md5(json.dumps(new_widgets_json_object, ensure_ascii=False))
            logger.debug("newWidgetFileMd5：%s" % new_widget_file_md5)
            resource_buffer += new_widget_file_md5

            # 调用构建前准备插件中的 clean_config_file_builder。简化react颗粒构建生成的build.json/pages.json/widgets.json
            # redmine:#6707  PMS:#249749
            logger.info(" rn-widget开始简化文件.....")
            self.__simple_widget_file(new_build_file_path, new_pages_file_path, new_widget_file_path)

        if resource_buffer != "":
            resource_buffer = get_md5(resource_buffer)
        return resource_buffer

    def _is_dev_version(self, npm_dependencies_json_object):
        dev_version = False
        for dependenvies_key in npm_dependencies_json_object:
            dependencies_value = npm_dependencies_json_object[dependenvies_key]
            for npm_key in dependencies_value:
                npm_value = dependencies_value[npm_key]
                if str(npm_value).endswith("-dev"):
                    # 存在-dev版本时，不走缓存
                    dev_version = True
                    break

        return dev_version

    def _get_cache_data(self, response_body, projectMd5, resourceMd5, plugin_key):
        data = {}
        if response_body is not None and response_body != {}:
            project_md5 = response_body.get("project_md5", "")
            resource_md5 = response_body.get("resource_md5", "")
            if project_md5 == projectMd5 and resource_md5 == resourceMd5:
                items_json_array = response_body.get("items", [])
                if items_json_array != []:
                    for item_json in items_json_array:
                        if isinstance(item_json, dict):
                            zip_url = item_json.get("zip_url", "")
                            if zip_url != "":
                                workspace_path = os.getcwd()
                                module_path = os.path.join(workspace_path, "target/react_widget", plugin_key)
                                unzip_file_path = os.path.join(module_path, plugin_key + "_package.zip")
                                logger.debug(" downloading package.zip, to path: %s" % unzip_file_path)

                                try:
                                    download_cs_file(zip_url, unzip_file_path, 3)
                                except Exception:
                                    logger.debug(" 下载zip包失败，直接进行npm构建： %s" % zip_url)

                                logger.debug(" unzip package.zip, to path: %s" % module_path)
                                unzip(unzip_file_path, module_path)

                                host = item_json.get("host", "")
                                version_url = item_json.get("version_url", "")

                                dependencies = response_body.get("dependencies", {})
                                data = {
                                    "host": host,
                                    "zip_url": zip_url,
                                    "version_url": version_url,
                                    "dependencies": dependencies,
                                    "namespace": response_body.get("namespace", ""),
                                    "bizName": response_body.get("biz_name", "")
                                }
                                break
        return data

    def _use_cache_build(self, record_arr, all_cache_data, is_use_build_tool, app_type, languages,
                         plugin_component_id_dir):
        for cache_key in all_cache_data:
            cache_data = all_cache_data[cache_key]

            host_path = cache_data.get("host")
            logger.debug(" hostPath: %s" % host_path)

            start_num = host_path.find("/widget/") + 8
            end_num = host_path.rfind("/test")
            snapshot_time = host_path[start_num:end_num]
            logger.debug(" 快照升级更新时间: %s" % snapshot_time)

            workspace_path = os.getcwd()
            # 拷贝构建文件到相应工作目录下
            if is_use_build_tool:
                self._publish_resource(workspace_path, app_type, plugin_component_id_dir)
            else:
                self._operation_files(workspace_path, app_type, True, None)
            arr = []
            json_object = {
                "namespace": cache_data.get("namespace", ""),
                "bizName": cache_data.get("bizName", ""),
                "host_path": cache_data.get("host", "")
            }
            arr.append(json_object)
            self._append_data_to_file(workspace_path, arr, snapshot_time, languages)

            record_arr.append(cache_data)

    def _publish_resource(self, workspace_path, app_type, plugin_component_id):
        logger.info("\r\n[INFO] -------------拷贝应用构建所需要的文件start-------------")
        react_app_path = os.path.join(workspace_path, "app/assets/app_factory/react_app")

        dist_folder_path = ""
        if app_type.lower() == "ios":
            dist_folder_path = os.path.join(workspace_path, "target/react_widget", plugin_component_id, "iOS")
        elif app_type.lower() == "android":
            dist_folder_path = os.path.join(workspace_path, "target/react_widget", plugin_component_id, "android")

        src_main_path = os.path.join(dist_folder_path, "main")
        dest_main_path = os.path.join(workspace_path, "app/assets/app_factory/react_app", plugin_component_id, "main")
        copy_directory(src_main_path, dest_main_path)
        logger.info(" 拷贝 %s,下所有文件到 %s" % (src_main_path, dest_main_path))

        component_path = os.path.join(react_app_path, "base", "component")
        main_bundle_file_path = os.path.join(component_path, "main.bundle")
        if not os.path.exists(main_bundle_file_path):
            base_path = os.path.join(dist_folder_path, "base")
            copy_directory(base_path, component_path)
            logger.debug(" 拷贝 %s 下所有文件到 %s" % (base_path, component_path))
        logger.info(" -------------拷贝应用构建所需要的文件end-------------\r\n")

    def _operation_files(self, workspace_path, app_type, is_cache, page_id_list):
        logger.info("\r\n[INFO] -------------拷贝应用构建所需要的文件start-------------")
        react_app_path = os.path.join(workspace_path, "app/assets/app_factory/react_app")
        if is_cache:
            dist_folder_path = ""

            if app_type.lower() == "iOS":
                dist_folder_path = os.path.join(workspace_path, "target/react_widget", "iOS")
            elif app_type.lower() == "android":
                dist_folder_path = os.path.join(workspace_path, "target/react_widget", "android")
            dist_folder_list = os.listdir(dist_folder_path)
            if len(dist_folder_list) > 0:
                for page_name in dist_folder_list:
                    if page_name == "i18n":
                        continue
                    dest_page_id_path = os.path.join(react_app_path, page_name)
                    if not os.path.exists(dest_page_id_path):
                        os.mkdir(dest_page_id_path)
                    src_page_id_path = os.path.join(dist_folder_path, page_name)
                    if app_type.lower() == "iOS":
                        # 拷贝/target/react_widget/iOS/{pageid}下所有数据到/app/assets/app_factory/react_app/{pageid}下
                        logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (src_page_id_path, dest_page_id_path))
                        copy_directory(src_page_id_path, dest_page_id_path)
                    elif app_type.lower() == "android":
                        # 拷贝/target/react_widget/android/{pageid}下bundle数据到/app/assets/app_factory/react_app/{pageid}下
                        logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (src_page_id_path, dest_page_id_path))
                        copy_file_first_level(src_page_id_path, dest_page_id_path)

                        res_dest_path = os.path.join(workspace_path, "app/res")
                        if not os.path.exists(res_dest_path):
                            os.mkdir(res_dest_path)
                        logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (src_page_id_path, res_dest_path))
                        copy_folder_first_level(src_page_id_path, res_dest_path)
                    # 拷贝/target/react_widget/android&iOS/i18n/{pageid}下所有文件到/app/assets/app_factory/react_app/i18n/{pageid}下
                    dest_i18n_page_id_path = os.path.join(react_app_path, "i18n", page_name)
                    if not os.path.exists(dest_i18n_page_id_path):
                        os.mkdir(dest_i18n_page_id_path)

                    ios_i18n_src_path = os.path.join(dist_folder_path, "i18n", page_name)
                    logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (ios_i18n_src_path, dest_i18n_page_id_path))
        else:
            for page_id in page_id_list:
                react_app_page_id_path = os.path.join(react_app_path, page_id)
                if not os.path.exists(react_app_page_id_path):
                    os.mkdir(react_app_page_id_path)

                if app_type.lower() == "ios":
                    # 拷贝/target/react_widget/{pageid}/dist/{pageid}/dist/iOS下除i18n文件夹外的所有数据到/target/react_widget/iOS/{pageid}和/app/assets/app_factory/react_app/{pageid}下
                    ios_src_path = os.path.join(workspace_path, "target/react_widget",
                                                "{PAGE_ID}/dist/{PAGE_ID}/dist/iOS".replace("{PAGE_ID}", page_id))
                    logger.debug(" 从 %s 路径下拷贝除i18n文件夹外的所有文件到 %s" % (ios_src_path, react_app_page_id_path))
                    copy_folder_except_folder(ios_src_path, react_app_page_id_path, True, "i18n")

                    ios_folder_path = os.path.join(workspace_path, "target/react_widget", "iOS")
                    page_folder_path = os.path.join(ios_folder_path, page_id)
                    if not os.path.exists(page_folder_path):
                        os.mkdir(page_folder_path)
                    logger.debug(" 从 %s 路径下拷贝除i18n文件夹外的所有文件到 %s" % (ios_src_path, page_folder_path))
                    copy_folder_except_folder(ios_src_path, page_folder_path, True, "i18n")

                    # 拷贝/target/react_widget/{pageid}/dist/{pageid}/dist/iOS/i18n下所有json文件到/target/react_widget/iOS/i18n/{pageid}下
                    i18n_folder_path = os.path.join(ios_folder_path, "i18n", page_id)
                    if not os.path.exists(i18n_folder_path):
                        os.mkdir(i18n_folder_path)

                    src_i18n_path = os.path.join(ios_src_path, "i18n")
                    logger.debug(" 从 %s 路径下拷贝当前一级目录下所有json文件到 %s" % (src_i18n_path, i18n_folder_path))
                    copy_folder_except_folder(ios_src_path, page_folder_path, False, "")
                elif app_type.lower() == "android":
                    android_folder_path = os.path.join(workspace_path, "target/react_widget", "android")

                    # 拷贝/target/react_widget/{pageid}/dist/{pageid}/dist/android/bundle数据到/app/assets/app_factory/react_app/{pageid}和/target/react_widget/android/{pageid}下
                    bundle_src_path = os.path.join(workspace_path, "target/react_widget",
                                                   "{PAGE_ID}/dist/{PAGE_ID}/dist/android/bundle".replace("{PAGE_ID}",
                                                                                                          page_id))
                    logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (bundle_src_path, react_app_page_id_path))
                    copy_directory(bundle_src_path, react_app_page_id_path)

                    android_page_id_path = os.path.join(android_folder_path, page_id)
                    if not os.path.exists(android_page_id_path):
                        os.mkdir(android_page_id_path)
                    logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (bundle_src_path, android_page_id_path))
                    copy_directory(bundle_src_path, android_page_id_path)

                    # 拷贝/target/react_widget/{pageid}/dist/{pageid}/dist/android/res数据到/target/react_widget/android/{pageid}和/app/res下
                    res_src_path = os.path.exists(workspace_path, "target/react_widget",
                                                  "{PAGE_ID}/dist/{PAGE_ID}/dist/android/res".replace("{PAGE_ID}",
                                                                                                      page_id))
                    logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (res_src_path, android_page_id_path))
                    copy_directory(res_src_path, android_page_id_path)

                    app_res_path = os.path.join(workspace_path, "app/res")
                    if not os.path.exists(app_res_path):
                        os.mkdir(app_res_path)
                    logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (res_src_path, app_res_path))
                    copy_directory(res_src_path, app_res_path)

                    # 拷贝/target/react_widget/{pageid}/dist/{pageid}/dist/android/i18n路径下当前一级目录下所有json文件到/target/react_widget/android/i18n/{pageid}下
                    android_i18n_page_id_path = os.path.join(android_folder_path, "i18n", page_id)
                    if not os.path.exists(android_i18n_page_id_path):
                        os.mkdir(android_i18n_page_id_path)
                    src_i18n_path = os.path.join(workspace_path, "target/react_widget",
                                                 "{PAGE_ID}/dist/{PAGE_ID}/dist/android/i18n".replace("{PAGE_ID}",
                                                                                                      page_id))
                    logger.debug(" 从 %s 路径下拷贝当前一级目录下所有json文件到 %s" % (src_i18n_path, android_i18n_page_id_path))
                    copy_folder_except_folder(src_i18n_path, android_i18n_page_id_path, False, "")
            logger.info(" -------------拷贝应用构建所需要的文件end-------------\r\n")

    def _append_data_to_file(self, workspace_path, zip_info_arr, update_time, languages):
        if len(zip_info_arr) > 0:
            for each_zip_info in zip_info_arr:
                component_json = {
                    "namespace": each_zip_info.get("namespace", ""),
                    "name": each_zip_info.get("bizName", "")
                }
                host_path = each_zip_info.get("hostPath", "")
                # announce.json文件
                announce_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/announce.json")
                try:
                    self._append_data_to_announce_file(announce_file_path, host_path, component_json)
                except IOError as e:
                    error_msg = "向 %s 文件追加数据出错 %s" % (announce_file_path, e)
                    logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
                    traceback.print_exc()
                    return "FAILTURE"

                # components.json文件
                component_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/components.json")
                try:
                    self._append_data_to_components_file(component_file_path, host_path, update_time, component_json)
                except IOError as e:
                    error_msg = "向 %s 文件追加数据出错 %s" % (component_file_path, e)
                    logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
                    traceback.print_exc()
                    return "FAILTURE"

                # 向各语言下build.json文件中追加widget内容
                try:
                    self._append_data_to_build_file(workspace_path, languages, component_json)
                except IOError as e:
                    error_msg = "向 %s 文件追加数据出错 %s" % (component_file_path, e)
                    logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
                    traceback.print_exc()
                    return "FAILTURE"
        return "SUCCESS"

    def _append_data_to_announce_file(self, announce_file_path, host_path, component_json):
        if os.path.exists(announce_file_path):
            announce_content = read_file_content(announce_file_path)
            logger.info(" 正在读取announce.json文件： %s" % announce_file_path)
            announce_json = json.loads(announce_content)

            react_json_arr = []
            react_content = announce_json.get(self.component_type)
            if react_content:
                announce_json.pop(self.component_type)
                react_json_arr = react_content
            if len(react_json_arr) > 0:
                for each_react_json in react_json_arr:
                    if isinstance(each_react_json, dict):
                        each_comp_json = each_react_json.get("component")
                        component_namespace = component_json.get("namespace", "")
                        component_name = component_json.get("name", "")
                        each_comp_namespace = each_comp_json.get("namespace", "")
                        each_comp_name = each_comp_json.get("name", "")
                        if component_namespace.lower() == each_comp_namespace.lower() and component_name.lower() == each_comp_name.lower():
                            return
            local_h5_json = {
                "component": component_json,
                "host": host_path,
                "version": "1.0.0"
            }
            react_json_arr.append(local_h5_json)
            announce_json[self.component_type] = react_json_arr

            announce_data = json.dumps(announce_json)
            logger.debug(" 正在向announce.json文件中新增 %s 节点内容" % self.component_type)
            write_content_to_file(announce_file_path, announce_data)

    def _append_data_to_components_file(self, component_file_path, host_path, update_time, component_json):
        if os.path.exists(component_file_path):
            components_content = read_file_content(component_file_path)
            logger.info(" 正在读取components.json文件： %s" % component_file_path)
            components_arr = json.loads(components_content)

            if len(component_file_path) > 0:
                for each_react_json in components_arr:
                    if isinstance(each_react_json, dict):
                        each_comp_json = each_react_json.get("component")
                        component_namespace = component_json.get("namespace", "")
                        component_name = component_json.get("name", "")
                        each_comp_namespace = each_comp_json.get("namespace", "")
                        each_comp_name = each_comp_json.get("name", "")
                        if component_namespace.lower() == each_comp_namespace.lower() and component_name.lower() == each_comp_name.lower():
                            return
            type_list = []
            type_list.append(self.component_type)

            widget_json = {
                "host": host_path,
                "build_time": update_time,
                "version": str(update_time)
            }
            json_object = {
                "component": component_json,
                "type": type_list,
                self.component_type: widget_json
            }
            components_arr.append(json_object)
            components_data = json.dumps(components_arr)
            logger.info(" 正在向components.json文件中新增widget内容")
            write_content_to_file(component_file_path, components_data)

    def _append_data_to_build_file(self, workspace_path, languages, component_json):
        for language_json in languages:
            if not isinstance(language_json, dict):
                continue
            language_name = language_json.get("name", "")
            build_file_path = os.path.join(workspace_path,
                                           "app/assets/app_factory/${TAG_LANGUAGE}/components/build.json".replace(
                                               "${TAG_LANGUAGE}", language_name))
            build_content = read_file_content(build_file_path)
            components_arr = json.loads(build_content)

            if len(components_arr) > 0:
                for each_react_json in components_arr:
                    if isinstance(each_react_json, dict):
                        each_comp_json = each_react_json.get("component")
                        component_namespace = component_json.get("namespace", "")
                        component_name = component_json.get("name", "")
                        each_comp_namespace = each_comp_json.get("namespace", "")
                        each_comp_name = each_comp_json.get("name", "")
                        if component_namespace.lower() == each_comp_namespace.lower() and component_name.lower() == each_comp_name.lower():
                            return
            json_object = {
                "component": component_json,
                "event": {},
                "properties": {}
            }
            components_arr.append(json_object)

            components_data = json.dumps(components_arr)
            logger.debug(" 正在向build.json文件中新增widget内容：%s" % build_file_path)
            write_content_to_file(build_file_path, components_data)

    def _get_nd_dependencies(self, plugin_component_id_dir):
        workspace_path = os.getcwd()
        if plugin_component_id_dir == "":
            nd_dependencies_file_path = os.path.join(workspace_path,
                                                     "target/react_widget/{PLUGIN_COMPONENT_ID}/ndDependencies.version".replace(
                                                         "{PLUGIN_COMPONENT_ID}", ""))
        else:
            nd_dependencies_file_path = os.path.join(workspace_path,
                                                     "target/react_widget/{PLUGIN_COMPONENT_ID}/ndDependencies.version".replace(
                                                         "{PLUGIN_COMPONENT_ID}", plugin_component_id_dir))
        return read_file_content(nd_dependencies_file_path)

    def _sub_app_append_components_data(self, build_app_name, app_type, env_target, ns, name, languages, update_time):
        cs_path = "/" + build_app_name + "/" + app_type.lower() + "/" + env_target + "/${PluginKey}/widget/" + update_time + "/test"
        host_path = self.cs_config.host + "/static/" + self.cs_config.server_name + cs_path
        zip_info_arr = []
        plugin_key = ns + "." + name
        zip_json = {
            "namespace": ns,
            "bizName": name,
            "cs_path": cs_path,
            "host_path": host_path.replace("${PluginKey}", plugin_key)
        }
        zip_info_arr.append(zip_json)
        self._append_data_to_file(os.getcwd(), zip_info_arr, update_time, languages)

    def _unuse_cache_build(self, is_use_build_tool, pages_jsonarray, page_id_list, plugin_component_id_dir,
                           variable_json):
        if is_use_build_tool:
            for page in pages_jsonarray:
                page_id_list.append(page["id"])

            # 调用RN颗粒构建工具
            build_tool_builder = BuildToolbuilder(page_id_list, plugin_component_id_dir)
            is_build_tool_builder = build_tool_builder.perform(variable_json)

            if not is_build_tool_builder:
                return False
        return True

    def _unuse_cache_result_handle(self, record_arr, is_use_build_tool, app_type, build_app_name, env_target,
                                   update_time, languages, page_id_list, plugin_key_map, plugin_component_id_id_dir,
                                   factory_app_type, variable_json):
        workspace_path = os.getcwd()
        current_time = int(round(time.time() * 1000))
        package_file_name = "${PluginKey}_package" + str(current_time) + ".zip"
        cs_path = "/" + build_app_name + "/" + app_type.lower() + "/" + env_target + "/${PluginKey}/widget/" + str(
            update_time) + "/test"
        host_path = self.cs_config.host + "/static/" + self.cs_config.server_name + cs_path
        version_path = host_path + "/version.json"
        zip_cs_path_str = host_path + "/" + package_file_name
        zip_cs_path = zip_cs_path_str.replace("http://cs.101.com", "https://gcdncs.101.com")

        if not is_use_build_tool:
            # 拷贝构建文件到相应工作目录下
            self._operation_files(workspace_path, app_type, False, page_id_list)

            # 替换国际化资源
            self._replace_language_resource(workspace_path, app_type, languages)
        param_map = {
            "appType": app_type,
            "envtarget": env_target,
            "updateTime": update_time,
            "langauges": languages,
            "csPath": cs_path,
            "zipCsPath": zip_cs_path,
            "hostPath": host_path,
            "packageFileName": package_file_name,
            "versionPath": version_path
        }
        return_json = self._npm_operation(workspace_path, param_map, is_use_build_tool, plugin_key_map,
                                          plugin_component_id_id_dir)

        result = return_json["result"]
        if result == "FAILTURE":
            raise Exception("构建失败，原因：如上【ERROR】日志内容↑↑↑")
            sys.exit(1)
        if result == "SUCCESS":
            session = get_cs_session(self.cs_config)
            cs_offline_host = variable_json["cs_offline_host"]
            cs_offline_url = cs_offline_host + "/v0.1/offline/unpack?session=" + session

            arr = return_json["zipInfo"]
            logger.info(" zipInfo: %s" % arr)
            if len(arr) > 0:
                for json_object in arr:
                    unzip_path = self.cs_config.server_name + json_object.get("csPath", "")
                    unzip_file_path = unzip_path + "/unzip_" + json_object.get("packageFileName", "")
                    self._unzip(cs_offline_url, unzip_file_path, unzip_path)

                    not_cache_data = {
                        "host": json_object.get("hostPath", ""),
                        "zip_url": json_object.get("zipCsPath", ""),
                        "version_url": json_object.get("versionPath", ""),
                        "namespace": json_object.get("namespace", ""),
                        "bizName": json_object.get("bizName", "")
                    }
                    record_arr.append(not_cache_data)

    def _replace_language_resource(self, workspace_path, app_type, languages):
        logger.info(" -------------替换多语言资源start-------------")

        prefix = "android"
        if app_type.lower() == "ios":
            prefix = "iOS"

        app_type_folder_path = os.path.join(os.getcwd(), "target/react_widget", prefix)
        for language_json in languages:
            if not isinstance(language_json, dict):
                continue
            language_name = language_json.get("name", "")
            alias_json = language_json.get("build_alias", {})

            language = alias_json.get(app_type.lower(), "")
            # PathConstant.WIDGET_NAMESPACE  + "###" + PathConstant.WIDGET_BIZNAME + "###" + langauge + ".zip"
            zip_file_name = ""
            zip_file_path = os.path.join(workspace_path, "target/languageTemp/react", zip_file_name)
            if os.path.exists(zip_file_path):
                logger.debug(" 开始语言包解压文件：%s" % zip_file_path)
                unzip_language(app_type_folder_path, zip_file_path, language_name)
                logger.debug(" 解压语言包完毕")
            else:
                logger.debug(" 解压语言包文件找不到：%s" % zip_file_path)
        i18n_dest_folder_path = os.path.join(workspace_path, "app/assets/app_factory/react_app", "i18n")
        if os.path.exists(i18n_dest_folder_path):
            os.mkdir(i18n_dest_folder_path)

        i18n_src_folder_path = os.path.join(app_type_folder_path, "i18n")
        logger.debug(" 从 %s 路径下拷贝所有文件到 %s" % (i18n_src_folder_path, i18n_dest_folder_path))
        copy_directory(i18n_src_folder_path, i18n_dest_folder_path)
        logger.info(" -------------替换多语言资源end-------------\r\n")

    def _npm_operation(self, workspace_path, param_map, is_use_build_tool, plugin_key_map, plugin_component_id_dir):
        return_json = {}
        zip_info_arr = []
        return_json["zipInfo"] = zip_info_arr
        return_json["result"] = "SUCCESS"

        app_type = param_map.get("appType")
        env_target = param_map.get("envtarget")
        update_time = param_map.get("updateTime")
        languages = param_map.get("langauges")

        react_widget_path = os.path.join(workspace_path, "target/react_widget", plugin_component_id_dir)
        app_type_path = ""

        if app_type.lower() == "ios":
            app_type_path = os.path.join(react_widget_path, "iOS")
        elif app_type.lower() == "android":
            app_type_path = os.path.join(react_widget_path, "android")

        if not os.path.exists(app_type_path):
            logger.debug(" 构建失败，%s 目录找不到" % app_type_path)
            return_json["result"] = "FAILTURE"
            return return_json

        zip_file_path = ""
        unzip_file_path = ""
        md5_file_path = os.path.join(react_widget_path, "md5.json")

        with open(md5_file_path, "rb") as f:
            md5_file_data = f.read()
        md5_file_md5 = get_md5(md5_file_data)

        logger.debug(" RSA签名前数据为: %s" % md5_file_md5)
        md5_file_rsa = rsa_util_jar_encryptMd5(md5_file_md5)
        logger.debug(" RSA签名后数据为: %s" % md5_file_rsa)

        for plugin_key in plugin_key_map:
            last_dot = plugin_key.rfind(".")
            ns = plugin_key[:last_dot]
            name = plugin_key[last_dot + 1:]

            zip_file_path = os.path.join(react_widget_path, plugin_key + "_package.zip")
            unzip_file_path = os.path.join(react_widget_path, plugin_key + "_unzip_package.zip")

            cs_path = param_map["csPath"]
            zip_cs_path = param_map["zipCsPath"]
            host_path = param_map["hostPath"]
            package_file_name = param_map["packageFileName"]
            unzip_package_file_name = "unzip_" + package_file_name
            version_path = param_map["versionPath"]

            cs_path = cs_path.replace("${PluginKey}", plugin_key)
            package_file_name = package_file_name.replace("${PluginKey}", plugin_key)
            unzip_package_file_name = unzip_package_file_name.replace("${PluginKey}", plugin_key)

            logger.debug(" versionPath: %s " % version_path)
            logger.debug(" hostPath: %s" % host_path)
            logger.debug(" zipCsPath: %s" % zip_cs_path)

            self._upload_zip_file(zip_file_path, package_file_name, cs_path)
            self._upload_zip_file(unzip_file_path, unzip_package_file_name, cs_path)
            self._upload_file_to_cs(react_widget_path, cs_path, plugin_key_map[plugin_key])

            version_object = {
                "namespace": ns,
                "bizName": name,
                "version": env_target,
                "zip": zip_cs_path.replace("${PluginKey}", plugin_key),
                "md5FileRSA": md5_file_rsa,
                "updateTime": update_time
            }

            version_file_path = os.path.join(react_widget_path, plugin_key + "_version.json")
            try:
                logger.info(" 生成version.json：%s" % version_file_path)
                write_content_to_file(version_file_path, json.dumps(version_object))

                logger.info(" 上传version.json")
                if upload_file_to_cs(version_file_path, cs_path, "version.json", self.cs_config):
                    logger.info("上传成功")
                else:
                    logger.warning("【ERROR】 上传失败")
                    return_json["result"] = "FAILTURE"
                    return return_json
            except Exception:
                logger.warning("【ERROR】  上传异常")
                return_json["result"] = "FAILTURE"
                return return_json

            zip_json = {
                "namespace": ns,
                "bizName": name,
                "csPath": cs_path,
                "packageFileName": package_file_name,
                "unzipPackageFileName": unzip_package_file_name,
                "hostPath": host_path.replace("${PluginKey}", plugin_key),
                "zipCsPath": zip_cs_path.replace("${PluginKey}", plugin_key),
                "versionPath": version_path.replace("${PluginKey}", plugin_key)
            }
            zip_info_arr.append(zip_json)

        result = self._append_data_to_file(workspace_path, zip_info_arr, update_time, languages)
        return_json["result"] = result
        return return_json

    def _upload_zip_file(self, zip_path, file_name, cs_path):
        if not os.path.exists(zip_path):
            error_msg = "编译压缩后zip包不存在 path：%s" % zip_path
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
            raise Exception('编译压缩后zip包不存在')

        # 配置内容服务
        logger.debug(" ContentServiceConfig: %s : %s : %s : %s : %s" % (
            self.cs_config.host, self.cs_config.server_name, self.cs_config.session_id, self.cs_config.user_id,
            cs_path))
        logger.debug(" 上传zip包 %s" % os.path.basename(zip_path))

        try:
            upload_file_to_cs(zip_path, cs_path, file_name, self.cs_config)
            logger.info("上传成功")
        except Exception:
            error_msg = "上传zip包失败"
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
            traceback.print_exc()
            sys.exit()

    def _unzip(self, url, unzip_file_path, unzip_path):
        logger.debug(" 离线解压zip包：%s" % unzip_file_path)

        request_body = {
            "dentry_id": "",
            "file_path": unzip_file_path,
            "parent_path": unzip_path,
            "scope": 1,
            "expire_days": 0
        }
        post_for_array(url, request_body, False)

    def _upload_file_to_cs(self, react_widget_path, cs_path, page_id_list):
        for page_id in page_id_list:
            zip_file_name = page_id + ".zip"
            zip_file_path = os.path.join(react_widget_path, zip_file_name)
            self._upload_zip_file(zip_file_path, zip_file_name, cs_path)

    def __simple_widget_file(self, new_build_file_path, new_pages_file_path, new_widget_file_path):
        """
        简化target/react-widget/{componnetId}/config/i18n/{language}下的build.json、page.json、widgets.json
        :param new_build_file_path:
        :param new_pages_file_path:
        :param new_widget_file_path:
        :return:
        """
        clean_config_builder = CleanConfigFileBuilder()
        # 去除build.json中versionNumber属性
        build_json_content = read_file_content(new_build_file_path)
        build_json = json.loads(build_json_content)

        clean_config_builder.build_remove_attribute(new_build_file_path, build_json)

        # 去除pages.json中第一层级带_的属性
        pages_json_content = read_file_content(new_pages_file_path)
        pages_json = json.loads(pages_json_content)

        clean_config_builder.pages_remove_attribute(new_pages_file_path, pages_json)

        # 简化widgets.json内容格式
        widget_json_content = read_file_content(new_widget_file_path)
        widget_json = json.loads(widget_json_content)

        clean_config_builder.widget_remove_attribute(new_widget_file_path, widget_json)
