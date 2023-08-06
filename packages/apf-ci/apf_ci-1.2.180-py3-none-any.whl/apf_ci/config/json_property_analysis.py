#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import json

class JsonPropertyAnalysis:
    def __init__(self, biz_comp_transform):
        self.biz_comp_transform = biz_comp_transform

    def make_widget_uuid_map(self, content, i18n_property_map, image_property_map):
        """
        生成颗粒uuid集合
        :param content:
        :param i18n_property_map:
        :param image_property_map:
        :return:
        """
        template_dict = {}

        content_array = json.loads(content)
        for page_id in content_array:
            page_data = content_array[page_id]
            if isinstance(page_data, dict):
                component_json = page_data['component']
                namespace = component_json['namespace']
                biz_name = component_json['name']

                template = page_data['template']
                template_id = template[template.index('?id=')+4:]

                try:
                    parent = page_data['__parent']
                    if parent:
                        index = parent.index('?id=')
                        parent_id = parent[index+4:]
                        page_data['__parent'] = parent_id
                except KeyError:
                    pass
                except ValueError:
                    pass

                try:
                    top = page_data['__top']
                    if top:
                        top_index = top.index('?id=')
                        top_id = top[top_index+4:]
                        page_data['__top'] = top_id
                except KeyError:
                    pass
                except ValueError:
                    pass

                pre_str = '%s%s%s%s' % (namespace, '.', biz_name, '.properties')
                properties_json = page_data['properties']
                self.parse_properties(properties_json, pre_str, i18n_property_map, image_property_map)

                page_data['template'] = template_id
                template_dict[template_id] = page_data

        return template_dict

    def make_uuid_map(self, content, key, i18n_property_map, image_property_map):
        """
        生成uuid集合
        :param content:
        :param key:
        :param i18n_property_map:
        :param image_property_map:
        :return:
        """
        content_array = json.loads(content)
        for content_json in content_array:
            component_json = content_json['component']
            if key == 'component_pages' or key == 'app_pages':
                if '_component' in content_json.keys():
                    component_json = content_json['_component']

            if not  'namespace' in component_json:
                print('不存在namespace2：'+str(content))
            namespace = component_json['namespace']
            biz_name = component_json['name']

            pre_str = '%s%s%s' % (namespace, '.', biz_name)
            if key != 'build':
                page_name = content_json['page_name']
                pre_str = '%s%s%s' % (pre_str, '.', page_name)

            pre_str = '%s%s' % (pre_str, '.properties')
            properties_json = content_json['properties']
            self.parse_properties(properties_json, pre_str, i18n_property_map, image_property_map)

    def parse_properties(self, properties_json, pre_str, i18n_property_map, image_property_map):
        for propertie_key in properties_json:
            propertie_value = properties_json[propertie_key]
            new_key = '%s%s%s' % (pre_str, '.', propertie_key)

            if isinstance(propertie_value, dict) or isinstance(propertie_value, list):
                self.record_uuid(propertie_value, new_key, i18n_property_map, image_property_map)
            else:
                self.set_property_map(new_key, propertie_value, i18n_property_map, image_property_map)

    def record_uuid(self, object, pre_str, i18n_property_map, image_property_map):
        if isinstance(object, dict):
            for key in object:
                new_pre_str = '%s%s%s' % (pre_str, '.', key)
                value = object[key]
                self.record_uuid(value, new_pre_str, i18n_property_map, image_property_map)
        elif isinstance(object, list):
            for object_json in object:
                self.record_uuid(object_json, pre_str, i18n_property_map, image_property_map)
        else:
            self.set_property_map(pre_str, object, i18n_property_map, image_property_map)

    def set_property_map(self, key, value, i18n_property_map, image_property_map):
        xml_i18n_property_map = self.biz_comp_transform.i18n_property_map
        xml_image_property_map = self.biz_comp_transform.image_property_map

        if key in xml_i18n_property_map.keys():
            i18n_property_map[value] = ''

        if key in xml_image_property_map.keys():
            image_property = xml_image_property_map[key]

            image_property_value = ''
            try:
                image_property_value = image_property_map[value]
            except KeyError:
                pass

            if image_property_value == '':
                if isinstance(image_property, list):
                    image_property_value = image_property
                else:
                    image_property_value = value

                image_property_map[value] = image_property_value




