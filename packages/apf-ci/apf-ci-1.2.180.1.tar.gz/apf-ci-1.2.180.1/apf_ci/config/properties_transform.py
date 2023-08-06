#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" a PropertiesTransform module """

__author__ = 'LianGuoQing'

import json
import re

from apf_ci.util.file_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger


class PropertiesTransform:
    def __init__(self, target_path, deveice_image_size_mode):
        self.target_path = target_path

        self.template = ''
        self.content = ''
        self.repalce_symbol = '_'
        self.regular = '://|/|\\?|=|\\.|-'
        self.adapter_key = ''
        self.adapter_json_array = None
        self.properties_json = None
        self.app_type = ''
        self.repalce_map = {}
        self.component = {}

        self.model_array = deveice_image_size_mode
        #['default', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi', 'iPhone4', 'iPhone6', 'iPhone6P', 'iPhoneX']

    def set_app_type(self, app_type):
        self.app_type = app_type

    def set_adapter_key(self, adapter_key):
        self.adapter_key = adapter_key

    def set_adapter_json_array(self, adapter_json_array):
        self.adapter_json_array = adapter_json_array

    def set_content(self, content):
        self.content = content

    def set_properties_json(self, properties_json):
        self.properties_json = properties_json

    def set_template(self, template):
        self.template = template

    def set_component(self, component):
        self.component = component

    def search_property(self, search_content):
        pass

    def get_property_prefix(self):
        pass

    def search_by_properties_json(self, search_char):
        property_prefix = self.get_property_prefix()

        if self.properties_json is None:
            return

        for properties_key in self.properties_json:
            replace_str = '%s%s' % (self.repalce_symbol, properties_key)
            replace_str = re.sub(self.regular, self.repalce_symbol, replace_str)

            property_object = self.properties_json[properties_key]
            if isinstance(property_object, str):
                if property_object == search_char:
                    if self.adapter_json_array is not None:
                        rename_file_name = '%s%s' % (property_prefix, replace_str.lower())
                        properties_json_object = self.picture_adapter(rename_file_name)
                        self.properties_json[properties_key] = properties_json_object
                        continue
                    else:
                        if search_char == '' or search_char.replace(' ', '') == '{\"default\":\"\"}':
                            self.properties_json[properties_key] = ''
                            continue

                        substr = search_char[search_char.rfind('.'):]
                        if search_char.rfind('.9.png') > -1:
                            substr = '.9.png'

                        replace_str = '%s%s' % (self.repalce_symbol, properties_key)
                        replace_str = re.sub(self.regular, self.repalce_symbol, replace_str)
                        replace_string = '%s%s%s' % (property_prefix, replace_str.lower(), substr)
                        logger.debug('getPropertyPrefix()前缀：【%s】' % property_prefix)
                        logger.debug('【%s】非数组找到，属性为【%s】' % (search_char, replace_string))

                        self.repalce_map[replace_string] = search_char

                        if replace_string.endswith('.zip'):
                            suffix_format = self.check_zip_file(replace_string, search_char)
                            replace_string = replace_string[0:replace_string.rfind('.zip')]
                            replace_string += suffix_format
                            logger.debug('after=【%s】非数组找到，属性为【%s】' % (search_char, replace_string))

                        self.properties_json[properties_key] = replace_string
                        continue

            elif isinstance(property_object, dict):
                if json.dumps(property_object).replace(' ', '') == search_char.replace(' ', ''):
                    logger.debug('[propertiesJsonString]%s' % property_object)
                    if self.adapter_json_array is not None:
                        rename_file_name = '%s%s' % (property_prefix, replace_str.lower())
                        properties_json_object = self.picture_adapter(rename_file_name)
                        self.properties_json[properties_key] = properties_json_object
                        continue
                    else:
                        default_url = property_object['default']
                        if default_url == '':
                            self.properties_json[properties_key] = ''
                            continue

                        substr = default_url[default_url.rfind('.'):]
                        if default_url.rfind('.9.png') > -1:
                            substr = '.9.png'

                        replace_string = '%s%s%s' % (property_prefix, replace_str.lower(), substr)
                        logger.debug('【%s】找到，属性为【%s】' % (search_char, replace_string))
                        self.repalce_map[replace_string] = default_url
                        self.properties_json[properties_key] = replace_string
                        continue

            elif isinstance(property_object, list):
                if search_char == '':
                    continue

                for i, property_chide_json in enumerate(property_object):
                    if json.dumps(property_chide_json).find(search_char) > -1:
                        # 页面默认使用数组序号
                        page = '%s%s%s' % (self.repalce_symbol, i, self.repalce_symbol)
                        # 属性标示
                        property = ''
                        param = ''
                        findProperties = []

                        if 'param' in property_chide_json.keys():
                            if property_chide_json['param'].__len__() > 0:
                                param = property_chide_json['param']

                        for property_chide_key in property_chide_json:
                            property_chide_value = property_chide_json[property_chide_key]
                            property_value = json.dumps(property_chide_value)

                            if property_value.replace(' ', '') == search_char.replace(' ', ''):
                                property = property_chide_key
                                findProperties.append(property)
                                logger.debug('【%s】第【%s】个item数组找到，属性为【%s】' % (search_char, i, property))

                            is_start = property_value.startswith('"cmp') or property_value.startswith(
                                '"local') or property_value.startswith('"online')
                            if property_chide_key == 'page' and is_start:
                                sub_page_name = property_value[property_value.rfind('/') + 1:property_value.find('?')]
                                page_name = re.sub(self.regular, self.repalce_symbol, sub_page_name)
                                pagename = page_name.lower()

                                data = '%s%s' % (property_chide_value, param)
                                md5_str = get_md5(data)[0:8]
                                page = '%s%s%s%s%s' % (
                                    self.repalce_symbol, md5_str, self.repalce_symbol, page_name, self.repalce_symbol)

                        if len(findProperties) > 0:
                            search_char_temp = search_char
                            for eachFindProperty in findProperties:
                                search_char = search_char_temp
                                property = eachFindProperty
                                if self.adapter_json_array is not None:
                                    rename_file_name = '%s%s%s' % (property_prefix, page, property)
                                    rename_file_name = rename_file_name.lower()
                                    properties_json_object = self.picture_adapter(rename_file_name)
                                    property_chide_json[property] = properties_json_object
                                else:
                                    page_property_str = '%s%s' % (page, property)
                                    page_property_str = re.sub(self.regular, self.repalce_symbol, page_property_str)
                                    page_property_str = page_property_str.lower()
                                    search_char_json = json.loads(search_char)
                                    if isinstance(search_char_json, dict):
                                        search_char = search_char_json['default']
                                        if search_char == '':
                                            property_chide_json[property] = ''
                                            continue

                                        search_char_str = search_char[search_char.rfind('.'):]
                                        if search_char.rfind('.9.png') > -1:
                                            search_char_str = '.9.png'

                                        replace_string = '%s%s%s' % (
                                            property_prefix, page_property_str.lower(), search_char_str)
                                        property_chide_json[property] = replace_string
                                    else:
                                        search_char = search_char.replace('\"', '')

                                        search_char_str = search_char[search_char.rfind('.'):]
                                        if search_char.rfind('.9.png') > -1:
                                            search_char_str = '.9.png'

                                        replace_string = '%s%s%s' % (
                                            property_prefix, page_property_str.lower(), search_char_str)
                                        property_chide_json[property] = replace_string
                                    if replace_string:
                                        self.repalce_map[replace_string] = search_char
                                        #continue

    def check_zip_file(self, file_name, zip_cs_file_path):
        # 取文件名索引
        index = file_name.rfind('/')
        if index == -1:
            # 不带路径的文件索引
            index = 0
        else:
            # 带路径的文件索引
            index += 1

        # 取不带格式的文件名
        folder_name = file_name[index:file_name.rfind('.zip')]
        # 放置zip解压文件的临时路径
        zip_temp_path = os.path.join(self.target_path, 'zipTemp', folder_name)

        zip_file_path = '%s%s' % (zip_temp_path, '.zip')
        logger.debug('下载文件【%s】保存在【%s】' % (zip_cs_file_path, zip_file_path))
        download_cs_file(zip_cs_file_path, zip_file_path, 3)

        unzip(zip_file_path, zip_temp_path)

        zip_temp_folder = os.listdir(zip_temp_path)
        if len(zip_temp_folder) == 3:
            # 主文件名必须完全一致
            check_file_name = ''
            # zip包里的文件格式是否一致，且只能为png或gif或jpg(jpeg)格式
            check_file_format = ''

            for temp_file_name in zip_temp_folder:
                temp_file_path = os.path.join(zip_temp_path, temp_file_name)
                if not os.path.isfile(temp_file_path):
                    error_message = 'zip包内不能存在任何目录:%s ' % temp_file_path
                    logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                    raise Exception(error_message)

            if is_image(temp_file_path) is False:
                error_message = 'zip包内文件可能是非图片文件或者非PNG或GIF或JPG(JPEG)格式图片文件（改后缀名）: %s ' % temp_file_path
                logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                raise Exception(error_message)

            format_index = temp_file_name.rfind('.')
            # 后缀格式：.png、.gif、.jpg、.jpeg
            suffix_format = temp_file_name[format_index:]

            if check_file_format:
                if suffix_format.endswith(check_file_format) is False:
                    error_message = 'zip包内图片文件格式不一致:%s ' % temp_file_path
                    logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                    raise Exception(error_message)
            else:
                check_file_format = suffix_format

            last_index = temp_file_name.rfind('@')
            if last_index == -1:
                temp_file_name = temp_file_name[0:format_index]
            else:
                xx_suffix = '%s%s' % ('@2x', suffix_format)
                xxx_suffix = '%s%s' % ('@3x', suffix_format)

                if temp_file_name.endswith(xx_suffix):
                    temp_file_name = temp_file_name[0:temp_file_name.rfind(xx_suffix)]
                elif temp_file_name.endswith(xxx_suffix):
                    temp_file_name = temp_file_name[0:temp_file_name.rfind(xxx_suffix)]
                else:
                    error_message = 'zip包内部必须包含@2x与@3x后缀的图片文件:%s ' % temp_file_path
                    logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                    raise Exception(error_message)

            if check_file_name:
                if temp_file_name.endswith(check_file_name) is False:
                    error_message = 'zip包内部不含@2x与@3x的情况下主文件名必须完全一致:%s ' % temp_file_path
                    logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                    raise Exception(error_message)
            else:
                check_file_name = temp_file_name

            return check_file_format

        else:
            error_message = 'zip包内部只能放置三张图片:%s ' % zip_file_path
            logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
            raise Exception(error_message)


    def picture_adapter(self, rename_file_name):
        result = ''
        for adapter_json in self.adapter_json_array:

            model = adapter_json['_model']
            if '_value' in adapter_json:
                value = adapter_json['_value']
            else:
                error_message = '组件配置adapter_json配置有误:%s ' % json.dumps(adapter_json)
                logger.error(LoggerErrorEnum.INVALID_ARGUMENT, error_message)
                raise Exception(error_message)
            if value:
                suffix_name = value[value.rfind('.'):]
                if value.rfind('.9.png') > -1:
                    suffix_name = '.9.png'

                replace_str = '%s%s' % (rename_file_name, suffix_name)

                os = adapter_json['_os']
                if os.lower() == 'android':
                    if self.app_type.lower() == os.lower() and replace_str != '':
                        self.repalce_map[model + '@' + replace_str] = adapter_json

                elif os.lower() == 'ios':
                    if model in self.model_array:
                        self.rename(rename_file_name, suffix_name, adapter_json)

                result = replace_str

            else:
                if model in self.model_array:
                    pass

        return result


    def rename(self, rename_file_name, suffix_name, adapter_json):
        is_resizes = False

        model = adapter_json['_model']
        os = adapter_json['_os']

        if '_resize' in adapter_json.keys():
            resizes = adapter_json['_resize']
            resize_arr = resizes.split(',')
            for resize in resize_arr:
                file_name = rename_file_name
                if model != 'default':
                    file_name += '%s%s' % ('@', model)

                if resize.strip().endswith('@2x'):
                    file_name += '@2x'
                elif resize.strip().endswith('@3x'):
                    file_name += '@3x'

                file_name += suffix_name

                if self.app_type.lower() == os.lower() and file_name:
                    replace_json = {}
                    replace_json['_os'] = os
                    replace_json['_value'] = adapter_json['_value']
                    replace_json['_model'] = model
                    replace_json['_resize'] = resize.strip()

                    self.repalce_map[file_name] = replace_json

                is_resizes = True

        if is_resizes is False:
            file_name = rename_file_name
            if model != 'default':
                file_name += '%s%s' % ('@', model)

            file_name += suffix_name

            if self.app_type.lower() == os.lower() and file_name:
                self.repalce_map[file_name] = adapter_json


