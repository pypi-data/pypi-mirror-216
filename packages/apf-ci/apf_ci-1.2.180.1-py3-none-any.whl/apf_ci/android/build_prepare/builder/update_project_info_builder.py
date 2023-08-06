#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from apf_ci.util.file_utils import *
from apf_ci.util.property import *
from lxml.etree import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import BuildConfig
from apf_ci.util.version_utils import get_min_version_android
class UpdateProjectInfoBuilder:
    def __init__(self, version, version_name, package_name, app_name, sdk):
        self.version = version
        self.version_name = version_name
        self.package_name = package_name
        self.app_name = app_name
        self.sdk = sdk

    def perform(self, variables_dict):
        """
        更新项目信息
        :param variables_dict:
        :return:
        """
        logger.info(" 开始do update project info")
        all_languages_array = variables_dict["allLanguages"]
        logger.debug("allLanguagesJson: %s" % all_languages_array)

        self._update_project_info(self.version, self.version_name, self.package_name, self.app_name, self.sdk, all_languages_array)
        logger.info(" do update project info完毕")

    def _update_project_info(self, version, version_name, package_name, app_name, sdk_dir, all_languages_array):
        logger.info(" updateProjectInfo 项目信息更新开始")
        package_id = package_name
        build_config = BuildConfig(os.path.join(os.getcwd(), 'target'))
        app_build = build_config.read_build_config()

        upper_case_package_name_android_array = app_build["upper_case_package_name_android"]
        logger.debug("统一配置中upper_case_package_name_android:%s" % upper_case_package_name_android_array)
        # 确认包名不为空
        if not package_id:
            package_id = "com.nd.android.app." + app_name
        package_id = self._check_package_name(package_id, upper_case_package_name_android_array)

        # 改写local.properties
        version_name_str = version_name.encode("unicode_escape").decode("utf-8")
        keystory_path = "/usr/android/keystore/debug.keystore"
        self._update_local_properties(sdk_dir, package_id, version, version_name_str, keystory_path, app_build)

        # 改写strings.xml
        try:
            self._update_strings_xml(app_name, all_languages_array)
            logger.info(" updateProjectInfo 项目信息更新结束")
        except Exception as e:
            error_message = '代码替换异常 %s' % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)
            traceback.print_exc()
            sys.exit(1)

    def _check_package_name(self, package_id, upper_case_package_name_android_array):
        if package_id not in upper_case_package_name_android_array:
            package_id = package_id.replace("-", "").lower()
            if package_id.startswith("[1-9]"):
                package_id = "n" + package_id
        return package_id

    def _update_local_properties(self, sdk_dir, package_id, version, version_name_str, keystory_path,
                                 app_build):
        """
        更新local.properties文件信息。
        :param sdk_dir:
        :param package_id:
        :param version:
        :param version_name_str:
        :param keystory_path:
        :param default_version_min_sdk_str:
        :return:
        """
        default_version_min_sdk_str = app_build["android_version_min_sdk_default"]
        logger.debug("统一配置中versionMinSdk:%s" % default_version_min_sdk_str)

        factory_dir_path = os.path.join(os.getcwd(), "app/assets/app_factory")
        config_json_path = os.path.join(factory_dir_path, "app/config.json")
        if not os.path.exists(config_json_path):
            logger.warning("app/assets/app_factory/app/config.json 文件不存在 path:%s" % config_json_path)
            return
        json_str = read_file_content(config_json_path)
        config_json = json.loads(json_str)

        property_file_path = os.path.join(os.getcwd(), "local.properties")
        properties = Properties(property_file_path)
        properties.put("sdk.dir", sdk_dir)
        properties.put("want.reset.package.name", package_id)
        properties.put("version.code.str", version)
        properties.put("version.name.str", version_name_str)
        properties.put("debug.keystory.path", keystory_path)

        android_arr = config_json["android"]
        if android_arr:
            android_obj = android_arr[0]
            if android_obj:
                version_min_sdk = get_min_version_android(app_build,android_obj["versionMinSdk"])
                logger.debug(" versionMinSdk = %s" % version_min_sdk)
                #if not version_min_sdk:
                #    version_min_sdk = default_version_min_sdk_str
                properties.put("versionMinSdk", version_min_sdk)

    def _update_strings_xml(self, app_name, all_languages_array):
        """
        改写各个语言包下的strings.xml 和 默认的values/strings.xml
        :param app_name:
        :param all_languages_array:
        :return:
        """
        values_dir_path = os.path.join(os.getcwd(), "app/res/values")
        default_display = app_name
        # 应用名字json
        app_name_json_file_path = os.path.join(os.getcwd(), "target/appNameJson.json")
        if not os.path.exists(app_name_json_file_path):
            logger.warning(" target/appNameJson.json 文件不存在 path:%s" % app_name_json_file_path)
            return

        app_name_json_file_content = read_file_content(app_name_json_file_path)
        app_name_json = json.loads(app_name_json_file_content)

        # 按语言
        for object in all_languages_array:
            if isinstance(object, dict):
                alias = object.get("build_alias", {})

                language = object.get("name", "")
                display = app_name_json.get(language, "")
                # 确认显示名不为空
                if not display:
                    display = app_name

                language = alias.get("android", "")
                if language.lower() == "en":
                    default_display = display
                elif language.lower() == "zh" or language.lower() == "zh-CN":
                    default_display = display

                new_values_dirpath = os.path.join(os.getcwd(), "app/res/values-" + language)
                logger.debug("把文件【%s】拷贝到【%s】" % (values_dir_path, new_values_dirpath))

                # app/res/values/strings.xml路径
                string_path = os.path.join(new_values_dirpath, "strings.xml")
                copy_file(os.path.join(values_dir_path, "strings.xml"), os.path.join(new_values_dirpath, "strings.xml"))
                copy_file(os.path.join(values_dir_path, "styles.xml"), os.path.join(new_values_dirpath, "styles.xml"))

                # 将display的值设置到string.xml的 "/resources/string[@name='app_name_appfactory'"节点值
                self._write_value_strings_xml(string_path, display)
                #####################
                # xml_doc = parse(string_path)
                # per = xml_doc.xpath("/resources/string[@name='app_name_appfactory']")
                # if per:
                #     par_element = per[0]
                #     # 修改节点的text
                #     par_element.text = display
                #     root_element = ElementTree(xml_doc)
                #     # 覆盖原strings.xml文件
                #     root_element.write(string_path, pretty_print=True, xml_declaration=True, standalone=False, encoding='utf-8')
                # else:
                #     logger.warning(" string.xml没有找到 resources/string[@name='app_name_appfactory']，路径: %s " % string_path)

                # 如果是中文的时候，也把string.xml拷贝到 values-zh-rCN 目录下面
                if language.lower() == "zh":
                    logger.debug(" updateProjectInfo 把string.xml拷贝到 values-zh-rCN 目录下面")
                    copy_file(string_path, os.path.join(new_values_dirpath+"-rCN", "strings.xml"))

        # 默认的strings.xml: 添加resource节点的text
        default_string_path = os.path.join(values_dir_path, "strings.xml")
        self._write_value_strings_xml(default_string_path, default_display)

    def _write_value_strings_xml(self, string_path, display):
        """
        重写各个语言下的 {workspace}/app/res/values-XXXX/strings.xml，将display的内容写入到 resource节点的text中
        :param string_path:
        :param display:
        :return:
        """
        root = parse(string_path).getroot()
        # 取string节点的属性名为app_name_appfactory的节点
        per = root.xpath("/resources/string[@name='app_name_appfactory']")
        if per:
            per_element = per[0]
            per_element.text = display
            root_element = ElementTree(root)
            root_element.write(string_path, pretty_print=True, xml_declaration=True, standalone=False, encoding='utf-8')
        else:
            logger.warning(" string.xml没有找到 resources/string[@name='app_name_appfactory']，路径: %s " % string_path)
