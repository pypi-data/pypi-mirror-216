#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = '961111'

import re
from concurrent.futures import ThreadPoolExecutor

from apf_ci.flutter.resource.flutter_resource import *


class FlutterSkinResource(FlutterResource):

    def load(self):
        """
        加载Flutter皮肤资源
        :return:
        """
        unzip_skin_array = self.unzip_skin()
        logger.info("开始在pubspec.yaml补充皮肤资源")
        workspace_path = os.getcwd()
        dependency_file_path = os.path.join(self.flutter_template_path, 'pubspec.yaml')
        dependency_file_content = read_file_content(dependency_file_path)
        flutter_skin_assets = '\nflutter:\n  assets:\n'
        for unzip_skin_json in unzip_skin_array:
            file_name = unzip_skin_json['file_name']
            flutter_skin_assets += '    - ' + os.path.join('assets', file_name, '') + '\n'

        final_dependency_file_content = re.sub(r"\nflutter:\n", flutter_skin_assets, dependency_file_content)
        write_content_to_file(dependency_file_path, final_dependency_file_content)
        logger.info("pubspec.yaml补充皮肤资源完成")

    def unzip_skin(self):
        """
        解压语言包到指定目录下
        :return:
        """
        logger.info(' 开始unzip flutter skin')
        flutter_skin_path = os.path.join(self.target_path, 'skinTemp', 'flutter')
        if not os.path.exists(flutter_skin_path):
            os.makedirs(flutter_skin_path)
        flutter_skin_file = os.listdir(flutter_skin_path)
        flutter_skin_file.sort()

        skin_md5_buffer = ''

        unzip_skin_array = []
        for file_name in flutter_skin_file:
            zip_file_path = os.path.join(flutter_skin_path, file_name)
            filename = file_name.replace('.zip', '').replace('###', '.')
            # 计算md5值
            skin_md5 = self.get_file_md5(zip_file_path)
            if skin_md5:
                # 将所有zip的md5值汇总
                skin_md5_buffer += skin_md5
            unzip_skin_json = {}
            unzip_skin_json['zip_file_path'] = zip_file_path
            unzip_skin_json['file_name'] = filename
            unzip_skin_array.append(unzip_skin_json)

        self._multi_unzip_skin_pool(unzip_skin_array)
        self.md5_buffer = skin_md5_buffer
        logger.info(' unzip flutter skin完毕')
        return unzip_skin_array

    def _multi_unzip_skin_pool(self, unzip_skin_array):
        """
        多线程解压
        :param unzip_skin_array:
        :return:
        """
        logger.info('multi unzip skin...')
        start = time.time()
        # 为避免触发file_zip.extract 这里先从8降为4试试
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self._unzip_all_skin, unzip_skin_array)

        end = time.time()
        logger.info('耗时：%s秒' % str(end - start))

    def _unzip_all_skin(self, unzip_skin_json):
        """
        解压皮肤资源
        :param unzip_skin_json:
        :return:
        """
        zip_file_path = unzip_skin_json['zip_file_path']
        file_name = unzip_skin_json['file_name']

        file_zip = zipfile.ZipFile(zip_file_path, 'r')
        unzip_path = os.path.join(self.flutter_template_path, 'assets', file_name)
        for file in file_zip.namelist():
            self.unzip_file_with_path(file_zip, file, unzip_path)
        file_zip.close()

if __name__ == '__main__':
    workspace = 'D:\\Downloads\\ap1668412616828_Application_Android_Factory'
    target = os.path.join(workspace, 'target', 'languageTemp', 'flutter')
    files = os.listdir(target)
    files.sort()
    for file in files:
        print(file)
    # test_json = {}
    # dragon_test_flutter_array = []
    # dragon_test_flutter = {}
    # dragon_test_flutter['package_name'] = 'flutter_comp2'
    # dragon_test_flutter_array.append(dragon_test_flutter)
    # test_json['com.nd.sdp.component:dragon-test-flutter:1'] = dragon_test_flutter_array
    # flutter_test_comp = {}
    # flutter_test_comp_array = []
    # flutter_test_comp['package_name'] = 'flutter_comp1'
    # flutter_test_comp_array.append(flutter_test_comp)
    # test_json['com.nd.sdp.component:flutter-demo-1:1'] = flutter_test_comp_array
    # flutter_resource = FlutterResource(os.path.join(workspace, 'flutter'), os.path.join(workspace, 'target'), test_json)
    # flutter_resource.load_language()
    # print("语言包md5:" + flutter_resource.language_md5)