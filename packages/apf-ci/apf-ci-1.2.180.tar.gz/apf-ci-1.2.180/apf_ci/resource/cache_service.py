#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger
from concurrent.futures import ProcessPoolExecutor

class CacheService:
    def __init__(self, app_type):
        self.base_path = "/data/jenkins/res"
        if platform.system() == "Darwin":
            self.base_path = "/usr/local/sdp/jenkins/res"
        self.app_type = app_type

    def resource_url_analysis(self, resource_url, cache_path, file_name, component_type, download_pool_array):
        download_zip_file_path = os.path.join(cache_path, file_name)
        # 验证是否有缓存,筛选出要下载的资源
        cache_contain_flag = self.check_zipfile_iscontain(download_zip_file_path)
        if cache_contain_flag:
            logger.debug(" 资源下载地址%s \n资源已经有缓存，资源为： %s , 缓存路径： %s " % (resource_url, file_name, cache_path))
        else:
            logger.debug(" 资源下载地址%s \n资源没有缓存，进入下载池等待下载。资源为： %s ，缓存路径: %s " % (resource_url, file_name, cache_path))
            url_path_json = {}
            url_path_json[resource_url] = download_zip_file_path
            download_pool_array.append(url_path_json)

    def check_zipfile_iscontain(self, download_zip_file_path):
        if os.path.exists(download_zip_file_path):
            return True
        else:
            return False


    def check_is_unzip(self, unzip_path):
        if os.path.exists(unzip_path):
            return True
        else:
            return False

    def download_new_resource(self, download_pool_array):
        logger.info("开始下载新的缓存资源。\ndownload files...")
        start = time.time()
        multi_download_pool(download_pool_array)
        logger.info("下载新的缓存资源结束，耗时 %s" % (time.time() - start))

    def unzip_new_resource(self, unzip_pool_array, resource_type):
        logger.info("开始解压新的缓存资源。\nunzip files...")
        start = time.time()
        if resource_type == "skin":
            with ProcessPoolExecutor(max_workers=8) as executor:
                executor.map(self.unzip_skin_resource, unzip_pool_array)
        elif resource_type == "language":
            with ProcessPoolExecutor(max_workers=8) as executor:
                executor.map(self.unzip_language_resource, unzip_pool_array)
        logger.info("解压新的缓存资源结束，耗时 %s" % (time.time() - start))

    def unzip_skin_resource(self, unzip_resource_json):
        zip_file_path = unzip_resource_json['zip_file_path']
        file_zip = zipfile.ZipFile(zip_file_path, 'r')
        app_type = self.app_type

        # 解压存放的目录
        path_sub = zip_file_path.rfind("/")
        target_path = os.path.join(zip_file_path[:path_sub], "unzip")
        logger.debug(" 解压的文件路径为: %s \n 解压目录为: %s" % (zip_file_path, target_path))
        # 解析file_name
        file_name = zip_file_path[path_sub + 1:]
        file_name = file_name.replace('.zip', '').replace('###', '_')

        if app_type.lower() == 'android':
            filename = file_name.replace("-", "_").replace(".", "_")
            #logger.debug('filename='+filename)
            for file in file_zip.namelist():
                if file.endswith(".xml"):
                    if file.find("res/values") == -1:
                        exists_file_path = os.path.join(target_path, file)

                        if os.path.exists(exists_file_path):
                            logger.debug('组件：%s文件：%s已经存在，请检查皮肤包中是否存在同名文件！' % (filename, exists_file_path))
                            raise Exception('文件：%s已经存在，请检查皮肤包中是否存在同名文件！' % exists_file_path)
                        else:
                            file_zip.extract(file, target_path)
                    else:
                        data = file_zip.read(file)
                        temp_file = file.replace(".xml", "_" + filename + ".xml").lower()
                        self._create_file(os.path.join(target_path, temp_file), data)
                else:
                    file_zip.extract(file, target_path)
        elif app_type.lower() == 'ios':
            for file in file_zip.namelist():
                file_zip.extract(file, target_path)
        file_zip.close()

    def unzip_language_resource(self, unzip_resource_json):
        zip_file_path = unzip_resource_json['zip_file_path']
        file_zip = zipfile.ZipFile(zip_file_path, 'r')
        app_type = self.app_type

        # 解压存放的目录
        path_sub = zip_file_path.rfind("/")
        target_path = os.path.join(zip_file_path[:path_sub], "unzip")
        logger.debug(" 语言资源解压的文件路径为: %s \n 解压目录为: %s" % (zip_file_path, target_path))
        # 解析file_name
        file_name = zip_file_path[path_sub + 1:]

        filename_array = file_name.replace(".zip", "").split("###")
        namespace = filename_array[0]
        biz_name = filename_array[1]
        language_name = filename_array[2]

        if app_type.lower() == 'android':
            namespace = namespace.replace('-', '_').replace('.', '_').lower()
            biz_name = biz_name.replace('-', '_').replace('.', '_').lower()
            for file in file_zip.namelist():
                rename_file = ''
                file_path_list = self.__get_pakg_name(language_name, file)
                for file_path in file_path_list:
                    rename_file += '/' + file_path

                if file.endswith('.xml'):
                    rename_file = rename_file.replace('.xml', '_' + namespace + '_' + biz_name + '.xml')

                data = file_zip.read(file)
                unzip_file_path = target_path + rename_file
                self._create_file(unzip_file_path, data)

        elif app_type.lower() == 'ios':
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
                unzip_file_path = os.path.join(target_path, rename)
                self._create_file(unzip_file_path, data)
        file_zip.close()

    def copy_cache_into_job(self, copy_pool_array, resource_type, target_dest_path=None):
        target_path = ""
        workspace_path = os.getcwd()
        app_type = self.app_type
        if target_dest_path is None:
            if resource_type == "skin":
                target_path = os.path.join(workspace_path, 'target', 'skinTemp')
            elif resource_type == "language":
                target_path = os.path.join(workspace_path, 'target', 'languageTemp')
        else :
            target_path = target_dest_path;
        if target_path.strip():
            for copy_json in copy_pool_array:
                source_path = copy_json["source_path"]
                file_name = copy_json["file_name"]
                component_type = copy_json["component_type"]
                dest_path = os.path.join(target_path, component_type, file_name)
                copy_file(source_path, dest_path)

    def copy_directory(self, source_dir, target_dir, app_type):
        # 复制一整个文件目录结构以及文件
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        if not os.path.isdir(source_dir):
            logger.warning('copy_directory：source_dir参数必须为 目录类型, 路径：%s' % source_dir)
        else:
            # 复制层级结构
            for file in os.listdir(source_dir):
                source_f = os.path.join(source_dir, file)
                target_f = os.path.join(target_dir, file)
                if os.path.isfile(source_f):
                    shutil.copy(source_f, target_f)
                    # logger.debug(" copy_directory：拷贝文件: %s 到目录下： %s" % (file, target_f))
                if os.path.isdir(source_f):
                    if not os.path.exists(target_f):
                        os.mkdir(target_f)
                        # logger.debug(" copy_directory：复制的目标目录不存在，创建目录： %s" % target_f)
                    self.copy_directory(source_f, target_f, app_type)

    def __get_pakg_name(self, language_name, path):
        path_name_list = path.split('/')
        length = len(path_name_list)
        if length >= 2:
            if path_name_list[1].startswith('values'):
                if language_name == 'en':
                    path_name_list[1] = 'values'
                else:
                    path_name_list[1] = 'values-' + language_name
            elif path_name_list[1].startswith('drawable'):
                if not (language_name == 'en'):
                    drawables_list = path_name_list[1].split('-')
                    if len(drawables_list) == 1:
                        path_name_list[1] = drawables_list[0] + '-' + language_name;
                    else:
                        path_name_list[1] = path_name_list[1].replace(drawables_list[0], drawables_list[0] + '-' + language_name)
        return path_name_list

    def _create_file(self, file_name_path, data):
        if not file_name_path.endswith('/'):
            index = file_name_path.rfind('/')
            parent_file_path = file_name_path[0:index]

            if not os.path.exists(parent_file_path):
                os.makedirs(parent_file_path)

            with open(file_name_path, 'wb') as code:
                code.write(data)