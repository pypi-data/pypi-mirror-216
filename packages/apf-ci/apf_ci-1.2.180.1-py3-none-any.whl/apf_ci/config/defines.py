#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
defines.json文件内容处理业务
"""

__author__ = 'LianGuoQing'

from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.md5_utils import *


class Defines:
    existIos = True

    def __init__(self, target_path):
        self.target_path = target_path

    def download_define_tag(self, variable_dict, storage_host, factory_id, insert_tag):
        """
        调用存储服务API，将获取到的数据保存到本地defines.json文件中
        :param storage_host:
        :param factory_id:
        :return:
        """
        define_url = "%s/v0.8/define/%s" % (storage_host, factory_id)
        define_json = get_data(define_url)['data']

        define_path = os.path.join(self.target_path, 'defines.json')
        if insert_tag:
            define_json = self.insert_tag_name(variable_dict, define_json)
        write_content_to_file(define_path, json.dumps(define_json))
        logger.info(" download define.json to %s" % define_path)

    def download_define(self, variable_dict, storage_host, factory_id):
        self.download_define_tag(variable_dict, storage_host, factory_id, True)

    def insert_tag_name(self, variable_dict, defines_json):
        """
        读取/target/defines.json文件内容,获取组件名称，然后获取对应xml md5值,并往defines.json回写
        """

        #defines_path = os.path.join(self.target_path, 'defines.json')
        logger.debug(" append tag_version to defines.json start")
        #defines_data = read_file_content(defines_path)
        #defines_json = json.loads(defines_data)
        version_map = {}
        # 由于都是查询release版本的tag，所以这里匹配时候，不带版本号存在component_map
        for component_name in defines_json.keys():
            #components = components + component_name + ','
            component_name_split = component_name.split(':')
            if len(component_name_split) == 3:
                component_version = component_name_split[2]
                if component_version not in version_map.keys():
                    version_map[component_version] = {'components': '', 'component_map': {}}
                version_map[component_version]['components'] = version_map[component_version][
                                                                   'components'] + component_name + ','
                component_map_key = component_name_split[0] + ':' + component_name_split[1]
                version_map[component_version]['component_map'][component_map_key] = component_name

        get_tag_name_body = {}
        biz_component_mng = variable_dict['biz_component_mng']
        get_tag_name_url = biz_component_mng + '/v1.0/bizs/batch/latestTag?bizVersion='
        for component_version in version_map.keys():
            component_temp = version_map[component_version]
            get_tag_name_body['comps'] = component_temp['components']
            component_map = component_temp['component_map']
            response = post_for_array(get_tag_name_url + component_version, get_tag_name_body, True)
            if response and len(response) > 0:
                for item in response:
                    item_name = item['namespace'] + ':' + item['biz_name']
                    #item_name = item['namespace'] + ':' + item['biz_name'] + ':' + item['biz_version']123
                    if item_name in component_map.keys():
                        defines_key = component_map[item_name]
                        #defines_json[defines_key]['tag_version'] = item['tag_name']
                        # 注意，这里的的版本修改了，biz-comp-mng服务的insertJobAndRun接口收集版本也得修改
                        defines_json[defines_key]['tag_version'] = self.get_xml_data(item['xml'])
                    else:
                        logger.warning(" %s 不在 defines.json 中" % item_name)
                        #write_content_to_file(defines_path, json.dumps(defines_json))

        logger.debug(" append tag_version to defines.json end")
        return defines_json

    def get_xml_data(self, xml_str):
        xml_split = xml_str.split("/")
        xml_date = xml_split[len(xml_split) - 2]
        return xml_date


    def defines_json(self):
        """
        读取/target/defines.json文件内容
        :return: 文件内容（dict格式）
        """
        defines_path = os.path.join(self.target_path, 'defines.json')
        defines_data = read_file_content(defines_path)
        return json.loads(defines_data)

    def get_local_h5_config(self):
        """
        读取/target/app_factory/app/local_h5_config.json文件内容
        :return: 文件内容（dict格式）
        """
        local_h5_config_path = os.path.join(self.target_path, 'app_factory/app/local_h5_config.json')
        if is_file_invalid(local_h5_config_path):
           return {}
        else:
            local_h5_config_data = read_file_content(local_h5_config_path)
            return json.loads(local_h5_config_data)

    def parse(self, lite_app_map, app_factory_path, app_type, update_time):
        """
        解析defines.json文件内容，按相应规则将数据分别保存到announce.json和components.json文件中
        :param lite_app_map:
        :param app_factory_path:
        :param app_type:
        :param update_time:
        :return:
        """
        self.app_type = app_type
        self.update_time = update_time

        native_list = []
        local_h5_list = []
        online_h5_list = []
        components_array = []
        # 安卓插件
        android_json = {}
        local_h5_config_data = self.get_local_h5_config()
        defines_json = self.defines_json()
        for define_key, define_json in defines_json.items():
            namespace = define_json['namespace']
            name = define_json['biz_name']

            # 判断产品启用了插件化
            if (name == "plugin-setting"):
                android_json["plugin-setting"] = True;

            component_attribute = {}
            component_attribute['namespace'] = namespace
            component_attribute['name'] = name

            announce_component_json = {}
            announce_component_json['component'] = component_attribute

            component_json = {}
            component_json['component'] = component_attribute

            extend_json = {}

            type_list = []

            if 'types' in define_json.keys():
                types_json = define_json['types']

                self.do_native_android(types_json, component_json, type_list, announce_component_json, extend_json)
                self.existIos = True
                self.do_native_ios(types_json, component_json, type_list, announce_component_json)

                # if 'library' in types_json.keys():
                #     type_list.append('library')
                #     announce_component_json['type'] = 'library'
                if 'ios' == self.app_type.lower():
                    if 'library' in types_json.keys():
                        announce_component_json['type'] = 'library'
                        if (self.existIos):
                            type_list.append('library')
                        else:
                            type_list = []
                            logger.debug("[debug]type_list已经置空")
                else:
                    if 'library' in types_json.keys():
                        type_list.append('library')
                        announce_component_json['type'] = 'library'

                announce_flag = False
                if 'android' in announce_component_json.keys() and announce_component_json['android']:
                    announce_flag = True

                if 'ios' in announce_component_json.keys() and announce_component_json['ios']:
                    announce_flag = True

                if announce_flag:
                    native_list.append(announce_component_json)

                self.do_react_widget(types_json, component_json, type_list)
                self.do_react_android(types_json, component_json, type_list)
                self.do_react_ios(types_json, component_json, type_list)

                self.do_h5_widget(types_json, component_json, type_list, local_h5_list, lite_app_map)

                self.do_local_h5(types_json, component_json, type_list, local_h5_list, lite_app_map, define_key,
                                 local_h5_config_data)
                self.do_online_h5(types_json, component_json, type_list, online_h5_list)
                self.do_template_h5(types_json, component_json, type_list, lite_app_map)
                self.do_flutter(types_json, component_json, type_list)

            # type_list去重
            component_json['type'] = list(set(type_list))

            components_array.append(component_json)

            # 收集安卓插件
            if self.app_type.lower() == 'android':
                if "plugin" in extend_json:
                    if extend_json["plugin"] == "true":
                        plugin_name = str('%s_%s' % (namespace, name))
                        logger.debug("[plugin_name = %s" % plugin_name)
                        android_json[plugin_name] = "true"

        announce_json = {}

        if native_list.__len__() > 0:
            announce_json['native'] = native_list

        if local_h5_list.__len__() > 0:
            announce_json['local-h5'] = local_h5_list

        if online_h5_list.__len__() > 0:
            announce_json['online-h5'] = online_h5_list

        app_announce_path = os.path.join(app_factory_path, 'app', 'announce.json')
        write_content_to_file(app_announce_path, json.dumps(announce_json))

        app_components_path = os.path.join(app_factory_path, 'app', 'components.json')
        write_content_to_file(app_components_path, json.dumps(components_array))

        android_plugin_path = os.path.join(self.target_path, 'android_plugin.json')
        write_content_to_file(android_plugin_path, json.dumps(android_json))

    def do_native_android(self, types_json, component_json, type_list, announce_component_json, extend_json):
        """
        封装android类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param announce_component_json:
        :return:
        """
        if 'native-android' in types_json.keys():
            type_json = types_json['native-android']

            class_value = ''
            if 'class' in type_json.keys():
                class_value = type_json['class']

            if 'extend' in type_json.keys():
                extend = type_json['extend']
                if "plugin" in extend:

                    if extend['plugin'] == "true":
                        extend_json['plugin'] = 'true'

            native_android_json = {}
            native_android_json['class'] = class_value
            component_json['native-android'] = native_android_json

            type_list.append('native-android')
            announce_component_json['android'] = class_value


            # if 'library' in types_json.keys():
            #     type_list.append('library')
            #     announce_component_json['type'] = 'library'


    def do_native_ios(self, types_json, component_json, type_list, announce_component_json):
        """
        封装iOS类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param announce_component_json:
        :return:
        """
        if 'native-iOS' in types_json.keys():
            type_json = types_json['native-iOS']

            class_value = ''
            dependency_value = ''
            if 'class' in type_json.keys():
                class_value = type_json['class']
            if 'dependency' in type_json.keys():
                dependency_value = type_json['dependency']

            if ('' != class_value and '' != dependency_value):
                native_ios_json = {}
                native_ios_json['class'] = class_value
                component_json['native-ios'] = native_ios_json

                type_list.append('native-ios')
                announce_component_json['ios'] = class_value
            elif ('' == dependency_value):
                self.existIos = False
                announce_component_json['ios'] = ''
            else:
                announce_component_json['ios'] = ''
        else:
            self.existIos = False


    def do_react_widget(self, types_json, component_json, type_list):
        """
        封装react-widget类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :return:
        """
        react_widget_npm = ''
        component_type = ''
        if self.app_type.lower() == 'android':
            if 'react-widget-android' in types_json.keys():
                type_json = types_json['react-widget-android']
                if 'npm' in type_json.keys():
                    react_widget_npm = type_json['npm'].strip()

                component_type = 'react-widget'
        elif self.app_type.lower() == 'ios':
            if 'react-widget-ios' in types_json.keys():
                type_json = types_json['react-widget-ios']
                if 'npm' in type_json.keys():
                    react_widget_npm = type_json['npm'].strip()

                component_type = 'react-widget'

        if component_type:
            react_widget_json = {}
            react_widget_json['npm'] = react_widget_npm
            react_widget_json['build_time'] = self.update_time

            type_list.append('react-widget')
            component_json['react-widget'] = react_widget_json

    def do_react_android(self, types_json, component_json, type_list):
        """
        封装react-android类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :return:
        """
        if 'react-android' in types_json.keys():
            type_json = types_json['react-android']
            npm_value = ''
            if 'npm' in type_json.keys():
                npm_value = type_json['npm'].strip()

            react_android_json = {}
            react_android_json['npm'] = npm_value
            react_android_json['build_time'] = self.update_time

            type_list.append('react-android')
            component_json['react-android'] = react_android_json

    def do_react_ios(self, types_json, component_json, type_list):
        """
        封装react-ios类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :return:
        """
        if 'react-ios' in types_json.keys():
            type_json = types_json['react-ios']
            npm_value = ''
            if 'npm' in type_json.keys():
                npm_value = type_json['npm'].strip()

            react_ios_json = {}
            react_ios_json['npm'] = npm_value
            react_ios_json['build_time'] = self.update_time

            type_list.append('react-ios')
            component_json['react-ios'] = react_ios_json

    def append_local_h5_list(self, types_json, component_json, version, local_h5_list, lite_app_map):
        """
        封装announce.json文件中local-h5节点数据
        :param types_json:
        :param component_json:
        :param version:
        :param local_h5_list:
        :param lite_app_map:
        :return:
        """
        component = component_json['component']

        host = ''
        key = '%s_%s' % (component['namespace'], component['name'])
        if key in lite_app_map.keys():
            host = lite_app_map[key]

        local_h5_json = {}
        if 'library' in types_json.keys():
            local_h5_json['type'] = 'library'

        local_h5_json['host'] = host
        local_h5_json['version'] = version
        local_h5_json['component'] = component
        local_h5_list.append(local_h5_json)

        return host

    def do_h5_widget(self, types_json, component_json, type_list, local_h5_list, lite_app_map):
        """
        封装widget类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param local_h5_list:
        :param lite_app_map:
        :return:
        """
        if 'widget' in types_json.keys():
            type_json = types_json['widget']
            version = type_json['version']
            self.append_local_h5_list(types_json, component_json, version, local_h5_list, lite_app_map)

            type_list.append('widget')

            h5_widget_json = {}
            h5_widget_json['build_time'] = self.update_time
            component_json['widget'] = h5_widget_json

    def do_local_h5(self, types_json, component_json, type_list, local_h5_list, lite_app_map, define_key,
                    local_h5_config_data):
        """
        封装local-h5类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param local_h5_list:
        :param lite_app_map:
        :return:
        """
        if 'local-h5' in types_json.keys():
            type_json = types_json['local-h5']
            version = type_json['version']
            host = self.append_local_h5_list(types_json, component_json, version, local_h5_list, lite_app_map)

            type_list.append('local-h5')

            local_h5_json = {}
            local_h5_json['host'] = host
            local_h5_json['npm'] = type_json['npm'].strip()
            local_h5_json['build_time'] = self.update_time
            local_h5_json['version'] = version
            # 默认是不预置到应用里
            local_h5_json['preassign'] = 'false'
            if define_key in local_h5_config_data:
                local_h5_config = local_h5_config_data[define_key]
                if 'preassign' in local_h5_config:
                    local_h5_json['preassign'] = local_h5_config['preassign'].strip()
            component_json['local-h5'] = local_h5_json

    def do_online_h5(self, types_json, component_json, type_list, online_h5_list):
        """
        封装online-h5类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param online_h5_list:
        :return:
        """
        if 'online-h5' in types_json.keys():
            type_json = types_json['online-h5']
            host = type_json['host']

            online_h5_json = {}
            if 'library' in types_json.keys():
                online_h5_json['type'] = 'library'
            online_h5_json['host'] = host
            online_h5_json['component'] = component_json['component']
            online_h5_list.append(online_h5_json)

            type_list.append('online-h5')

            online_h5 = {}
            online_h5['host'] = host
            component_json['online-h5'] = online_h5

    def do_template_h5(self, types_json, component_json, type_list, lite_app_map):
        """
        封装template-h5类型数据
        :param types_json:
        :param component_json:
        :param type_list:
        :param lite_app_map:
        :return:
        """
        if 'template-h5' in types_json.keys():
            type_json = types_json['template-h5']
            component = component_json['component']

            host = ''
            key = '%s_%s' % (component['namespace'], component['name'])
            if key in lite_app_map.keys():
                host = lite_app_map[key]

            type_list.append('template-h5')

            template_h5_json = {}
            template_h5_json['host'] = host
            template_h5_json['npm'] = type_json['npm'].strip()
            template_h5_json['version'] = type_json['version']
            component_json['template-h5'] = template_h5_json

    def do_flutter(self, types_json, component_json, type_list):
        """
        封装flutter类型数据
        :param type_json:
        :param component_json:
        :param type_list:
        :return:
        """
        if 'flutter' in types_json.keys():
            type_json = types_json['flutter']

            type_list.append('flutter')
            component_json['flutter'] = type_json
