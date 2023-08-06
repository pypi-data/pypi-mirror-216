#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import json

from apf_ci.config.defines import Defines
from apf_ci.util.file_utils import *

class Runtime(Defines):
    def __get_attributes_array(self, runtime_json, runtime_key, element_type):
        """
        runtime节点下有properties、providers、handlers三种属性（runtime_json），
        通过属性值获取相应的attributes_json，如果其下属性满足provider、handler，
        则将attributes_json统一加入到数组中
        :param runtime_json: runtime节点内容
        :param runtime_key: properties、providers、handlers
        :param element_type: provider、handler
        :return: 返回包含attributes_json的数组
        """
        attributes_array = []
        attributes_json = runtime_json[runtime_key]
        for attributes_key in attributes_json:
            attribute_json = attributes_json[attributes_key]
            if attribute_json['_elementType'] == element_type:
                attributes_array.append(attribute_json)

        return attributes_array

    def __get_providers_handlers_map(self):
        """
        将defines.json文件中含有runtime节点的providers、handlers属性解析出来
        :return: 分别输出含provider和handler属性的键值对dict格式
        """
        runtime_providers_map = {}
        runtime_handlers_map = {}

        defines_json = super().defines_json()
        for defines_key in defines_json:
            define_json = defines_json[defines_key]

            if 'extensions' not in define_json.keys():
                continue

            extensions_json = define_json['extensions']
            if 'runtime' not in extensions_json.keys():
                continue

            namespace = define_json['namespace']
            biz_name = define_json['biz_name']
            runtime_attributes_key = '%s_%s' % (namespace, biz_name)

            runtime_json = extensions_json['runtime']
            for runtime_key in runtime_json:
                if runtime_key == 'providers':
                    providers_array = self.__get_attributes_array(runtime_json, runtime_key, 'provider')
                    runtime_providers_map[runtime_attributes_key] = providers_array
                elif runtime_key == 'handlers':
                    handlers_array = self.__get_attributes_array(runtime_json, runtime_key, 'handler')
                    runtime_handlers_map[runtime_attributes_key] = handlers_array

        return runtime_providers_map, runtime_handlers_map

    def __handle_runtime_providers(self, runtime_providers_map, runtime_providers_key, build_json):
        """
        向build.json文件中添加providers节点（JSONArray格式），其内容provider_json包含name、filter、anClass、iosClass属性
        :param runtime_providers_map:
        :param runtime_providers_key:
        :param build_json:
        :return:
        """
        if runtime_providers_key in runtime_providers_map.keys():
            providers_array = []
            runtime_providers_array = runtime_providers_map[runtime_providers_key]
            for runtime_provider_json in runtime_providers_array:
                filter_array = []
                if '_filter' in runtime_provider_json.keys():
                    filter = runtime_provider_json['_filter']
                    if filter:
                        filter_array = [item for item in filter.split(',')]

                an_class = ''
                if '_anClass' in runtime_provider_json.keys():
                    an_class = runtime_provider_json['_anClass']

                ios_class = ''
                if '_iosClass' in runtime_provider_json.keys():
                    ios_class = runtime_provider_json['_iosClass']

                provider_json = {}
                provider_json['name'] = runtime_provider_json['_name']
                provider_json['filter'] = filter_array

                if an_class:
                    provider_json['anClass'] = an_class

                if ios_class:
                    provider_json['iosClass'] = ios_class

                providers_array.append(provider_json)

            if providers_array.__len__() > 0:
                build_json['providers'] = providers_array

    def __handle_runtime_handlers(self, runtime_handlers_map, runtime_handlers_key, build_json):
        """
        向build.json文件中添加或修改event节点（JSONObject格式）：以键为receive_event_item，
        值为数组且其内容event_handle_json包含component、handler、sync、anClass、iosClass属性
        :param runtime_handlers_map:
        :param runtime_handlers_key:
        :param build_json:
        :return:
        """
        if runtime_handlers_key in runtime_handlers_map.keys():
            if 'event' not in build_json.keys():
                build_json['event'] = {}
            event_json = build_json['event']
            component_json = build_json['component']

            runtime_handlers_array = runtime_handlers_map[runtime_handlers_key]
            for runtime_handler_json in runtime_handlers_array:
                name = runtime_handler_json['_name']

                an_class = ''
                if '_anClass' in runtime_handler_json.keys():
                    an_class = runtime_handler_json['_anClass']

                ios_class = ''
                if '_iosClass' in runtime_handler_json.keys():
                    ios_class = runtime_handler_json['_iosClass']

                if '_receive_event' in runtime_handler_json.keys():
                    receive_event = runtime_handler_json['_receive_event']
                    if receive_event:
                        receive_event_array = [item.strip() for item in receive_event.split(',')]
                        for receive_event_item in receive_event_array:
                            event_handle_array = []
                            if receive_event_item in event_json.keys():
                                event_handle_array = event_json[receive_event_item]

                            event_handle_json = {}
                            event_handle_json['component'] = component_json
                            event_handle_json['handler'] = name
                            event_handle_json['sync'] = '1'

                            if an_class:
                                event_handle_json['anClass'] = an_class

                            if ios_class:
                                event_handle_json['iosClass'] = ios_class

                            event_handle_array.append(event_handle_json)

                            event_json[receive_event_item] = event_handle_array

    def handle_build_json_file(self, languages_array, app_factory_path):
        """
        向多语言路径下的build.json内容添加providers属性，该属性值为defines.json文件中含有runtime节点的providers属性值
        :param languages_array: 语言数组
        :param app_factory_path: 存放路径
        :return: 无
        """
        runtime_providers_map, runtime_handlers_map = self.__get_providers_handlers_map()

        is_handle_runtime_providers = False
        if runtime_providers_map.__len__() > 0:
            is_handle_runtime_providers = True

        is_handle_runtime_handlers = False
        if runtime_handlers_map.__len__() > 0:
            is_handle_runtime_handlers = True

        for language_name in languages_array:
            build_path = os.path.join(app_factory_path, language_name, 'components', 'build.json')
            build_data = read_file_content(build_path)
            build_array = json.loads(build_data)

            for build_json in build_array:
                component_json = build_json['component']
                namespace = component_json['namespace']
                name = component_json['name']
                runtime_attributes_key = '%s_%s' % (namespace, name)

                if is_handle_runtime_providers:
                    self.__handle_runtime_providers(runtime_providers_map, runtime_attributes_key, build_json)

                if is_handle_runtime_handlers:
                    self.__handle_runtime_handlers(runtime_handlers_map, runtime_attributes_key, build_json)

            write_content_to_file(build_path, json.dumps(build_array))

    def __get_runtime_properties_map(self, app_type):
        """
        将defines.json文件中含有runtime节点的properties属性解析出来
        :return:键值对dict格式输出
        """
        runtime_properties_map = {}

        defines_json = super().defines_json()
        for defines_key in defines_json:
            define_json = defines_json[defines_key]
            if 'extensions' not in define_json.keys():
                continue

            extensions_json = define_json['extensions']
            if 'runtime' not in extensions_json.keys():
                continue

            runtime_json = extensions_json['runtime']
            if 'properties' not in runtime_json.keys():
                continue

            property_array = []
            properties_json = runtime_json['properties']
            for properties_key in properties_json:
                property_json = properties_json[properties_key]

                if property_json['_elementType'] == 'property':
                    property_array.append(property_json)
                elif property_json['_elementType'] == 'group':
                    property_json_temp = properties_json[properties_key]
                    for property_key in list(property_json.keys()):
                        if property_key.startswith('_'):
                            if property_key != '_elementType' and property_key != '_name':
                                property_json_temp.pop(property_key)
                        else:
                            property_value_temp = property_json_temp[property_key]
                            # 如果group下的子节点_elementType属性不是property，则不记录build.json
                            # 如果os平台和构建类型不符，则不记录build.json
                            if "_elementType" in property_value_temp.keys() and property_value_temp["_elementType"] == "property":
                                if "_os" in property_value_temp.keys() and property_value_temp["_os"].lower() != app_type.lower():
                                    property_json_temp.pop(property_key)
                                else:
                                    property_json_temp[property_key] = property_value_temp['_value']
                            else:
                                property_json_temp.pop(property_key)

                    property_array.append(property_json_temp)

            runtime_properties_key = '%s_%s' % (define_json['namespace'], define_json['biz_name'])
            runtime_properties_map[runtime_properties_key] = property_array

        return runtime_properties_map

    def handle_runtime_properties(self, content, app_type):
        """
        defines.json文件中解析到的runtime节点properties属性集合，通过key值比对build.json内容中的properties属性，
        将集合中的_name值以key形式、_value值以value形式追加到properties属性中
        :param content: build.json文件内容
        :return: 返回追加runtime节点properties属性到properties属性中的内容
        """
        runtime_properties_map = self.__get_runtime_properties_map(app_type)

        if runtime_properties_map.__len__() == 0:
            return content

        content_array = json.loads(content)
        for build_json in content_array:
            component_json = build_json['component']
            biz_key = '%s_%s' % (component_json['namespace'], component_json['name'])

            if biz_key in runtime_properties_map.keys():
                properties_json = build_json['properties']

                runtime_properties_array = runtime_properties_map[biz_key]
                for runtime_properties_json in runtime_properties_array:
                    name = runtime_properties_json['_name']

                    if runtime_properties_json['_elementType'] == 'group':
                        runtime_properties_json.pop('_name')
                        runtime_properties_json.pop('_elementType')

                        group_name_array = []
                        group_name_array.append(runtime_properties_json)
                        properties_json[name] = group_name_array
                    else:
                        # 判断构建的平台类型是否和定义的_os符合，没定义默认输出。
                        if "_os" in runtime_properties_json.keys():
                            if runtime_properties_json["_os"].lower() == app_type.lower():
                                properties_json[name] = runtime_properties_json['_value']
                        else:
                            properties_json[name] = runtime_properties_json['_value']

        return json.dumps(content_array)