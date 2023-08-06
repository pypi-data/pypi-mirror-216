#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
App颗粒控件对接翻译门户。
颗粒插件支持多语言化，需要从翻译平台下载国际化的widget语言资源。
需求来源：redmine #9940 移动端：cmk
author: pyf
"""
from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.mac_token_utils import gen_mac_authorization_v11

from apf_ci.util.file_utils import read_file_content, download_cs_file
from apf_ci.util.upload_utils import *


class MultiLanguageResourceBuilder:
    def __init__(self):
        pass

    def widget_language_resource_perform(self, widgets_json_arr, languages_array, factory_id, widget_module_json,
                                         cs_config, plugin_component_id_dir, variables_json):
        # 遍历 widget_json_arr，用于获取各个weiget对应的Npm版本号
        widgets_npm_json = self.get_widget_npm_json(widgets_json_arr)

        # 根据npm 去移动组件服务查询lang_version
        widgets_language_version_json = self.component_service_to_query_language_version(widgets_npm_json, cs_config,
                                                                                         variables_json)

        # 前提条件1：应用支持的语言数组 languages_array
        # 前提条件2：tenant_id 对于构建来说，等于 factory_id
        # 前提条件3：module_id。 widget_module_json 已获取
        # 前提条件4：widgets_name 和 lang_version。 widgets_language_version_json 已获取
        # 根据已知参数条件，向颗粒资源平台获取widget的各个语言资源（用的是颗粒资源服务生产环境的接口）
        # 移动应用语言资源查询 [POST] /v0.1/widgets/language/app/query
        language_result_arr = self.query_widget_language_app_resource(languages_array, factory_id, widget_module_json,
                                                                      widgets_language_version_json, cs_config,
                                                                      variables_json)

        # 对获取到的资源数据，依次下载到/target/language_temp/widget/{plugin_Mame}目录下
        self.download_widget_language(language_result_arr, plugin_component_id_dir)

    # 调用 翻译资源接口 前的准备方法。可获得module_id
    def get_widget_module_id_json(self, app_language_list):
        """
        遍历widget.json，取出每个widget对应的ModuleId。供后续下载颗粒语言资源使用。
        1、获取app语言列表，遍历各个语言下的widget.json，取出每个widget对应的moduleId。
        2、整理语言最终数据结构为： (这里的module_id就是每个widget下的 _module_properties中的 id 字段)
        widget_module_json = {
                                {language} : {
                                    "module_id":[
                                        widget_name , widget_name , widget_name
                                    ],
                                    "module_id":[ ... ]
                                },
                                {language} : { ... },
                                ...
                            }
        :param app_language_list: app语言列表。从variables_json中获取
        :return: widget_module_json
        """
        logger.debug(" multi_resource 开始获取widget module id. 应用语言列表为：%s" % app_language_list)
        workspace_path = os.getcwd()
        app_factory_path = os.path.join(workspace_path, "app", "assets", "app_factory")

        # 最终返回结果json
        widget_module_json = {}

        for language_json in app_language_list:
            language = language_json.get("name")
            # 各语言下的widgets.json路径
            widget_json_path = os.path.join(app_factory_path, language, "pages", "widgets.json")
            widget_json = json.loads(read_file_content(widget_json_path))

            widget_element_dict = {}
            # 遍历widget json数据。取 "widget_name" 和 "properties -> _module_properties -> id"
            for widget_key in widget_json:
                widget_value = widget_json[widget_key]

                widget_name = widget_value.get("widget_name")
                # 校验json节点是否为null
                properties = widget_value.get("properties")
                if not properties:
                    logger.debug(" multi_resource widget.json的 key:%s ，properties节点为空" % widget_key)
                    continue
                module_properties = properties.get("_module_properties")
                if not module_properties:
                    logger.debug(" multi_resource widget.json的 key:%s ，_module_properties节点为空" % widget_key)
                    continue
                module_id = module_properties.get("id", "")

                # 判断module_id是否已经在数据结构中
                if module_id not in widget_element_dict.keys():
                    widget_element_dict[module_id] = []
                widget_element_dict[module_id].append(widget_name)

            # 包装好了一个语言下的 widget -> module
            widget_module_json[language] = widget_element_dict
            logger.debug(" 语言【%s】下的widget-module数据为：%s" % (language, widget_element_dict))
        logger.info(" multi_resource 结束获取widget module id")
        return widget_module_json

    # 调用 翻译平台接口 前的准备方法。可获得widget 和 npm 版本号
    def get_widget_npm_json(self, widgets_json_arr):
        """
        遍历 widget_json_arr，用于获取各个weiget对应的Npm版本号。
        :param widgets_json_arr: 每一个widget_plugin中的widgets数组。大概内容如下：
                                widgets:[
                                            {
                                                "namespace": "com.nd.sdp.widget",
                                                "biz_name": "appcommonwidget",
                                                "version": "release",
                                                "npm": "@app.react.widget.sdp.nd/image_left-item:0.0.35"
                                                "widget_name": "image_left-item"
                                            },
                                            {...}
                                        ]
        :return:返回结果数据结构为：
                widget_npm_json = {
                                    "widget_name": "npm版本号",
                                    "widget_name": "npm版本号",
                                    ...
                                 }
        """
        # 最终返回结果json
        widget_npm_json = {}

        logger.debug(" multi_resource 开始获取widget npm version， 遍历的widget列表为: %s" % widgets_json_arr)
        for widget_info_json in widgets_json_arr:
            npm = widget_info_json.get("npm", "")
            npm_split_list = npm.split(":")
            # [0]左边需要再次分割"/"号,去斜杠右边部分。
            widget_sdp_nd_widgetname = npm_split_list[0]
            # 20190426 widget_name使用解析analysis_page_builder出来，而不是使用npm版本中的widgetName，
            # 因为widget_name可能存在alias的情况
            widget_name = widget_info_json.get("widget_name", "")
            # [1]右边为 npm 版本号 or tag号
            npm_version = npm_split_list[1]

            # 使用Npm的名称从Npm info中获取它的版本号。
            npm_info_command = ['npm', 'info', '%s@%s' % (widget_sdp_nd_widgetname, npm_version), 'version']
            logger.debug(" 执行命令：%s" % npm_info_command)
            npm_version = execute_command(npm_info_command).replace("\n", "")
            logger.debug(" 获取npm version 为：%s" % npm_version)

            widget_npm_json[widget_name] = npm_version
        logger.debug(" multi_resource 结束获取widget npm version，获取的widget_npm结果为：%s" % widget_npm_json)
        return widget_npm_json

    # 调用 翻译平台接口
    def component_service_to_query_language_version(self, widgets_npm_json, cs_config, variables_json):
        """
        向 移动组件服务 根据widget的npm版本查询对应语言的版本号 language_version
        :param variables_json:
        :param cs_config:
        :param widgets_npm_json:
        :return: 返回结果为： widgets_language_version = {
                                " widget_name " : "language_version"
                            }
        """
        logger.info(" multi_resource 开始从移动组件获取language_version")
        # 最终返回结果json
        widgets_language_version_json = {}
        # 移动组件域名获取
        component_mng_host = variables_json["component_mng"]
        logger.info(" multi_resource 移动组件域名 component_mng :%s" % component_mng_host)

        # 调用移动服务之前，需要生成一个 BearToken
        access_token = get_uc_token(cs_config)

        # key 为 widgets_name， value 为 npm版本号
        for widgets_name in widgets_npm_json:
            npm_version = widgets_npm_json[widgets_name]
            # 构建端type写死为app
            widget_type = "app"

            # 调用http://component-mng.sdp.101.com 移动组件服务接口 (统一用生产环境的数据，因为debug环境没有widget数据)
            # [GET] /v0.1/widget_language
            # [Args] type、widget_name、npm_version
            get_restful_url = component_mng_host + "v0.1/widget_language"
            querystring = {"type": widget_type, "widget_name": widgets_name, "npm_version": npm_version}
            headers = {
                'Authorization': "Bearer " + access_token,
            }
            logger.debug(" multi_resource 向移动组件查询颗粒的language_version: %s" % get_restful_url)
            logger.debug(" multi_resource 参数为: %s" % querystring)
            logger.debug(" multi_resource headers为: %s" % headers)

            response_result = requests.request("GET", get_restful_url, headers=headers, params=querystring)
            if not response_result or not response_result.content:
                logger.warning(" 【%s】请求移动组件的颗粒版本有误。请确认上面的url和参数。" % widgets_name)
            else:
                result_json = json.loads(response_result.content.decode('utf-8'))
                logger.debug(" multi_resource 获取的颗粒版本结果为：%s" % result_json)

                # 塞入存储结果的Json中
                if result_json.get("language_version"):
                    widgets_language_version_json[widgets_name] = result_json.get("language_version", "")
        logger.debug(" multi_resource 结束从移动组件获取 widgets_language_version_json: %s" % widgets_language_version_json)
        return widgets_language_version_json

    def query_widget_language_app_resource(self, languages_array,
                                           factory_id,
                                           widget_module_json,
                                           widgets_language_version_json,
                                           cs_config, variables_json):
        """
        # 根据已知参数条件，向颗粒资源平台获取widget的各个语言资源（用的是颗粒资源服务生产环境的接口）
        # 移动应用语言资源查询 [POST] /v0.1/widgets/language/app/query
        :param variables_json:
        :param cs_config:
        :param languages_array:
        :param factory_id:
        :param widget_module_json:
        :param widgets_language_version_json:
        :return: 返回资源服务提供的widget 语言资源，结构如下：
            {
                "zh-CN": {
                    "widget_name": "URL" -- 对应的翻译资源CS文件地址
                    "widget_name": ....
                },
                "{language}": ...
            }
        """
        logger.debug(
            " multi_resource 开始获取颗粒语言资源的数据。factory_id: %s, languages_array:%s " % (factory_id, languages_array))
        #
        widget_i18n_store_host = variables_json["widget_i18n_store"]
        logger.debug(" multi_resource 颗粒多语言平台域名 widget_i18n_store: %s" % widget_i18n_store_host)

        # app支持的语言数组 多语言用","隔开
        languages_array_splicing = ""
        for language_json in languages_array:
            languages_array_splicing += language_json.get("name") + ","
        if not languages_array_splicing:
            logger.warning(" 没有支持的语言，请确认 languages_array")

        # 调用颗粒资源平台的接口，参数的结构为：
        # {
        # 	"language":"zh-CN,en",
        # 	"tenant_id":"78005472-dbf4-4436-9792-4a63106b6dc1",
        # 	"module_id":"8f8373c2-2650-44b0-a5b2-02f152105387",
        # 	"widgets":[
        # 		{
        # 			"widget_name":"motiondiarywidget",
        # 			"lang_version":1
        # 		},
        # 		{}....
        # 	]
        # }
        # 去掉字符串最后一个逗号
        # 1、language 参数
        languages_array_str = languages_array_splicing[0:len(languages_array_splicing) - 1]
        # 2、tenant_id 参数
        tenant_id = factory_id
        # 3、module_id 参数 ，需要for循环遍历。
        # 以moduleid为隔离，获取module下widget所有语言资源地址。
        # 各个语言下的Moduleid是一样的，所以只需要取第一个语言下的moduleid即可
        module_json = {}
        for language_key in widget_module_json:
            # value 为 module对象
            module_json = widget_module_json[language_key]
            break

        # 颗粒资源请求结果
        widgets_language_result_arr = []

        for module_id in module_json:
            # key是module_id value是widgetName数组
            widgets_name_arr = module_json[module_id]

            # widget 参数数组：
            widget_args_arr = []
            for widget_name in widgets_name_arr:
                # 从 widgets_language_version_json中 获取language_version
                if widget_name not in widgets_language_version_json.keys():
                    logger.warning(" 该widgetname在移动组件没有获取到对应的language_version。 widget: %s" % widget_name)
                    continue
                language_version = widgets_language_version_json[widget_name]

                widget_lang_version_json = {
                    "widget_name": widget_name,
                    "lang_version": language_version
                }
                widget_args_arr.append(widget_lang_version_json)
                # 若widget_args_arr为空，则表示没有widgetName需要查询语言资源。直接Continue
            if not widget_args_arr:
                continue

            # 调用移动应用语言资源查询
            # [POST] /v0.1/widgets/language/app/query
            post_url = widget_i18n_store_host + "v0.1/widgets/language/app/query"
            mac_authorization = gen_mac_authorization_v11(cs_config, post_url, "POST")

            # 开始构造接口参数
            post_args = {
                "language": languages_array_str,
                "tenant_id": factory_id,
                "module_id": module_id,
                "widgets": widget_args_arr
            }
            post_args = json.dumps(post_args)

            headers = {
                'Content-Type': "application/json",
                'Authorization': mac_authorization,
            }
            logger.debug(" multi_resource 请求颗粒资源的url: %s" % post_url)
            logger.debug(" multi_resource 请求颗粒资源的body: %s" % post_args)
            logger.debug(" multi_resource 请求颗粒资源的headers: %s" % headers)

            response_result = requests.request("POST", post_url, data=post_args, headers=headers)
            if not response_result or not response_result.content:
                logger.warning(" 【%s】请求颗粒资源有误。请确认上面的url和参数。" % module_id)
            else:
                result_json = json.loads(response_result.content.decode('utf-8'))
                logger.debug(" multi_resource 获取的颗粒版本结果为：%s" % result_json)
                # 向结果中增加module_id作为区分语言的标识（有可能不同Module_id，但下载的链接是一样的。需要区分）
                result_json["module_id"] = module_id

                widgets_language_result_arr.append(result_json)
        logger.info(" multi_resource 结束获取颗粒语言资源的数据")
        return widgets_language_result_arr

    def download_widget_language(self, language_result_arr, plugin_component_id_dir):
        """
        下载widget语言资源到	languageTemp/widget/{plugin_name}目录下
        :param plugin_component_id_dir: pluginName
        :param language_result_arr: 颗粒资源平台返回的数据
        :return:
        """
        logger.debug(" multi_resource 开始下载颗粒语言资源 language_result_arr: %s" % language_result_arr)
        language_temp_path = os.path.join(os.getcwd(), "target", "languageTemp")
        widget_language_path = os.path.join(language_temp_path, "widget", plugin_component_id_dir)
        if not os.path.exists(widget_language_path):
            os.makedirs(widget_language_path)

        for language_resource_json in language_result_arr:
            module_id = language_resource_json["module_id"]
            # key 为 语言，value为 {widget: url}
            for language_key in language_resource_json:
                widget_language_resource = language_resource_json[language_key]
                for widget_name in widget_language_resource:
                    # 过滤掉key是module_id的情况
                    if not isinstance(widget_language_resource, dict):
                        continue
                    resource_url = widget_language_resource[widget_name]

                    # 文件格式命名： {widgetName}###{language}###language.json
                    language_resource_file_name = widget_name + "###" + module_id + "###" + language_key + ".json"
                    language_resource_file_path = os.path.join(widget_language_path, language_resource_file_name)
                    download_cs_file(resource_url, language_resource_file_path, 3)
                    logger.debug(" 下载文件 %s 到 %s" % (language_resource_file_name, language_resource_file_path))
        logger.info(" multi_resource 结束下载颗粒语言资源")




