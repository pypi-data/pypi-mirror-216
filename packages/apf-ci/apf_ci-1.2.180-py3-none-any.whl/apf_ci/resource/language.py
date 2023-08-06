#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" a language module """

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *
from apf_ci.resource.cache_service import CacheService

class LanguageResource:
    def __init__(self, target_path, variables_json):
        self.target_path = target_path
        self.variables_json = variables_json

    def _get_app_language_info(self):
        app_language_info = []

        languages_array = self.variables_json['languages']
        all_languages_json_array = self.variables_json['allLanguages']
        for languages_json in all_languages_json_array:
            language_name = languages_json['name']
            if language_name in languages_array:
                app_language_info.append(languages_json)

        return app_language_info

    def get_language_resources(self, download_type=None, app_language_array=None):
        return self.get_language_resources_array(app_language_array, download_type)


    def get_language_resources_array(self, app_language_array=None, download_type=None):
        storage_host = self.variables_json['app_native_storage']
        factory_id = self.variables_json['factoryId']
        app_type = self.variables_json['build_app_type']

        if app_language_array is None:
            app_language_array = self._get_app_language_info()
            self.variables_json['app_language_array'] = app_language_array

        download_language_array = {}
        for app_language_json in app_language_array:
            build_alias = app_language_json["build_alias"]
            language_name = build_alias[app_type.lower()];
            id = app_language_json["id"]

            language_resource_url = '%s/v0.8/apps/%s/%s' % (storage_host, factory_id, id)
            language_resources_array = get_data(language_resource_url)

            if download_type is None:
                file_name = 'language_%s.txt' % app_language_json['name']
                language_path = os.path.join(self.target_path, file_name)
                write_content_to_file(language_path, json.dumps(language_resources_array))
            download_language_array[language_name] = language_resources_array

        return download_language_array

    def download_language(self, app_type, language_name, language_resources_array, download_type, language_temp_path):
        logger.info('开始donwload language')

        # 轻应用语言资源集合（key为资源包下载的最终路径，value为资源包下载的源路径）
        lite_app_dict = {}

        url_path_array = []
        if language_temp_path is None:
            language_temp_path = os.path.join(self.target_path, 'languageTemp')

        for language_resource_json in language_resources_array:
            items_json_array = language_resource_json["items"]
            namespace = language_resource_json["namespace"]
            biz_name = language_resource_json["biz_name"]
            key = '%s###%s###%s' % (namespace, biz_name, language_name)

            for item_json in items_json_array:
                component_type = item_json["component_type"]

                if download_type is None or download_type == component_type:
                    os_type = item_json["os_type"]

                    if app_type.lower() == os_type.lower() or os_type.lower() == 'all':
                        resource_url = item_json["resource_url"]
                        is_overdue = item_json["is_overdue"]

                        if is_overdue is False:
                            custom_resource_url = item_json["custom_resource_url"]
                            if not (custom_resource_url is None) and custom_resource_url.strip():
                                resource_url = custom_resource_url

                        if resource_url.strip():
                            file_name = key + '.zip'
                            download_path = os.path.join(language_temp_path, component_type, file_name)
                            logger.debug('从%s\n下载资源包到：%s' % (resource_url, download_path))

                            if component_type == 'h5' or component_type == 'react':
                                lite_app_dict[download_path] = resource_url

                            url_path_json = {}
                            url_path_json[resource_url] = download_path
                            url_path_array.append(url_path_json)
                        else:
                            logger.debug('语言包地址为空，无法下载资源: %s' % key)

        multi_download_pool(url_path_array)
        logger.info('donwload language完毕')

        self.variables_json['liteAppLanguageJson'] = lite_app_dict

        if download_type is not None:
            variables_path = os.path.join(self.target_path, 'variables.json')
            write_content_to_file(variables_path, json.dumps(self.variables_json, ensure_ascii=False))

    def __init_language_resource_array_validate(self, language_resources_array, download_type, language_name, app_type):
        """
        初始化，筛选符合条件的资源数组。
        :param skin_resources_array:
        :param download_type:
        :param app_type:
        :return:
        """
        language_validate_array = []

        for language_resource_json in language_resources_array:
            items_json_array = language_resource_json["items"]
            namespace = language_resource_json["namespace"]
            biz_name = language_resource_json["biz_name"]
            key = '%s###%s###%s' % (namespace, biz_name, language_name)
            if not items_json_array:
                continue
            for item_json in items_json_array:
                component_type = item_json["component_type"]

                if download_type is None or download_type == component_type:
                    os_type = item_json["os_type"]

                    if app_type.lower() == os_type.lower() or os_type.lower() == 'all':
                        resource_url = item_json["resource_url"]
                        is_overdue = item_json["is_overdue"]

                        if is_overdue is False:
                            custom_resource_url = item_json["custom_resource_url"]
                            if not (custom_resource_url is None) and custom_resource_url.strip():
                                resource_url = custom_resource_url
                            language_validate_dict = {}
                            language_validate_dict["key"] = key
                            language_validate_dict["namespace"] = namespace
                            language_validate_dict["biz_name"] = biz_name
                            language_validate_dict["component_type"] = component_type
                            language_validate_dict["os_type"] = os_type
                            language_validate_dict["resource_url"] = resource_url
                            language_validate_array.append(language_validate_dict)
        return language_validate_array

    def language_resource_cache_handle(self, language_resources_array, language_name, download_type):
        logger.info('开始donwload language')
        language_temp_path = os.path.join(self.target_path, 'languageTemp')

        # 轻应用语言资源集合（key为资源包下载的最终路径，value为资源包下载的源路径）
        lite_app_dict = {}
        app_type = self.variables_json['build_app_type']

        # 下载池、解压池、拷贝池
        cache_service = CacheService(app_type)
        download_pool_array = []  # download_pool_array[resource_url] = zip_file_path
        copy_pool_array = []      # copy_json["source_path"] = source_path

        language_validate_array = self.__init_language_resource_array_validate(language_resources_array, download_type, language_name, app_type)
        for language_json in language_validate_array:
            key = language_json["key"]
            namespace = language_json["namespace"]
            biz_name = language_json["biz_name"]
            component_type = language_json["component_type"]
            os_type = language_json["os_type"]
            resource_url = language_json["resource_url"]

            if resource_url.strip():
                base_path = cache_service.base_path

                # 解析url，时间戳
                timestamp = "default"
                url_filename_index = resource_url.rfind("/") + 1
                # url中的文件名，取 "_"的位置和 "."位置来截取出时间戳。
                # begin_index > 0 时,表示有找到"_"，begin != end 则取 begin:end的字符串。begin = end 则取系统时间戳（_.zip的情况）
                # begin_index = 0 时,表示没有找到"_"，end >= 1 则取 begin:end的字符串（1.zip的情况）。
                # begin_index = 0 时,表示没有找到"_"，end = 0 则取系统时间戳（.zip的情况）。
                url_filename = resource_url[url_filename_index:]
                begin_index = url_filename.rfind("_") + 1
                end_index = url_filename.rfind(".")
                if begin_index > 0:
                    if begin_index != end_index:
                        timestamp = url_filename[begin_index:end_index]
                    else:
                        timestamp = int(round(time.time() * 1000))
                elif begin_index == 0:
                    if end_index >= 1:
                        timestamp = url_filename[begin_index:end_index]
                    else:
                        timestamp = int(round(time.time() * 1000))

                file_name = key + '.zip'
                cache_path = os.path.join(base_path, "language", namespace, biz_name, os_type, language_name,
                                          component_type, timestamp)

                download_path = os.path.join(cache_path, file_name)

                # 资源分析、过滤
                cache_service.resource_url_analysis(resource_url, cache_path, file_name, component_type,
                                                    download_pool_array)
                logger.debug('【语言包下载】缓存位置：%s  component类型： %s' % (download_path, component_type))

                if component_type == 'h5' or component_type == 'react':
                    logger.debug("【h5 react 语言包下载】 下载位置：%s \n地址：%s" % (download_path, resource_url))
                    h5_react_path = os.path.join(language_temp_path, component_type, file_name)
                    lite_app_dict[h5_react_path] = resource_url

                # H5和react类型的资源 不用拷贝缓存。
                copy_json = {}
                copy_json["source_path"] = download_path
                copy_json["file_name"] = file_name
                copy_json["component_type"] = component_type
                copy_pool_array.append(copy_json)
            else:
                logger.debug('【语言包下载】语言包地址为空，无法下载资源: %s' % key)

        self.variables_json['liteAppLanguageJson'] = lite_app_dict

        if download_type is not None:
            variables_path = os.path.join(self.target_path, 'variables.json')
            write_content_to_file(variables_path, json.dumps(self.variables_json, ensure_ascii=False))

        # logger.debug("language download before: download_pool_array => %s" % download_pool_array)
        # logger.debug("copy_pool_array => %s" % copy_pool_array)
        logger.info(' 语言资源缓存处理language_resource_cache_handle 完毕')
        return download_pool_array, copy_pool_array

if __name__ == "__main__":
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')

    variables_path = os.path.join(target_path, 'variables.json')
    variables_data = read_file_content(variables_path)
    variables_json = json.loads(variables_data)

    download_type = 'react'

    language_resource = LanguageResource(target_path, variables_json)
    language_resource.get_language_resources(download_type)
    #language_resource.unzip_language()