class PageWidgetTransform(PropertiesTransform):
    def search_property(self, search_content):
        if isinstance(search_content, list):
            search_char = self.adapter_key
            self.set_adapter_json_array(search_content)
        else:
            search_char = json.dumps(search_content)
            self.set_adapter_json_array(None)

        logger.debug('==================【Page】开始查找替换【%s】==============' % search_char)
        content_json = json.loads(self.content)
        for pages_key in content_json:
            page_json = content_json[pages_key]

            if isinstance(page_json, dict):
                if json.dumps(page_json).find(search_char) > -1:
                    for attribute_key in page_json:

                        attribute_value = page_json[attribute_key]
                        if attribute_key == 'properties':
                            self.set_properties_json(attribute_value)
                        elif attribute_key == 'template':
                            self.set_template(attribute_value)

                    self.search_by_properties_json(search_char)

        self.set_content(json.dumps(content_json))

    def get_property_prefix(self):
        template = self.template.lower()

        if template.find('-') > 0:
            template = template.split('-')[0]

        template_main = template[template.rfind('/') + 1:]
        template_main = re.sub(self.regular, self.repalce_symbol, template_main)
        template = re.sub(self.regular, self.repalce_symbol, template)

        md5_str = get_md5(template)[0:8]
        template = '%s_%s' % (template_main, md5_str)

        return template


class BuildTransform(PropertiesTransform):
    def search_property(self, search_content):
        if isinstance(search_content, list):
            search_char = self.adapter_key
            self.set_adapter_json_array(search_content)
        else:
            search_char = json.dumps(search_content)
            self.set_adapter_json_array(None)

        logger.debug('==================【Build】开始查找替换【%s】==============' % search_char)

        content_array = json.loads(self.content)
        for build_json in content_array:
            if json.dumps(build_json).find(search_char) > -1:
                for chide_key in build_json:
                    chide_value = build_json[chide_key]
                    if chide_key == 'properties':
                        self.set_properties_json(chide_value)
                    elif chide_key == 'component':
                        self.set_component(chide_value)

                self.search_by_properties_json(search_char)

        self.set_content(json.dumps(content_array))

    def get_property_prefix(self):
        namespace = self.component['namespace']
        name = self.component['name']

        replace_str = '%s%s%s' % (namespace, self.repalce_symbol, name)
        prefix = re.sub(self.regular, self.repalce_symbol, replace_str.lower())

        return prefix










