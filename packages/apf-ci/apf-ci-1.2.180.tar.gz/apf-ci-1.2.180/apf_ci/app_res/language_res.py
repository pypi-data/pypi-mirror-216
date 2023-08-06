#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
a language module
"""

__author__ = 'LianGuoQing'

from concurrent.futures import ProcessPoolExecutor
from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *


class LanguageRes:
    def __init__(self, target_path, variables_json):
        self.target_path = target_path
        self.variables_json = variables_json


    def unzip_language(self, android_plugin, android_plugin_json, target_path=None, en_language_unzip_dir=None):
        logger.info(' 开始unzip native language')
        native_language_path = None
        if target_path is None:
            native_language_path = os.path.join(self.target_path, 'languageTemp', 'native')
        else:
            native_language_path = target_path
        if not os.path.exists(native_language_path):
            os.makedirs(native_language_path)
        native_language_file = os.listdir(native_language_path)
        app_type = self.variables_json['build_app_type']

        unzip_language_array = []
        for file_name in native_language_file:
            zip_file_path = os.path.join(native_language_path, file_name)

            # 安卓插件不解压语言资源
            filename_array = file_name.replace(".zip", "").split("###");
            namespace = filename_array[0]
            biz_name = filename_array[1]
            plugin_name = str('%s_%s' % (namespace, biz_name))
            if android_plugin.check_android_plugin(android_plugin_json, plugin_name):
                continue;

            unzip_language_json = {}
            unzip_language_json['zip_file_path'] = zip_file_path
            unzip_language_json['file_name'] = file_name
            unzip_language_json['app_type'] = app_type
            unzip_language_json['en_language_unzip_dir'] = en_language_unzip_dir
            unzip_language_array.append(unzip_language_json)

        self._multi_unzip_language_pool(unzip_language_array)
        logger.info(' unzip native language完毕')

    def _multi_unzip_language_pool(self, unzip_language_array):
        logger.info('multi unzip languages...')
        start = time.time()
        with ProcessPoolExecutor(max_workers=8) as executor:
            executor.map(self._unzip_all_language, unzip_language_array)

        end = time.time()
        logger.info('耗时：%s秒' % str(end - start))

    def _unzip_all_language(self, unzip_language_json):
        zip_file_path = unzip_language_json['zip_file_path']
        file_name = unzip_language_json['file_name']
        app_type = unzip_language_json['app_type']

        filename_array = file_name.replace(".zip", "").split("###")
        namespace = filename_array[0]
        biz_name = filename_array[1]
        language_name = filename_array[2]
        en_language_unzip_dir = unzip_language_json.get('en_language_unzip_dir')

        file_zip = zipfile.ZipFile(zip_file_path, 'r')

        if app_type.lower() == 'android':
            namespace = namespace.replace('-', '_').replace('.', '_').lower()
            biz_name = biz_name.replace('-', '_').replace('.', '_').lower()
            #language_name = language_name.replace('-', '_').replace('.', '_')
            android_unzip_path = os.path.join(os.getcwd(), 'app')

            for file in file_zip.namelist():
                rename_file = ''
                file_path_list = self._get_pakg_name(language_name, file, en_language_unzip_dir)

                for file_path in file_path_list:
                    rename_file += '/' + file_path

                if file.endswith('.xml'):
                    rename_file = rename_file.replace('.xml', '_' + namespace + '_' + biz_name + '.xml')

                data = file_zip.read(file)
                unzip_file_path = android_unzip_path + rename_file
                logger.debug('解压组件语言包：%s ，文件：%s 到 %s' % (file_name, file, rename_file))
                self._create_file(unzip_file_path, data)

        elif app_type.lower() == 'ios':
            ios_unzip_path = os.path.join(os.getcwd(), 'ComponentAppBase', 'Resources', 'i18n')
            for file in file_zip.namelist():
                rename = file
                pre_str = ''
                i18n_bundle = '%s.%s_i18n.bundle' % (namespace, biz_name)

                if rename.find(i18n_bundle) == -1:
                    pre_str += '%s/' % i18n_bundle
                    if rename.find(language_name + '.lproj') == -1:
                        pre_str += '%s.lproj/' % language_name
                    rename = pre_str + rename
                else:
                    pre_str += '%s/' % i18n_bundle
                    temp_name = rename.replace(i18n_bundle + '/', '')
                    if temp_name.find(language_name + '.lproj') == -1:
                        pre_str += '%s.lproj/' % language_name
                    rename = pre_str + temp_name

                data = file_zip.read(file)
                unzip_file_path = os.path.join(ios_unzip_path, rename)
                self._create_file(unzip_file_path, data)
        file_zip.close()

    def _get_pakg_name(self, language_name, path, en_language_unzip_dir):
        path_name_list = path.split('/')
        length = len(path_name_list)
        if length >= 2:
            if path_name_list[1].startswith('values'):
                if language_name == 'en' and en_language_unzip_dir is not None:
                    path_name_list[1] = en_language_unzip_dir
                else:
                    path_name_list[1] = 'values-' + language_name
            elif path_name_list[1].startswith('drawable'):
                if not (language_name == 'en'):
                    drawables_list = path_name_list[1].split('-')
                    if len(drawables_list) == 1:
                        path_name_list[1] = drawables_list[0] + '-' + language_name;
                    else:
                        path_name_list[1] = path_name_list[1].replace(drawables_list[0],
                                                                      drawables_list[0] + '-' + language_name)
        return path_name_list

    def _create_file(self, file_name_path, data):
        if not file_name_path.endswith('/'):
            index = file_name_path.rfind('/')
            parent_file_path = file_name_path[0:index]

            if not os.path.exists(parent_file_path):
                os.makedirs(parent_file_path)

            with open(file_name_path, 'wb') as code:
                code.write(data)

    def _android_en_language_resource_handle(self, app_type, download_language_array, cache_switch, language_resource,
                                             language_res, cache_service, android_plugin, android_plugin_json,
                                             variables_json):
        app_exist_en_language = False
        en_language_name = None
        en_language_json = None
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, 'target', 'languageTemp_en')
        all_languages_json_array = variables_json['allLanguages']
        for languages_json in all_languages_json_array:
            each_language_name = languages_json['name']
            if "en" == each_language_name.lower():
                en_language_name = each_language_name
                en_language_json = languages_json

        for language_name in download_language_array:
            if "en" != language_name.lower():
                continue
            app_exist_en_language = True

        if app_exist_en_language:
            # 英语存在，进行拷贝/res/values-en到/res/values, 只要values-en,其他的不用管了
            logger.debug(' android native en language -- 英语存在，进行拷贝/res/values-en到/res/values, 只要values-en,其他的不用管了')
            workspace_path = os.getcwd()
            source_dir = os.path.join(workspace_path, 'app', 'res', 'values-en')
            target_dir = os.path.join(workspace_path, 'app', 'res', 'values')
            copy_directory(source_dir, target_dir)
            logger.debug(' android native en language 完毕-- 英语存在，进行拷贝/res/values-en到/res/values, 只要values-en,其他的不用管了')
        else:
            # 英语不存在，进行解压到/res/values
            logger.debug(' android native en language -- 英语不存在，进行下载、解压到/res/values')
            en_language_arr = []
            en_language_arr.append(en_language_json)
            download_language_array = language_resource.get_language_resources(None, en_language_arr)
            language_resources_array = download_language_array[en_language_name]
            if cache_switch:
                resource_type = "language"
                download_pool_array, copy_pool_array = language_resource.language_resource_cache_handle(
                    language_resources_array, en_language_name, download_type=None)
                # 未命中的统一下载
                cache_service.download_new_resource(download_pool_array)
                # 将资源拷贝到工作空间的目录下
                cache_service.copy_cache_into_job(copy_pool_array, resource_type, target_path)
            else:
                language_resource.download_language(app_type, 'en', language_resources_array,
                                                    None, target_path)
            target_path = os.path.join(workspace_path, 'target', 'languageTemp_en', "native")
            language_res.unzip_language(android_plugin, android_plugin_json, target_path, "values")
            logger.debug(' android native en language 完毕-- 英语不存在，进行下载、解压到/res/values')


if __name__ == "__main__":
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')

    variables_path = os.path.join(target_path, 'variables.json')
    variables_data = read_file_content(variables_path)
    variables_json = json.loads(variables_data)

    download_type = 'react'
    #
    #language_resource = LanguageResource(target_path, variables_json)
    #language_resource.get_language_resources(download_type)
    #language_resource.unzip_language()
