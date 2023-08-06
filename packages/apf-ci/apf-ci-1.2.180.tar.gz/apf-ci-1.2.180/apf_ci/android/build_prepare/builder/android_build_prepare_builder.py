#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.etree import *

from apf_ci.android.build_prepare.builder.certificate_builder import *
from apf_ci.android.build_prepare.builder.clean_config_file_builder import *
from apf_ci.android.build_prepare.builder.config_info_sync import provide_android_capabilities_to_app, \
    provide_android_permission_to_assets
from apf_ci.android.build_prepare.builder.local_properties_builder import *
from apf_ci.android.build_prepare.builder.multi_channel_builder import *
from apf_ci.android.build_prepare.builder.update_project_info_builder import *
from apf_ci.app_init.utils.build_config_utils import BuildConfig, parse_private_host, get_app_factory_deploy_host
from apf_ci.util.hook_service import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.util.private_support_utils import support_private_host
from apf_ci.util.version_utils import get_min_version_android


class AndroidBuildPrepareBuilder:
    def __init__(self):
        pass

    def perform(self, args):
        """
        应用工厂-安卓构建前准备插件 执行入口
        :param args:
        :return:
        """
        is_local = args.isLocal == "true"
        workspace = os.getcwd()
        # 取全局变量
        variables_path = os.path.join(workspace, "target", "variables.json")
        variables_content = read_file_content(variables_path)
        variables_dict = json.loads(variables_content)

        # 调用Hook
        app_type = variables_dict["build_app_type"]
        gradle_home = variables_dict['gradleHome']
        hook_service = HookService(app_type)
        hook_service.hook('pre_android_build_prepare', gradle_home, is_local)

        cert_host = variables_dict["codesign"]

        app_name = variables_dict["build_app_name"]
        sdp_package = variables_dict["build_package"]
        version_code = variables_dict["build_version_code"]
        version_name = variables_dict["build_version_label"]
        app_id = variables_dict["build_app_id"]
        icon_path = variables_dict["build_app_icon"]
        launch_image_android = variables_dict["launch_image_android"]
        #launch_path = variables_dict["launch_url"]
        #launch_xxxhdpi_path = variables_dict["launch_url_xxxhdpi"]
        build_number = os.getenv("BUILD_NUMBER")

        sdk_path = variables_dict["sdk_path"]
        logger.debug("sdkPath:%s" % sdk_path)

        builder_list = []

        # update project info
        if not version_name:
            version_name = build_number
        update_project_info_builder = UpdateProjectInfoBuilder(version_code, version_name, sdp_package, app_name,
                                                               sdk_path)
        update_project_info_builder.perform(variables_dict)

        # gradle cetificate info init
        certificate_builder = CertificateBuilder(app_id, cert_host, True, sdp_package)
        certificate_builder.perform(variables_dict)

        # strict model/  debug mode / target sdk verion
        local_properties_builder = LocalPropertiesBuilder()
        local_properties_builder.perform(variables_dict)

        # update icon
        self.update_icon(icon_path)
        # update launch img
        self.update_launch_img(launch_image_android)

        self.receive_event(variables_dict)

        config_josn_path = os.path.join(os.getcwd(), "app/assets/app_factory/app/config.json")
        config_content = read_file_content(config_josn_path)
        logger.debug("zh-CN的config.json内容：%s" % config_content)
        config_json = json.loads(config_content)

        # 下载安卓通知小图标，从zh-CN下的config取
        self.download_notice_png(config_json)
        # 修改pad支持
        self.android_launcher_icon_support(workspace, config_json)

        # 多渠道包插件构建
        multi_channel_builder = MultiChannelBuilder()
        multi_channel_builder.perform(config_json, variables_dict)

        # reform config builder 修改./app/assets/app_factory/app/app.json
        self.reform_config(config_json)
        #  把配置的android_capabilities内容从android_config_data.json拷贝到app.json
        provide_android_capabilities_to_app(workspace)
        #  把配置的高敏感权限内容从target下拷贝到assets下
        provide_android_permission_to_assets(workspace)

        # 简化文件内容（build.json/page.json/widgets.json），删除不必要的文件。
        clean_config_file_builder = CleanConfigFileBuilder()
        clean_config_file_builder.perform(variables_dict)

        # 安卓应用apk压缩优化
        self._apk_compress(variables_dict)

        # jssdk文件生成
        self._write_jssdk_file(variables_dict)

        # 结束调用hook
        hook_service.hook('post_android_build_prepare', gradle_home, is_local)


    def update_icon(self, icon_path):
        """
        下载app_factory_launcher icon并复制到各个mipmap-hdpi中去
        :param icon_path:
        :return:
        """
        logger.info("开始do update icon")
        if not icon_path:
            logger.warning(" 图标的URL路径为空")
            return

        # 下载到临时文件
        workspace_path = os.getcwd()
        temp = os.path.join(workspace_path, "target/temp/appfactory_launcher_ic.png")
        if os.path.exists(temp):
            os.remove(temp)

        try:
            temp_dir = os.path.dirname(temp)
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            download_cs_file(icon_path, temp, 3)
        except Exception as e:
            logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, '%s 下载失败' % icon_path)
            traceback.print_exc()
            sys.exit(1)
            # 路径不对或获取不到图片，则不替换
        file_size = os.path.getsize(temp)
        if not os.path.exists(temp) or file_size < 1000:
            logger.warning(" 图片的URL错误，从%s获取数据为空." % icon_path)
            return

        hdpi = os.path.join(workspace_path, "app/res/mipmap-hdpi/appfactory_launcher_ic.png")
        mdpi = os.path.join(workspace_path, "app/res/mipmap-mdpi/appfactory_launcher_ic.png")
        xhdpi = os.path.join(workspace_path, "app/res/mipmap-xhdpi/appfactory_launcher_ic.png")
        xxhdpi = os.path.join(workspace_path, "app/res/mipmap-xxhdpi/appfactory_launcher_ic.png")
        xxxhdpi = os.path.join(workspace_path, "app/res/mipmap-xxxhdpi/appfactory_launcher_ic.png")

        copy_file(temp, hdpi)
        copy_file(temp, mdpi)
        copy_file(temp, xhdpi)
        copy_file(temp, xxhdpi)
        copy_file(temp, xxxhdpi)

        logger.info("do update icon完毕")

    def update_launch_img(self, launch_image_android):
        """
        下载 加载图片
        :param launch_url:
        :return:
        """
        logger.info("开始do update launch img")
        for key in launch_image_android:
            launch_url = launch_image_android[key]
            if not launch_url:
                logger.warning("运行图片 default 的URL路径为空")
                continue
            if key == 'default':
                key = 'xxhdpi'
            launch_path_temp = "app/res/drawable-%s/appfactory_splash.9.png" % key
            launch_path = os.path.join(os.getcwd(), launch_path_temp)
            if os.path.exists(launch_path):
                os.remove(launch_path)
            download_cs_file(launch_url, launch_path, 3)
        logger.info(" do update launch img完毕")

    def receive_event(self, variables_dict):
        """
        解析组件定义的事件，更新到每个语言的build.json中
        :param variables_dict:
        :return:
        """
        languages_json = variables_dict["languages"]

        biz_define_map = {}
        define_json_file_path = os.path.join(os.getcwd(), "target/defines.json")
        source = read_file_content(define_json_file_path)
        define_json = json.loads(source)
        for key in define_json:
            define_value = define_json[key]
            handlers = define_value.get("handlers")
            if not handlers:
                continue
            arr = []
            for handler_key in handlers:
                handler_value = handlers[handler_key]
                if isinstance(handler_value, dict):
                    if handler_value.get("_receive_event"):
                        arr.append(handler_value)
            if len(arr) > 0:
                biz_define_key = define_value.get("namespace") + "_" + define_value.get("biz_name")
                biz_define_map[biz_define_key] = arr
        return self._write_build_json_and_handle_event(languages_json, biz_define_map)

    def _write_build_json_and_handle_event(self, languages_json, biz_define_map):
        workspace_path = os.getcwd()
        for language in languages_json:
            build_json_file_path = os.path.join(workspace_path, "app/assets/app_factory", language,
                                                "components/build.json")
            build_content = read_file_content(build_json_file_path)
            build_arr = json.loads(build_content)

            namespace = ""
            name = ""
            for build_element in build_arr:
                temp_com = build_element.get("component")
                temp_event = build_element.get("event")
                # 先读取注解的ID
                namespace = temp_com.get("namespace")
                name = temp_com.get("name")

                handles_key = namespace + "_" + name
                handles = biz_define_map.get(handles_key)
                # define.json中不存在该组件事件，跳过
                if not handles:
                    continue

                # 读取组件的事件。
                if not temp_event:
                    temp_event = {}
                    build_element["event"] = temp_event
                logger.debug("biz: %s --------------- handler event--------------------------" % handles_key)
                for handler in handles:
                    handler_name = handler.get("_name")

                    receive_event = handler.get("_receive_event")
                    logger.debug("handlerName=%s, receiveEvent=%s" % (handler_name, receive_event))
                    if not receive_event:
                        continue
                    for event in receive_event.split(","):
                        event_arr = []
                        if event in temp_event.keys():
                            event_arr = temp_event.get(event)
                        component = {
                            "name": name,
                            "namespace": namespace
                        }
                        event_handler = {
                            "component": component,
                            "handler": handler_name,
                            "sync": "1"
                        }

                        event_arr.append(event_handler)
                        temp_event[event] = event_arr
                    logger.debug("tempEvent = %s" % temp_event)
            build_arr = json.dumps(build_arr, ensure_ascii=False)
            write_content_to_file(build_json_file_path, build_arr)

    def download_notice_png(self, config_json):
        """
        下载安卓通知小图标
        :param config_json:
        :return:
        """
        logger.info("开始下载安卓通知小图标")
        # 获取安卓通知小图标
        notice_url = ""
        android_arr = config_json.get("android")
        if android_arr:
            android_obj = android_arr[0]
            if android_obj:
                notice_url = android_obj.get("notice")

        if not notice_url:
            logger.debug("zh-CN的config.json中没有配置安卓通知小图标notice, 不下载")
        else:
            logger.debug("zh-CN的config.json中的安卓通知小图标notice：%s" % notice_url)
            drawable_hdpi_path = os.path.join(os.getcwd(), "app/res/drawable-hdpi")
            logger.debug("下载安卓通知小图标到：%s目录下，名字为android_notice.png" % drawable_hdpi_path)
            notice_png_path = os.path.join(drawable_hdpi_path, "android_notice.png")

            try:
                # 开始下载
                if not os.path.exists(drawable_hdpi_path):
                    os.mkdir(drawable_hdpi_path)
                download_cs_file(notice_url, notice_png_path, 3)
                logger.info("下载安卓通知小图标完毕！")
            except Exception as e:
                logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, '安卓通知小图标出错 %s 下载失败' % notice_url)
                traceback.print_exc()
                sys.exit(1)

    def android_launcher_icon_support(self, workspace, config_json):
        logger.info(" 查看pad支持开始")
        android_lancher_icon = ""
        android_arr = config_json.get("android")
        if android_arr:
            android_obj = android_arr[0]
            if android_obj:
                android_lancher_icon = android_obj.get("android_lancher_icon")
        if not android_lancher_icon:
            logger.warning("【pad支持】config.json android_lancher_icon 配置不存在或者为空！")
            return
        if android_lancher_icon.lower() == "true":
            # 进行 androidmanifest.xml文件操作
            android_manifest_xml_file_path = os.path.join(workspace, "app/AndroidManifest.xml")
            logger.debug("AndroidManifest.xml 文件路径为：【%s】" % android_manifest_xml_file_path)
            try:
                root_xml = parse(android_manifest_xml_file_path)
                root = root_xml.getroot() #获取根节点

                # 由于 xpath对于转义字符支持不友好，对于 {http://schemas.android.com/apk/res/android}name 这种不容易解析
                # 通过 遍历所有 activity 来查找  属性名为.LoadDexActivity或者.SplashActivity的节点
                activity_nodes = root.xpath("/manifest/application/activity")
                if activity_nodes:
                    # 获取xml的命名空间dict。使用QName设置带有命名空间的属性值
                    xml_namespace_dict = root.nsmap
                    if "android" not in xml_namespace_dict:
                        message = 'manifest的命名空间中没有包含android'
                        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
                        raise Exception(message)
                    for activity in activity_nodes:
                        activity_attribute_name = QName(xml_namespace_dict["android"], "name")
                        activity_name = activity.attrib[activity_attribute_name]
                        if activity_name == '.SplashActivity' or activity_name == '.LoadDexActivity':
                            logger.debug("横屏配置支持 /manifest/application/activity name =【%s】" % activity_name)
                            activity_attribute_screenOrientation = QName(xml_namespace_dict["android"],
                                                                         "screenOrientation")
                            activity.attrib[activity_attribute_screenOrientation] = "landscape"
                root_element = ElementTree(root)
                root_element.write(android_manifest_xml_file_path, pretty_print=True, xml_declaration=True,
                                   encoding='utf-8')
            except Exception as e:
                logger.error(LoggerErrorEnum.UNKNOWN_ERROR, 'AndroidManifest.xml android_lancher_icon 修改异常 %s' % e)
                traceback.print_exc()
                sys.exit(1)
        logger.info("【pad支持】config.json android_lancher_icon 配置【%s】" % android_lancher_icon)
        logger.info(" 查看pad支持结束")

    def reform_config(self, config_json):
        obj = {}
        map = {}
        build_config = BuildConfig(os.path.join(os.getcwd(), 'target'))
        build_config_json = build_config.read_build_config()
        android_app_json_keyset = build_config_json["android_app_json_keyset"]
        # 需要从target/	build_config.json 直接拷贝到app.json的数据
        android_app_json_build_keyset = build_config_json["android_app_json_build_keyset"]
        for build_key in android_app_json_build_keyset:
            obj[build_key] = build_config_json[build_key]

        for object in android_app_json_keyset:
            map[object] = object

        for config_key in config_json:
            if not map.get(config_key):
                continue
            elif config_key.lower() == "android":
                arr = config_json[config_key]
                if arr:
                    android_object = arr[0]
                    version_min_sdk = get_min_version_android(build_config_json, android_object.get("versionMinSdk"))
                    version_min_dict = {
                        "versionMinSdk": str(version_min_sdk)
                    }
                    obj[config_key] = version_min_dict
            else:
                if config_key == "pkgid" and config_json[config_key] == "":
                    # 2018-01-16 add pkgid by lianguoqing
                    obj[config_key] = config_json.get("appid")
                else:
                    obj[config_key] = config_json[config_key]
        if not obj.get("pkgid"):
            obj["pkgid"] = config_json.get("appid")
        support_private_host(build_config_json, obj)
        # ./app_factory/app/app.json路径
        app_json_file = os.path.join(os.getcwd(), "app/assets/app_factory/app/app.json")
        obj_content = json.dumps(obj, ensure_ascii=False)
        write_content_to_file(app_json_file, obj_content)



    def _apk_compress(self, variables_dict):
        """
        安卓应用apk压缩优化:向app-factory-product.gradle文件中写入信息
        :param variables_dict:
        :return:
        """
        sb = "\r\nandroid {\r\n" + "    defaultConfig {\r\n"

        build_alias_array = []
        languages_arr = variables_dict["languages"]
        all_languages = variables_dict["allLanguages"]
        for language_obj in all_languages:
            if isinstance(language_obj, dict):
                name = language_obj.get("name")
                if name in languages_arr:
                    build_alias_json = language_obj.get("build_alias")
                    build_alias = build_alias_json.get("android")
                    build_alias_array.append(build_alias)

        languages_array_str = json.dumps(build_alias_array, ensure_ascii=False)
        languages = languages_array_str[1:len(languages_array_str) - 1]
        sb += "        resConfigs "
        sb += languages + "\r\n"
        sb += "    }" + "\r\n"
        sb += "}"

        # 将sb的内容写入到app-factory-product.gradle中
        gradle_file_path = os.path.join(os.getcwd(), "app/app-factory-product.gradle")
        with open(gradle_file_path, "a", encoding='utf-8') as f:
            f.write(sb)
        return True


    def _write_jssdk_file(self, variables_dict):
        """
        组件中定义的extensions -> sdk -> js-sdk 的内容解析，写入 ./..../nd_sdk.json
        :param variables_dict:
        :return:
        """
        app_type = variables_dict["build_app_type"]
        js_sdk_file_path = os.path.join(os.getcwd(), "app/assets/app_factory/app/nd_sdk.json")

        biz_define_map = {}
        define_json_file = os.path.join(os.getcwd(), "target/defines.json")
        define_str = read_file_content(define_json_file)
        define_json = json.loads(define_str)

        return_json = {}
        for define_key in define_json:
            define_value = define_json[define_key]
            extensions = define_value.get("extensions", {})
            if not extensions:
                continue
            sdk = extensions.get("sdk", {})
            if not sdk:
                continue
            jssdk = sdk.get("js-sdk", {})
            if not jssdk:
                continue
            name = jssdk.get("name")
            version = jssdk.get("version")

            json_object = {
                "version": version
            }
            plat_form = jssdk.get(app_type, {})
            if plat_form:
                for plat_form_key in plat_form:
                    plat_form_value = plat_form[plat_form_key]
                    json_object[plat_form_key] = plat_form_value

            return_json[name] = json_object

        # 写入nd_sdk.json文件
        write_content_to_file(js_sdk_file_path, json.dumps(return_json, ensure_ascii=False))

