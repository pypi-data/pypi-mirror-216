"""
flutter构建模块
"""

__author__ = '961111'

from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from abc import ABCMeta, abstractmethod


class FlutterBuild(metaclass=ABCMeta):

    def __init__(self, package_name, env, app_type, flutter_cs_config, flutter_template_path, flutter_command):
        self.package_name = package_name
        self.env = env
        self.app_type = app_type
        self.flutter_cs_config = flutter_cs_config
        self.flutter_template_path = flutter_template_path
        self.flutter_command = flutter_command
        self.language_resource_md5 = ''
        self.skin_resource_md5 = ''
        self.flutter_cs_cache_path = '/flutter/' + self.package_name + '/' + self.env + '/' + self.app_type

    @abstractmethod
    def build(self):
        """
        构建
        :return:
        """
        pass

    @abstractmethod
    def after_build(self):
        """
        在构建完执行的方法
        :return:
        """
        pass

    @abstractmethod
    def generate_cache(self):
        """
        生成缓存
        :return:
        """
        pass

    @abstractmethod
    def get_cache(self):
        """
        获取缓存
        :return:
        """
        pass

    def generate_md5_json(self):
        workspace_path = os.getcwd()
        # 计算pubspec.lock md5
        pubspec_lock_path = os.path.join(self.flutter_template_path, 'pubspec.lock')
        pubspec_lock_content = read_file_content(pubspec_lock_path)
        new_md5 = get_md5(pubspec_lock_content)

        md5_json = {
            'pubspec_lock': new_md5,
            'language_resource': self.language_resource_md5,
            'skin_resource': self.skin_resource_md5
        }

        # 在md5_json中写入二级缓存的下载地址
        result_download_key = 'result_download_url'
        result_download_url = self.flutter_cs_config.host + '/static/' + self.flutter_cs_config.server_name + self.flutter_cs_cache_path + '/android_aar.zip'
        if self.app_type == 'ios':
            result_download_url = self.flutter_cs_config.host + '/static/' + self.flutter_cs_config.server_name + self.flutter_cs_cache_path + '/Release.zip'
        md5_json[result_download_key] = result_download_url

        md5_json_file_name = 'md5.json'
        md5_json_path = os.path.join(self.flutter_template_path, md5_json_file_name)
        write_content_to_file(md5_json_path, json.dumps(md5_json))

        cs_path = '/flutter/' + self.package_name + '/' + self.env
        cs_file_name = md5_json_file_name
        cs_file_path = cs_path + '/' + cs_file_name
        # 上传md5文件
        upload_file_to_cs(md5_json_path, cs_path, cs_file_name, self.flutter_cs_config, cs_file_path)

    def generate_second_level_cache(self, cs_file_name, source_file_path):
        """
        保存二级缓存
        :param package_name:
        :param env:
        :param flutter_cs_config:
        :param cs_file_name:
        :param source_file_path:
        :return:
        """
        cs_file_path = self.flutter_cs_cache_path + '/' + cs_file_name
        logger.info("上传flutter 缓存文件:" + source_file_path + "   到CS:" + cs_file_path)
        upload_file_to_cs(source_file_path, self.flutter_cs_cache_path, cs_file_name, self.flutter_cs_config, cs_file_path)

    def generate_first_level_cache(self, source_file_name, source_file_path):
        """
        保存一级缓存
        :param package_name:
        :param env:
        :param app_type:
        :param source_file_path:
        :return:
        """
        workspace_path = os.getcwd()
        target_file_path = os.path.join(workspace_path, '..', '..', 'flutter_cache', self.package_name, self.env, self.app_type, source_file_name)
        copy_file(source_file_path, target_file_path)

    def get_first_level_cache(self, source_file_name, target_file_path):
        workspace_path = os.getcwd()
        source_file_path = os.path.join(workspace_path, '..', '..', 'flutter_cache', self.package_name, self.env, self.app_type, source_file_name)
        exists = os.path.exists(source_file_path)
        if exists:
            # 若一级缓存存在，则直接返回
            copy_file(source_file_path, target_file_path)
            return True

        return False

    def get_second_level_cache(self, cs_file_name, target_file_path):
        cache_file_url = get_cs_download_path(self.flutter_cs_config, '/flutter/' + self.package_name + '/' + self.env + '/' + self.app_type + '/' + cs_file_name)
        logger.info("下载flutter 缓存文件:" + cache_file_url + "   到本地:" + target_file_path)
        try:
            download_cs_file(cache_file_url, target_file_path, 3)
        except Exception:
            error_message = "下载flutter i缓存文件 %s" % cache_file_url
            logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, error_message)
            traceback.print_exc()
            return False

        return True

    def check_use_cache(self):
        md5_json_path = os.path.join(self.flutter_template_path, 'md5.json')
        url_timestamp = "?timestamp=" + str(int(time.time() * 1000))
        md5_json_url = get_cs_download_path(self.flutter_cs_config, '/flutter/' + self.package_name + '/' + self.env + '/md5.json' + url_timestamp)
        logger.info("下载md5:" + md5_json_url + "   到本地:" + md5_json_path)
        try:
            download_cs_file(md5_json_url, md5_json_path, 3)
        except Exception:
            error_message = "下载md5文件失败 %s" % md5_json_url
            logger.error(LoggerErrorEnum.DOWNLOAD_ERROR, error_message)
            traceback.print_exc()
            return False

        md5_json = read_file_content(md5_json_path)
        md5_json_content = json.loads(md5_json)
        old_md5 = md5_json_content['pubspec_lock']
        old_skin_md5 = md5_json_content.get('skin_resource')
        old_language_md5 = md5_json_content.get('language_resource')
        pubspec_lock_path = os.path.join(self.flutter_template_path, 'pubspec.lock')
        pubspec_lock_content = read_file_content(pubspec_lock_path)
        new_md5 = get_md5(pubspec_lock_content)
        if new_md5 != old_md5 \
                or old_language_md5 != self.language_resource_md5 \
                or old_skin_md5 != self.skin_resource_md5:
            # 若资源、配置md5存在更新，则不使用缓存
            logger.info("不使用缓存,开始构建")
            return False

        return True
