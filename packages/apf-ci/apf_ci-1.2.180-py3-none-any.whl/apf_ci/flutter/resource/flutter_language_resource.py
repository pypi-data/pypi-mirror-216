#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = '961111'

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from apf_ci.util.file_utils import *
from apf_ci.flutter.resource.flutter_resource import *
import re


class FlutterLanguageResource(FlutterResource):

    def load(self):
        """
        加载Flutter语言资源
        :return:
        """
        # 根据Flutter组件依赖预先创建语言目录，防止后续异步创建目录带来的语言文件丢失问题
        biz_component_array = []
        for index in range(len(self.flutter_component_dependency)):
            comp_info = list(self.flutter_component_dependency.keys())[index]
            flutter_package_list = self.flutter_component_dependency[comp_info]
            comp_info_split = comp_info.split(':')
            biz_component_array.append(comp_info_split[1])
            for flutter_package in flutter_package_list:
                flutter_package_name = flutter_package['package_name']
                flutter_language_path = os.path.join(self.flutter_template_path, 'l10n', flutter_package_name)
                if not os.path.exists(flutter_language_path):
                    os.makedirs(flutter_language_path)
        self.unzip_language()
        for biz_component in biz_component_array:
            biz_component_tmp_path = os.path.join(self.flutter_template_path, 'l10n', biz_component)
            if os.path.exists(biz_component_tmp_path):
                # 在拷贝完成后删除临时目录
                shutil.rmtree(biz_component_tmp_path)

    def unzip_language(self):
        """
        解压语言资源
        :return:
        """
        logger.info(' 开始unzip flutter language')
        flutter_language_path = os.path.join(self.target_path, 'languageTemp', 'flutter')
        if not os.path.exists(flutter_language_path):
            os.makedirs(flutter_language_path)
        flutter_language_file = os.listdir(flutter_language_path)
        flutter_language_file.sort()

        language_md5_buffer = ''

        unzip_language_array = []
        for file_name in flutter_language_file:
            zip_file_path = os.path.join(flutter_language_path, file_name)
            # 计算md5值
            language_md5 = self.get_file_md5(zip_file_path)
            if language_md5:
                # 将所有zip的md5值汇总
                language_md5_buffer += language_md5
            unzip_language_json = {}
            unzip_language_json['zip_file_path'] = zip_file_path
            unzip_language_json['file_name'] = file_name
            unzip_language_array.append(unzip_language_json)

        self._multi_unzip_language_pool(unzip_language_array)
        self.md5_buffer = language_md5_buffer
        logger.info(' unzip flutter language完毕')

    def _multi_unzip_language_pool(self, unzip_language_array):
        """
        多线程解压语言资源
        :param unzip_language_array:
        :return:
        """
        logger.info('multi unzip languages...')
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(self._unzip_all_language, unzip_language_array)
            for result in results:
                if not result:
                    raise Exception("[ERROR]资源初始化失败，请检查并更新资源后重试")
            # for args in unzip_language_array:
            #     executor.submit(self._unzip_all_language, args).add_done_callback(self.process_callback)
            #     if self.flutter_resource_error_flag:
            #         break

        end = time.time()
        logger.info('耗时：%s秒' % str(end - start))

    def _unzip_all_language(self, unzip_language_json):
        """
        解压语言资源
        :param unzip_language_json:
        :return:
        """
        zip_file_path = unzip_language_json['zip_file_path']
        file_name = unzip_language_json['file_name']

        filename_array = file_name.replace(".zip", "").split("###")
        namespace = filename_array[0]
        biz_name = filename_array[1]
        language_name = filename_array[2]

        # 获取移动业务组件依赖的Flutter组件
        flutter_component_array = []
        biz_component_key = namespace + ":" + biz_name
        for biz_component in self.flutter_component_dependency:
            if biz_component.startswith(biz_component_key):
                for flutter_package in self.flutter_component_dependency[biz_component]:
                    flutter_component_array.append(flutter_package['package_name'])

        file_zip = zipfile.ZipFile(zip_file_path, 'r')
        # 先解压至临时目录
        unzip_path = os.path.join(self.flutter_template_path, 'l10n', biz_name, 'tmp', language_name)
        for file in file_zip.namelist():
            self.unzip_file_with_path(file_zip, file, unzip_path)
        file_zip.close()
        # 将临时目录中的语言资源拷贝至正式目录
        # 开始读取i18n目录下的文件
        language_i18n_path = os.path.join(self.flutter_template_path, 'l10n', biz_name, 'tmp', language_name, 'i18n')
        language_file_array = os.listdir(language_i18n_path)
        for language_file in language_file_array:
            file_split = os.path.splitext(language_file)
            language_file_name = file_split[0]
            # 校验移动业务组件是否依赖该Flutter组件
            if language_file_name not in flutter_component_array:
                logger.error(LoggerErrorEnum.INVALID_ARGUMENT, "移动业务组件 " + biz_component_key + " 下不存在Flutter组件 " + language_file_name + " 的依赖，请移除该Flutter组件资源")
                return False

            final_language_name = self.get_flutter_language_name(language_name)
            # Flutter语言包需要重命名，由xxx.json转为app_{language_type}.arb
            language_file_final_name = 'app_' + final_language_name + '.arb'
            language_file_source_path = os.path.join(language_i18n_path, language_file)
            language_file_target_path = os.path.join(self.flutter_template_path, 'l10n', language_file_name,
                                                     language_file_final_name)
            shutil.copyfile(language_file_source_path, language_file_target_path)

        # 在拷贝完成后删除临时目录
        shutil.rmtree(unzip_path)
        return True

    def get_flutter_language_name(self, language_name):
        """
        Flutter语言文件重命名
        :param language_name:
        :return:
        """
        final_language_name = language_name
        language_replace_dict = {
            'zh-Hans': 'zh',
            'zh-rHK': 'zh-Hant-HK',
            'zh-rTW': 'zh-Hant-TW',
            'zh-Hant': 'zh-Hant-TW'
        }
        if language_name in language_replace_dict:
            final_language_name = language_replace_dict[language_name]
        return final_language_name

if __name__ == '__main__':
    workspace = 'D:\\Downloads\\ap1668412616828_Application_Android_Factory'
    test_json = {}
    dragon_test_flutter_array = []
    dragon_test_flutter = {}
    dragon_test_flutter['package_name'] = 'flutter_comp2'
    dragon_test_flutter_array.append(dragon_test_flutter)
    test_json['com.nd.sdp.component:dragon-test-flutter:1'] = dragon_test_flutter_array
    flutter_test_comp = {}
    flutter_test_comp_array = []
    flutter_test_comp['package_name'] = 'flutter_comp1'
    flutter_test_comp_array.append(flutter_test_comp)
    test_json['com.nd.sdp.component:flutter-demo-1:1'] = flutter_test_comp_array
    flutter_resource = FlutterLanguageResource(os.path.join(workspace, 'flutter'), os.path.join(workspace, 'target'), test_json)
    final_language_name = flutter_resource.get_flutter_language_name('zh-Hant-HK')
    print("最终的语言：" + final_language_name)
