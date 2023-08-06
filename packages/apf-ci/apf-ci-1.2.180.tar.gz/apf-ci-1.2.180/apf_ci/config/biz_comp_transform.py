#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
获取i18n和图片属性集合
"""

__author__ = 'LianGuoQing'

import json
from apf_ci.util.log_utils import logger


class BizCompTransform:
    i18n_property_map = {}
    image_property_map = {}
    # 为满足h5颗粒新需求，，存储i18n_property_map数据
    h5_widget_i18n_property_map = {}

    def make_property_map(self, info):
        pass


class BizCompJsonTransform(BizCompTransform):
    def __init__(self, app_type):
        self.app_type = app_type

    def make_property_map(self, defines_json):
        """
        解析defines_json内容，按pages、properties、widgets、extensions节点取出i18n和图片属性集合
        :param defines_json:
        :return:
        """
        for biz_comp_key in defines_json:
            biz_comp_json = defines_json[biz_comp_key]
            namespace = biz_comp_json['namespace']
            biz_name = biz_comp_json['biz_name']

            if 'pages' in biz_comp_json.keys():
                pages_json = biz_comp_json['pages']
                for page_key in pages_json:
                    page_json = pages_json[page_key]
                    if isinstance(page_json, dict):
                        self.make_composited_property_map(namespace, biz_name, 'page', page_json, '')

            if 'properties' in biz_comp_json.keys():
                properties_json = biz_comp_json['properties']
                self.make_composited_property_map(namespace, biz_name, 'properties', properties_json, '')

            if 'widgets' in biz_comp_json.keys():
                widgets_json = biz_comp_json['widgets']
                for widgets_key in widgets_json:
                    widget_json = widgets_json[widgets_key]
                    if 'properties' in widget_json.keys():
                        widget_properties_json = widget_json['properties']
                        self.make_composited_property_map(namespace, biz_name, 'properties', widget_properties_json, '')

            if 'extensions' in biz_comp_json.keys():
                extensions_json = biz_comp_json['extensions']
                if 'runtime' in extensions_json.keys():
                    runtime_json = extensions_json['runtime']
                    if 'properties' in runtime_json.keys():
                        runtime_properties_json = runtime_json['properties']
                        for runtime_properties_key in runtime_properties_json:
                            runtime_property_json = runtime_properties_json[runtime_properties_key]
                            if '_name' in runtime_property_json:
                                name = runtime_property_json['_name']
                                if runtime_property_json['_elementType'] == 'property' and runtime_property_json[
                                    '_type'] == 'image':
                                    key = '%s.%s.properties.%s' % (namespace, biz_name, name)
                                    self.image_property_map[key] = '1'
                                else:
                                    if runtime_property_json['_elementType'] == 'group':
                                        for runtime_property_key in runtime_property_json:
                                            if not runtime_property_key.startswith('_'):
                                                group_property_json = runtime_property_json[runtime_property_key]
                                                if group_property_json['_elementType'] == 'property' and group_property_json['_type'] == 'image':
                                                    key = '%s.%s.properties.%s.%s' % (
                                                    namespace, biz_name, name, group_property_json['_name'])
                                                    self.image_property_map[key] = '1'

    def make_composited_property_map(self, namespace, biz_name, element_type, element, pre_property):
        """
        以起点和最终节点的连接串为key，值为1（多分辨率除外）
        :param namespace:
        :param biz_name:
        :param element_type:
        :param element:
        :param pre_property:
        :return:
        """
        _element_type = ''
        try:
            _element_type = element['_elementType'].lower()
        except KeyError:
            pass

        if _element_type == 'page':
            prefix = '%s%s' % (element['_name'], '.')

            for page_element_key in element:
                if page_element_key.lower() == 'properties':
                    properties_json = element[page_element_key]
                    self.make_composited_property_map(namespace, biz_name, 'properties', properties_json, prefix)

        elif element_type.lower() == 'properties':
            prefix = '%s%s' % (pre_property, 'properties')

            for propertie_key in element:
                if propertie_key.lower() == 'page_display':
                    continue

                propertie_json = element[propertie_key]
                if isinstance(propertie_json, dict):
                    if not '_elementType' in propertie_json:
                        logger.warning('以下业务组件定义有问题：')
                        logger.warning(propertie_json)
                    if propertie_json['_elementType'].lower() == 'group':
                        self.make_composited_property_map(namespace, biz_name, 'group', propertie_json, prefix)
                    elif propertie_json['_elementType'].lower() == 'property':
                        self.make_composited_property_map(namespace, biz_name, 'property', propertie_json, prefix)

        elif _element_type == 'group':
            group_name = element['_name']
            prefix = '%s%s%s' % (pre_property, '.', group_name)

            for propertie_element_key in element:
                propertie_element_json = element[propertie_element_key]
                if isinstance(propertie_element_json, dict):
                    try:
                        if propertie_element_json['_elementType'].lower() == 'property':
                            self.make_composited_property_map(namespace, biz_name, 'property', propertie_element_json,
                                                              prefix)
                    except KeyError:
                        pass

        elif _element_type == 'property':
            is_i18n = False
            try:
                i18n_element = element['_i18n']
                if i18n_element.lower() == 'true':
                    is_i18n = True
            except KeyError:
                pass

            is_image = False
            try:
                type_element = element['_type']
                if type_element.lower() == 'image':
                    is_image = True
            except KeyError:
                pass

            name_element = element['_name']
            key = '%s%s%s%s%s%s%s' % (namespace, '.', biz_name, '.', pre_property, '.', name_element)

            try:
                transfer_element = element['transfer']
                transfer_json_array = []
                if isinstance(transfer_element, dict):
                    transfer_json_array.append(transfer_element)
                elif isinstance(transfer_element, list):
                    transfer_json_array = transfer_element

                is_default = False
                for transfer_json in transfer_json_array:
                    model = ''
                    try:
                        model = transfer_json['_model']
                    except KeyError:
                        is_default = True
                        transfer_json['_model'] = 'default'

                    if model == 'default':
                        is_default = True
                        if transfer_json['_os'].lower() != self.app_type:
                            continue

                if is_default is False:
                    default_json = {}
                    default_json['_model'] = 'default'
                    if self.app_type.lower() == 'android':
                        default_json['_os'] = 'Android'
                    elif self.app_type.lower() == 'ios':
                        default_json['_os'] = 'iOS'

                    transfer_json_array.append(default_json)

                if is_i18n:
                    self.i18n_property_map[key] = transfer_json_array
                if is_image:
                    self.image_property_map[key] = transfer_json_array

            except KeyError:
                if is_i18n:
                    self.i18n_property_map[key] = '1'
                if is_image:
                    self.image_property_map[key] = '1'

    def make_h5_widget_property_map(self, defines_json):
        """
        解析defines_json内容，将widgets节点取出i18n属性集合
        其中key值为 namespace.biz_name.widgets_name  ，value值为 属性.属性 ，通过split('.')过滤出具体参数层次
        :param defines_json:
        :return:
        """
        logger.debug("从应用组件定义中获取h5颗粒的定义")
        for biz_comp_key in defines_json:
            biz_comp_json = defines_json[biz_comp_key]
            namespace = biz_comp_json['namespace']
            biz_name = biz_comp_json['biz_name']

            if 'widgets' in biz_comp_json.keys():
                widgets_json = biz_comp_json['widgets']
                for widgets_key in widgets_json:
                    widget_json = widgets_json[widgets_key]
                    if 'properties' in widget_json.keys():
                        widget_properties_json = widget_json['properties']
                        self.make_h5_widget_composited_property_map(namespace, biz_name, widgets_key, 'properties',
                                                                    widget_properties_json, '')


    def make_h5_widget_composited_property_map(self, namespace, biz_name, widgets_name, element_type, element,
                                               pre_property):
        """
        以起点和最终节点的连接串为key，值为1（多分辨率除外）
        :param namespace:
        :param biz_name:
        :param element_type:
        :param element:
        :param pre_property:
        :return:
        """
        _element_type = ''
        try:
            _element_type = element['_elementType'].lower()
        except KeyError:
            pass

        if _element_type == 'page':
            prefix = '%s%s' % (element['_name'], '.')

            for page_element_key in element:
                if page_element_key.lower() == 'properties':
                    properties_json = element[page_element_key]
                    self.make_h5_widget_composited_property_map(namespace, biz_name, widgets_name, 'properties', properties_json, prefix)

        elif element_type.lower() == 'properties':
            prefix = '%s%s' % (pre_property, 'properties')

            for propertie_key in element:
                if propertie_key.lower() == 'page_display':
                    continue

                propertie_json = element[propertie_key]
                if isinstance(propertie_json, dict):
                    if propertie_json['_elementType'].lower() == 'group':
                        self.make_h5_widget_composited_property_map(namespace, biz_name, widgets_name, 'group', propertie_json, prefix)
                    elif propertie_json['_elementType'].lower() == 'property':
                        self.make_h5_widget_composited_property_map(namespace, biz_name, widgets_name, 'property', propertie_json, prefix)

        elif _element_type == 'group':
            group_name = element['_name']
            prefix = '%s%s%s' % (pre_property, '.', group_name)

            for propertie_element_key in element:
                propertie_element_json = element[propertie_element_key]
                if isinstance(propertie_element_json, dict):
                    try:
                        if propertie_element_json['_elementType'].lower() == 'property':
                            self.make_h5_widget_composited_property_map(namespace, biz_name, widgets_name, 'property', propertie_element_json,
                                                              prefix)
                    except KeyError:
                        pass
        # 前面循环
        elif _element_type == 'property':
            try:
                i18n_element = element['_i18n']
                if i18n_element.lower() == 'true':
                        name_element = element['_name']
                        key = '%s%s%s%s%s' % (namespace, '.', biz_name, '.', widgets_name)
                        value = '%s%s%s' % (pre_property, '.', name_element)
                        self.h5_widget_i18n_property_map[key] = value
            except KeyError:
                pass




from apf_ci.util.file_utils import *

if __name__ == '__main__':
    defines_path = os.path.join('e:\\', 'target', 'defines.json')
    defines_data = read_file_content(defines_path)
    defines_json = json.loads(defines_data)

    app_type = 'Android'
    biz_comp_transform = BizCompJsonTransform(app_type)
    biz_comp_transform.make_property_map(defines_json)

    logger.debug('【xmlI18nPropertyMap】=%s' % biz_comp_transform.i18n_property_map)
    logger.debug('【xmlImagePropertyMap】=%s' % biz_comp_transform.image_property_map)