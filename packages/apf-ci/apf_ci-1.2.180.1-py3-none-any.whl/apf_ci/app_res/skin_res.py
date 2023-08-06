#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" a skin module """

__author__ = 'LianGuoQing'

from concurrent.futures import ProcessPoolExecutor
from apf_ci.util.http_utils import *
from apf_ci.util.file_utils import *
from apf_ci.util.log_factory.logger_error_enum import *
#from apf_ci.config.android_plugin import *


class SkinResource:
    def __init__(self, target_path, variables_json):
        self.target_path = target_path
        self.variables_json = variables_json

    def unzip_skin(self, android_json_obj, android_json):
        logger.info(' 开始unzip native skin')

        native_skin_path = os.path.join(self.target_path, 'skinTemp', 'native')
        if not os.path.exists(native_skin_path):
            os.makedirs(native_skin_path)
        native_skin_file = os.listdir(native_skin_path)
        app_type = self.variables_json['build_app_type']



        unzip_skin_array = []
        for file_name in native_skin_file:
            zip_file_path = os.path.join(native_skin_path, file_name)
            filename = file_name.replace('.zip', '').replace('###', '_')

            # 安卓插件不解压皮肤资源
            if android_json_obj.check_android_plugin(android_json, filename):
                continue

            unzip_skin_json = {}
            unzip_skin_json['zip_file_path'] = zip_file_path
            unzip_skin_json['filename'] = filename
            unzip_skin_json['app_type'] = app_type
            unzip_skin_array.append(unzip_skin_json)

        self._multi_unzip_skin_pool(unzip_skin_array)
        logger.info(' unzip native skin完毕')

    def _multi_unzip_skin_pool(self, unzip_skin_array):
        logger.info('multi unzip skin...')
        start = time.time()
        # 为避免触发file_zip.extract 这里先从8降为4试试
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = executor.map(self._unzip_all_skin, unzip_skin_array)
            for result in results:
                if result:
                    logger.info(' unzip result is: %s' % result)

        end = time.time()
        logger.info('耗时：%s秒' % str(end - start))

    def _unzip_all_skin(self, unzip_skin_json):
        zip_file_path = unzip_skin_json['zip_file_path']
        filename = unzip_skin_json['filename']
        app_type = unzip_skin_json['app_type']

        file_zip = zipfile.ZipFile(zip_file_path, 'r')
        if app_type.lower() == 'android':
            android_unzip_path = os.path.join(os.getcwd(), 'app')
            filename = filename.replace("-", "_").replace(".", "_")
            #logger.debug('filename=' + filename)
            for file in file_zip.namelist():
                logger.debug('解压组件：%s ，文件：%s ' % (filename,file))
                if file.endswith(".xml"):
                    if file.find("res/values") == -1:
                        exists_file_path = os.path.join(android_unzip_path, file)

                        if os.path.exists(exists_file_path):
                            logger.error(LoggerErrorEnum.FILE_ALREADY_EXIST,'组件：%s文件：%s已经存在，请检查皮肤包中是否存在同名文件！' % (filename, exists_file_path))
                            raise Exception('文件：%s已经存在，请检查皮肤包中是否存在同名文件！' % exists_file_path)
                        else:
                            file_zip.extract(file, android_unzip_path)
                    else:
                        data = file_zip.read(file)
                        temp_file = file.replace(".xml", "_" + filename + ".xml").lower()
                        self._create_file(os.path.join(android_unzip_path, temp_file), data)

                        #temp_time = time.time();
                        #file_zip.extract(file, os.path.join(android_unzip_path, temp_time))
                        #temp_file = file.replace(".xml", "_" + filename + ".xml").lower()
                        #shutil.move(os.path.join(android_unzip_path, temp_time, file), os.path.join(android_unzip_path, temp_file))
                else:

                    self.unzip_file_with_path(file_zip, file, android_unzip_path)

        elif app_type.lower() == 'ios':
            ios_unzip_path = os.path.join(os.getcwd(), 'ComponentAppBase', 'Resources', 'skin')
            for file in file_zip.namelist():
                #logger.debug('filename=' + filename)
                self.unzip_file_with_path(file_zip, file, ios_unzip_path)
        file_zip.close()

    def unzip_file_with_path(self, file_zip, file, unzip_path):
    # 这里多线程操作，extract内有创建目录操作，偶发会同时创建一个目录，暂无合适解决方案,捕获后再创建一次
    # 报错 FileExistsError: [Errno 17] File exists
        try:
            file_zip.extract(file, unzip_path)
        except Exception as e:
            logger.warning('file_zip.extract file: %s , unzip_path: %s' % (file, unzip_path))
            logger.warning(e)
            file_zip.extract(file, unzip_path)

    def _create_file(self, file_name_path, data):
        if not file_name_path.endswith('/'):
            index = file_name_path.rfind('/')
            parent_file_path = file_name_path[0:index]

            if not os.path.exists(parent_file_path):
                os.makedirs(parent_file_path)

            with open(file_name_path, 'wb') as code:
                code.write(data)




if __name__ == "__main__":
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')

    variables_path = os.path.join(target_path, 'variables.json')
    variables_data = read_file_content(variables_path)
    variables_json = json.loads(variables_data)

    download_type = 'react'

    #skin_resource = SkinResource(target_path, variables_json)
    # skin_resource.get_skin_resources(download_type)
    #skin_resource.unzip_skin()