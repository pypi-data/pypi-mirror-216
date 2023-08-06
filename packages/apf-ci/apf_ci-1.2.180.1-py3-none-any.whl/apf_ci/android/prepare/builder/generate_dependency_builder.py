#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import re
import traceback
from apf_ci.util.file_utils import *
from apf_ci.android.prepare.model.meta_data_note import MetaDataNote
from apf_ci.util.http_utils import *
from lxml.etree import *


class GenerateDependencyBuilder:
    def __init__(self, app_id, variables_dict):
        self.app_id = app_id
        self.variables_dict = variables_dict

    def perform(self):
        logger.info(" 开始do generate dependency")
        variables_dict = self.variables_dict
        native_storage_host = variables_dict["app_native_storage"]
        # 获取defines.json文件内容
        defines_path = os.path.join(os.getcwd(), "target/defines.json")
        defines_content_str = read_file_content(defines_path)
        defines_json_dict = json.loads(defines_content_str)
        # 获取dependencyFinal.txt文件内容
        dependency_final_path = os.path.join(os.getcwd(), "target/dependencyFinal.txt")
        dependency_final_content_str = read_file_content(dependency_final_path)
        dependency_json_list = json.loads(dependency_final_content_str)

        self.do_generate_dependency(dependency_json_list, defines_json_dict, native_storage_host)
        logger.info(" do generate dependency完毕")
        return True

    def do_generate_dependency(self, dependency_json_list, defines_json_dict, native_storage_host):
        """
        处理组件定义的denpendency，生成.gradle 和 manifest XML文件
        :param dependency_json_list:
        :param defines_json_dict:
        :param native_storage_host:
        :return:
        """
        groovy_strbuffer = ""
        dependency_strbuffer = "dependencies{\nrepositories { flatDir { dirs './aars' } }\n"

        # 搜集name -value 值对
        properties_map = {}
        try:
            self._init_properties_map(dependency_json_list, properties_map)
        except Exception as e:
            logger.debug("初始化properties 键值对失败 %s" % e)
            traceback.print_exc()

        meta_map = {}
        res_map = {}
        meta_data_notes_list = []
        meta_data_key_map = {}

        biz_comp_xml_map = {}
        try:
            self._init_biz_comp_xml_map(defines_json_dict, biz_comp_xml_map)
        except Exception as e:
            logger.warning("解析各组件xml失败 %s" % e)
            traceback.print_exc()

        # 解析相关的main
        for dependency_element in dependency_json_list:
            if isinstance(dependency_element, dict):
                component = dependency_element.get("component", {})
                namespace = component.get("namespace", "")
                name = component.get("name", "")

                define_str = biz_comp_xml_map.get(namespace + ":" + name)
                if not isinstance(define_str, str):
                    logger.warning("查找不到对应的组件定义：" + namespace + ":" + name)
                define_dict = json.loads(define_str)
                types = define_dict.get("types", "")
                if types:
                    native_android = types.get("native-android", {})
                    if native_android:
                        dependency_strbuffer += native_android.get("dependency", "")
                        dependency_strbuffer += "\n"

                        groovy_strbuffer += native_android.get("groovy", "")
                        groovy_strbuffer += "\n"

                # page - class  这段的作用是啥。
                pages = define_dict.get("pages", {})
                if pages:
                    for page_key in pages:
                        page_dict = pages[page_key]
                        if page_dict.get("_android_class") is None or page_dict.get("_name") is None or page_dict.get(
                                "_type") is None:
                            continue

                # properties>>property, + property - android_meta, + property - android_res
                properties_property_map = {}
                properties_dict = define_dict.get("properties", {})
                if properties_dict:
                    for key in properties_dict:
                        properties_value = properties_dict[key]
                        if "_name" in properties_value:
                            name_str = properties_value.get("_name", "")
                            if properties_value.get("_elementType", "").lower() == "property":
                                if properties_value.get("_android_meta", "").lower() == "1":
                                    meta_map[name_str] = properties_map.get(name_str, "")
                                elif properties_value.get("_android_res", "").lower() == "1":
                                    res_map[name_str] = properties_map.get(name_str, "")
                                properties_property_map[name_str] = name_str
                        else:
                            logger.warning("%s 中 _name 不存在" % json.dumps(properties_value))

                # component - android - meta-datas 解析meta-datas并且置换特定字符值
                self._parse_meta_data_and_set_value(properties_map, define_dict, meta_data_notes_list,
                                                    properties_property_map, meta_data_key_map)

        # add subapp dependencies
        subapp_dependency_json = self._get_subapp_dependencies(native_storage_host)
        dependency_strbuffer += subapp_dependency_json["dependency"]
        dependency_strbuffer += "}"

        groovy_strbuffer += subapp_dependency_json["groovy"]
        dependency_strbuffer += groovy_strbuffer

        # dependency内容写入 app-factory-component.gradle
        gradle_path = os.path.join(os.getcwd(), "app/app-factory-component.gradle")
        write_content_to_file(gradle_path, dependency_strbuffer)

        # 生成app/assets/ci/dependency.txt 2020.06.04 屏蔽
        #self._write_assets_ci_dependency_file(dependency_strbuffer)

        # 写mainfest
        self._write_android_manifest_xml(meta_data_notes_list)

        meta_strbuffer = ""
        for key in meta_map:
            meta_strbuffer += "<meta-data android:name=\""
            meta_strbuffer += key
            meta_strbuffer += "\" android:value=\""
            meta_strbuffer += meta_map[key]
            meta_strbuffer += "\"/>\n"
        meta_strbuffer += "</application>"
        manifest_file_path = os.path.join(os.getcwd(), "app/AndroidManifest.xml")
        manifest_str = read_file_content(manifest_file_path)
        manifest_str = manifest_str.replace("</application>", meta_strbuffer)
        write_content_to_file(manifest_file_path, manifest_str)
        logger.debug(" 传统方式替换后的manifestStr ：%s" % manifest_str)

        # 写string_ci.xml 拼接str
        res_strbuffer = ""
        res_strbuffer += "<resources>\n"
        for key in res_map:
            res_strbuffer += '<string name="%s">%s</string>\n' % (key, res_map[key])
        res_strbuffer += "</resources>"
        res_file_path = os.path.join(os.getcwd(), "app/res/values/strings_ci.xml")
        write_content_to_file(res_file_path, res_strbuffer)

    def _init_properties_map(self, dependency_json_list, properties_map):
        """
        根据dependencyFinal.txt 内容。初始化 properties_map。
        dependencyFinal.txt大致结构 list类型：[ { "component":{xxx}, "properties":{xxx}}, ]
        :param dependency_json_list:
        :param properties_map:
        :return:
        """
        for dependency_element in dependency_json_list:
            if isinstance(dependency_element, dict):
                properties = dependency_element.get("properties", {})
                for properties_key in properties:
                    key = properties_key
                    value = properties[properties_key]
                    if not properties_map.get(key):
                        properties_map[key] = value
                    else:
                        logger.debug("属性：%s 有重复，优先选用不为空的值，值有:%s,%s。" % (key, properties_map[key], value))
                        if value:
                            properties_map[key] = value

    def _init_biz_comp_xml_map(self, defines_json_dict, biz_comp_xml_map):
        """
        根据define.json内容，初始化biz_comp_map
        define.json大概结构 dict类型：{ "包名:组件名:tag_xx" : {"xx":xx,"properties":{xxxx} }, }
        :param defines_json_dict:
        :param biz_comp_xml_map:
        :return:
        """
        for define_key in defines_json_dict:
            element = defines_json_dict[define_key]
            namespace = element.get("namespace", "")
            biz_name = element.get("biz_name", "")

            key = namespace + ":" + biz_name
            biz_comp_xml_map[key] = json.dumps(element)

    def _parse_meta_data_and_set_value(self, properties_map, biz_comp_define_dict, meta_data_notes_list,
                                       properties_property_map, meta_data_key_map):
        """
        获取组件定义的内容biz_comp_define，解析metadata
        :param properties_map:
        :param biz_comp_define_dict:
        :param meta_data_notes_list:
        :param properties_property_map:
        :param meta_data_key_map:
        :return:
        """
        types = biz_comp_define_dict.get("types", {})
        if not types:
            return meta_data_notes_list
        native_android = types.get("native-android", {})
        if not native_android:
            return meta_data_notes_list
        meta_datas = native_android.get("meta-datas", [])
        if not meta_datas:
            return meta_data_notes_list

        logger.debug("meta-data list length: %s" % len(meta_datas))
        xpath = ""
        file = ""
        type = ""
        index_number = 0
        for metadata in meta_datas:
            xpath = metadata.get("xpath", "")
            file = metadata.get("file", "")
            if not xpath or not file:
                continue
            type = metadata.get("type", "")

            meta_data_note = MetaDataNote()
            meta_data_note.xpath = xpath
            meta_data_note.file = file

            cdata = ""
            if type and type == "attribute":
                for key in metadata:
                    if key == "attribute":
                        child_element_dict = metadata[key]
                        # 匹配字符串，返回匹配列表
                        matcher = re.findall("\\$\\{(.*?)\\}", child_element_dict.get("value", ""))
                        if len(matcher) > 0:
                            for matcher_data in matcher:
                                # 这里的matcher matcher : (xxx,xxx)取第一个xxx的值
                                properties_str = properties_property_map.get(matcher_data)
                                if not properties_str:
                                    continue
                                    # 从属性值中取value 替换掉 cdata 中 ${name}
                                value = properties_map.get(matcher_data)

                                if not value:
                                    logger.warning("属性： %s 的值为空，可能导致某个功能不能用" % matcher_data)
                                child_element_dict["value"] = value
                                logger.debug("标签<%s> 添加value值为【%s】" % (key, value))
                        meta_data_note.child_node = child_element_dict
            else:
                cdata = metadata.get("text", "")
            logger.debug("cdata: %s" % cdata)
            duplicate_key_flag = False
            matcher = re.findall("\\$\\{(.*?)\\}", cdata)
            property_str = ""
            if len(matcher) > 0:
                for matcher_data in matcher:
                    logger.debug("属性find:%s" % matcher_data)
                    property_str = properties_property_map.get(matcher_data)
                    logger.debug("属性是否存在：%s" % property_str)
                    if not property_str:
                        continue
                    logger.debug("属性对象的metadata key：%s" % meta_data_key_map.get(property_str))
                    if meta_data_key_map.get(property_str):
                        duplicate_key_flag = True
                        break

                    # 从属性值中取value 替换掉 cdata 中 ${name}
                    v = properties_map.get(matcher_data)
                    if not v:
                        logger.warning("属性：%s的值为空，可能导致某个功能不能用" % matcher_data)
                    v = "" if v is None else v
                    cdata = cdata.replace("${%s}" % matcher_data, v)

            if not duplicate_key_flag:
                meta_data_key_map[property_str] = property_str
            else:
                continue
            meta_data_note.type = type
            meta_data_note.cdata = cdata
            logger.debug("第【%s】 %s" % (index_number, meta_data_note.tostring_format()))
            meta_data_notes_list.append(meta_data_note)
            index_number += 1
        return meta_data_notes_list

    def _get_subapp_dependencies(self, native_storage_host):
        """
        获取子应用的依赖。
        :param native_storage_host:
        :return:
        """
        dependency_strbuffer = ""
        groovy_strbuffer = ""

        url = native_storage_host + "/v0.8/define/" + self.app_id + "/subapps"
        logger.debug("get subapp biz defines: %s" % url)

        subapp_def = get_data(url)
        if subapp_def:
            data = subapp_def.get("data", {})
            for key in data:
                each_def = data[key]
                types = each_def.get("types", {})
                if types:
                    native_android = types.get("native-android", {})
                    if native_android:
                        dependency_strbuffer += native_android.get("dependency", "")
                        dependency_strbuffer += "\n"

                        groovy_strbuffer += native_android.get("groovy", "")
                        groovy_strbuffer += "\n"
        else:
            logger.debug("subapp biz defien: %s" % subapp_def)

        return_json = {
            "dependency": dependency_strbuffer,
            "groovy": groovy_strbuffer
        }
        return return_json

    def _write_android_manifest_xml(self, meta_data_notes_list):
        """
        生成android_manifest.xml文件
        ${workspace}:
            ├── app
            │   ├── AndroidManifest.xml
        :param meta_data_notes_list:
        :return:
        """
        for meta_data_note_object in meta_data_notes_list:
            logger.debug(meta_data_note_object.tostring_format())

            # 替换androidManifest.xml 文件，可能 xpath,跟 file 路径不一样，所以每次都重新获取文件
            manifest_file_path = os.getcwd() + meta_data_note_object.file
            if not os.path.isfile(manifest_file_path) or not os.path.exists(manifest_file_path):
                logger.warning("构建失败，文件查找不到：%s" % manifest_file_path)
            manifest_text = read_file_content(manifest_file_path)

            # etree.fromstring()  etree.tostring()
            manifest_doc = fromstring(manifest_text.encode())
            xpath_node = manifest_doc.xpath(meta_data_note_object.xpath)
            if len(xpath_node) > 0:
                xpath_node = xpath_node[0]
            else:
                xpath_node = None
                logger.debug("构建失败 %s 文件查找不到节点 Xapth : %s" % (meta_data_note_object.file, meta_data_note_object.xpath))
                # 添加属性metaDate 属性
            if meta_data_note_object.type == "attribute":
                attribute_name = meta_data_note_object.child_node.get("name", "")
                attribute_value = meta_data_note_object.child_node.get("value", "")
                logger.debug("要替换 xPath Node 【%s】" % tostring(xpath_node).decode("utf-8"))
                logger.debug("MetaDataNote name【%s】，value 【%s】" % (attribute_name, attribute_value))

                # 判断标签属性是否已存在 xpath_node 的标签字典中
                if attribute_name.find(":") > 0 and attribute_name.split(":")[1] in xpath_node.attrib.keys():
                    logger.warning("%s 标签属性已存在 : %s" % (xpath_node.tag, attribute_name))
                namespace_attribute_name = self._get_xml_attribute_name(attribute_name, xpath_node)
                xpath_node.attrib[namespace_attribute_name] = attribute_value
            else:
                logger.debug("writeAndroidManifestXml cdata : %s" % meta_data_note_object.cdata)
                xml_text = '<application xmlns:android="http://schemas.android.com/apk/res/android">' + meta_data_note_object.cdata + ' </application>'
                doc = fromstring(xml_text)

                # 文本转成 element 之后，该对象可以当做列表取子节点
                for cnode in doc:
                    xpath_node.append(copy.copy(cnode))

            # xml内容 写入 androidManifest.xml 文件 这种写法的话，会丢失xml的开头定义 <?xml version='1.0' encoding='UTF-8'?>
            # write_content_to_file(manifest_file_path, tostring(manifest_doc).decode("utf-8"))
            # 将element转为elementTree 使用etree.write将xml对象写入文件，可设置xml_declaration、standalone
            root_elemnt = ElementTree(manifest_doc)
            root_elemnt.write(manifest_file_path, pretty_print=True, xml_declaration=True, encoding='utf-8')

            logger.debug(" 替换mate—date的androidmanifest：%s" % tostring(manifest_doc).decode("utf-8"))

    def _get_xml_attribute_name(self, attribute_name, element_node):
        element_namespace_dict = element_node.nsmap
        if attribute_name.find(":") > 0:
            xml_namespace = attribute_name.split(":")[0]
            xml_attri_name = attribute_name.split(":")[1]
            if xml_namespace in element_namespace_dict:
                xml_attribute_qname = QName(element_namespace_dict[xml_namespace], xml_attri_name)
                return xml_attribute_qname
            else:
                logger.debug("[WARN] xml的命名空间没有该key值 %s" % xml_namespace)
                return attribute_name
        else:
            logger.debug("[WARN] 传入的属性值没有命名空间 %s" % attribute_name)
            return attribute_name

    def _write_assets_ci_dependency_file(self, dependency_strbuffer):
        """
        生成app/assets/ci/dependency.txt文件
        ${workspace}:
            ├── app
            │   ├── assets
            │        ├── ci
            │             ├── dependency.txt
        :param dependency_strbuffer:
        :return:
        """
        ci_dir_path = os.path.join(os.getcwd(), "app/assets/ci")
        if not os.path.exists(ci_dir_path):
            os.mkdir(ci_dir_path)
        write_content_to_file(os.path.join(ci_dir_path, "dependency.txt"), dependency_strbuffer)
