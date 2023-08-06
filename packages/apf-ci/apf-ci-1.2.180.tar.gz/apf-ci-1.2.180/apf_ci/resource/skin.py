#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" a skin module """

__author__ = 'LianGuoQing'

from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *
from apf_ci.resource.cache_service import CacheService


class SkinResource:
    def __init__(self, target_path, variables_json):
        self.target_path = target_path
        self.variables_json = variables_json

    def get_skin_resources(self, download_type=None):
        resource_host = self.variables_json['fac_resource_manage']
        skin_config_url = '%s/v0.1/resconfig/skin' % resource_host
        skin_config_array = get_data(skin_config_url)
        if skin_config_array.__len__ == 0:
            error_msg = '【error】皮肤资源类型未配置，请联系管理员进行配置管理！'
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_msg)
            raise Exception()
            sys.exit(1)

        skin_config_id = skin_config_array[0]['id']
        self.variables_json['skinResourceId'] = skin_config_id

        storage_host = self.variables_json['app_native_storage']
        factory_id = self.variables_json['factoryId']
        skin_resource_url = '%s/v0.8/apps/%s/%s' % (storage_host, factory_id, skin_config_id)
        skin_resources_array = get_data(skin_resource_url)

        if download_type is None:
            skins_path = os.path.join(self.target_path, 'skins.txt')
            write_content_to_file(skins_path, json.dumps(skin_resources_array))

        return skin_resources_array

    def download_skin(self, skin_resources_array, download_type):
        logger.info('开始donwload skin')

        # 轻应用皮肤资源集合（key为资源包下载的最终路径，value为资源包下载的源路径）
        lite_app_dict = {}

        url_path_array = []
        skin_temp_path = os.path.join(self.target_path, 'skinTemp')
        app_type = self.variables_json['build_app_type']

        for skin_resource_json in skin_resources_array:
            namespace = skin_resource_json["namespace"]
            biz_name = skin_resource_json["biz_name"]
            key = '%s###%s' % (namespace, biz_name)

            items_json_array = skin_resource_json["items"]
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
                            download_path = os.path.join(skin_temp_path, component_type, file_name)
                            logger.debug('【皮肤包下载】从%s\n下载资源包到：%s' % (resource_url, download_path))

                            if component_type == 'h5' or component_type == 'react':
                                lite_app_dict[download_path] = resource_url

                            url_path_json = {}
                            url_path_json[resource_url] = download_path
                            url_path_array.append(url_path_json)
                        else:
                            logger.debug('【皮肤包下载】皮肤地址为空，不下载资源: %s' % key)

        multi_download_pool(url_path_array)
        logger.info('donwload skin完毕')

        self.variables_json['liteAppSkinJson'] = lite_app_dict


    def __init_skin_resource_array_validate(self, skin_resources_array, download_type, app_type):
        """
        初始化，筛选符合条件的资源数组。
        :param skin_resources_array:
        :param download_type:
        :param app_type:
        :return:
        """
        skin_validate_array = []

        for skin_resource_json in skin_resources_array:
            namespace = skin_resource_json["namespace"]
            biz_name = skin_resource_json["biz_name"]
            key = '%s###%s' % (namespace, biz_name)

            items_json_array = skin_resource_json["items"]
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
                            skin_validate_dict = {}
                            skin_validate_dict["key"] = key
                            skin_validate_dict["namespace"] = namespace
                            skin_validate_dict["biz_name"] = biz_name
                            skin_validate_dict["component_type"] = component_type
                            skin_validate_dict["os_type"] = os_type
                            skin_validate_dict["resource_url"] = resource_url
                            skin_validate_array.append(skin_validate_dict)
        return skin_validate_array

    def skin_resource_cache_handle(self, skin_resources_array, download_type):
        logger.info('开始 资源缓存处理resource cache handle')
        # 轻应用下载地址
        skin_temp_path = os.path.join(self.target_path, 'skinTemp')

        # 轻应用皮肤资源集合（key为资源包下载的最终路径，value为资源包下载的源路径）
        lite_app_dict = {}
        app_type = self.variables_json['build_app_type']

        # 下载池、拷贝池
        cache_service = CacheService(app_type)
        download_pool_array = []    # download_pool_array[resource_url] = zip_file_path
        copy_pool_array = []        # copy_json["source_path"] = source_path

        skin_validate_array = self.__init_skin_resource_array_validate(skin_resources_array, download_type, app_type)
        for resource_json in skin_validate_array:
            key = resource_json["key"]
            namespace = resource_json["namespace"]
            biz_name = resource_json["biz_name"]
            component_type = resource_json["component_type"]
            os_type = resource_json["os_type"]
            resource_url = resource_json["resource_url"]

            # 判断url是否为""
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

                file_name = key + ".zip"
                cache_path = os.path.join(base_path, "skin", namespace, biz_name, os_type, component_type,
                                          timestamp)

                download_path = os.path.join(cache_path, file_name)

                # 资源分析、过滤
                cache_service.resource_url_analysis(resource_url, cache_path, file_name, component_type,
                                                    download_pool_array)
                logger.debug('【皮肤包下载】缓存位置：%s  component类型： %s' % (download_path, component_type))

                if component_type == 'h5' or component_type == 'react':
                    logger.debug('【h5 react 皮肤包下载】 下载位置：%s \n地址：%s' % (download_path, resource_url))
                    h5_react_path = os.path.join(skin_temp_path, component_type, file_name)
                    lite_app_dict[h5_react_path] = resource_url

                # H5和react类型的资源 不用拷贝缓存。
                copy_json = {}
                copy_json["source_path"] = download_path
                copy_json["file_name"] = file_name
                copy_json["component_type"] = component_type
                copy_pool_array.append(copy_json)
            else:
                logger.debug('【皮肤包下载】皮肤地址为空，不下载资源: %s' % key)

        self.variables_json['liteAppSkinJson'] = lite_app_dict

        # logger.debug(" download_pool_array => %s" % download_pool_array)
        # logger.debug(" copy_pool_array => %s" % copy_pool_array)
        logger.info('语言资源缓存处理skin_resource_cache_handle 完毕')
        return download_pool_array, copy_pool_array


if __name__ == "__main__":
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')

    variables_path = os.path.join(target_path, 'variables.json')
    variables_data = read_file_content(variables_path)
    variables_json = json.loads(variables_data)

    download_type = 'react'

    skin_resource = SkinResource(target_path, variables_json)
    # skin_resource.get_skin_resources(download_type)
    skin_resource.unzip_skin()