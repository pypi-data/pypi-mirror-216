"""
flutter ios 构建模块
"""

__author__ = '961111'

from apf_ci.flutter.flutter_build import *
from apf_ci.flutter.flutter_command_utils import execute_command


class FlutterIosBuild(FlutterBuild):

    def after_build(self):
        pass

    def build(self):
        """
        ios构建flutter
        :return:
        """
        logger.info("开始构建flutter ios")
        execute_command([self.flutter_command, 'build', 'ios-framework', '--output=./build/ios/framework', '--no-debug', '--no-profile'], chdir=self.flutter_template_path)
        logger.info("构建flutter ios完成")

    def generate_cache(self):
        framework_path = os.path.join(self.flutter_template_path, 'build', 'ios', 'framework')
        release_zip_name = 'Release.zip'
        release_path = os.path.join(framework_path, 'Release')
        release_zip_path = os.path.join(framework_path, release_zip_name)

        zipDir(release_path, release_zip_path)

        # 保存二级缓存
        self.generate_second_level_cache(release_zip_name, release_zip_path)

        # 保存一级缓存
        self.generate_first_level_cache(release_zip_name, release_zip_path)

        # 保存md5文件
        self.generate_md5_json()

    def get_cache(self):
        check_md5 = self.check_use_cache()
        if not check_md5:
            return False

        release_zip_name = 'Release.zip'
        release_zip_path = os.path.join(self.flutter_template_path, 'build', 'ios', 'framework',
                                        release_zip_name)
        # 从一级缓存中获取
        first_level_cache_exits = self.get_first_level_cache(release_zip_name, release_zip_path)
        if not first_level_cache_exits:
            # 从二级缓存中获取
            second_level_cache_exits = self.get_second_level_cache(release_zip_name, release_zip_path)
            if not second_level_cache_exits:
                return False

            logger.info("获取到二级缓存文件")
            # 将二级缓存中的文件复制到一级缓存中
            self.generate_first_level_cache(release_zip_name, release_zip_path)
        else:
            logger.info("获取到一级缓存文件")

        release_unzip_path = os.path.join(self.flutter_template_path, 'build', 'ios', 'framework', 'Release')
        unzip(release_zip_path, release_unzip_path)
        return True

