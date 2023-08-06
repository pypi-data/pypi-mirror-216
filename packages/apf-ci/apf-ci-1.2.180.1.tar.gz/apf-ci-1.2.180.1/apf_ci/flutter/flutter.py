"""
flutter模块
"""

__author__ = '961111'

from apf_ci.flutter.flutter_android_build import *
from apf_ci.flutter.flutter_ios_build import *
from apf_ci.flutter.resource.flutter_language_resource import *
from apf_ci.flutter.resource.flutter_skin_resource import *
from apf_ci.util.upload_utils import *
import platform


class FlutterService:

    def __init__(self):
        workspace_path = os.getcwd()
        variables_json_path = os.path.join(workspace_path, 'target', 'variables.json')
        variables_json_file = read_file_content(variables_json_path)
        variables_json = json.loads(variables_json_file)
        self.app_name = variables_json['build_app_name']
        self.package_name = variables_json['build_package']
        self.env = variables_json['env_target']
        self.app_type = variables_json['build_app_type']

        self.flutter_sdk_version, self.flutter_sdk_cache_home, self.flutter_command = self.get_flutter_config()

        # 此处复用h5的cs配置
        flutter_cs_config = ContentServiceConfig()
        flutter_cs_config.user_id = variables_json["local_h5_cs_user_id"]
        flutter_cs_config.host = variables_json["local_h5_cs_host"]
        flutter_cs_config.server_name = variables_json["local_h5_cs_server_name"]
        flutter_cs_config.session_id = variables_json["local_h5_cs_session_id"]
        flutter_cs_config.secret_key = variables_json["local_h5_cs_secret_key"]
        flutter_cs_config.access_key = variables_json["local_h5_cs_access_key"]
        self.flutter_cs_config = flutter_cs_config

        if self.app_type == 'android':
            self.flutter_template_path = os.path.join(workspace_path, 'flutter')
            self.flutter_build_service = FlutterAndroidBuild(
                self.package_name,
                self.env,
                self.app_type,
                self.flutter_cs_config,
                self.flutter_template_path,
                self.flutter_command
            )
        else:
            self.flutter_template_path = os.path.join(workspace_path, 'target', 'flutter')
            self.flutter_build_service = FlutterIosBuild(
                self.package_name,
                self.env,
                self.app_type,
                self.flutter_cs_config,
                self.flutter_template_path,
                self.flutter_command
            )

    def prepare_flutter_sdk(self):
        """
        预安装Flutter SDK
        :return:
        """
        flutter_download_url = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/linux/flutter_linux_%s-stable.tar.xz" % self.flutter_sdk_version
        flutter_zip_name = "flutter_linux_%s-stable.tar.xz" % self.flutter_sdk_version
        if platform.system() == "Darwin":
            # 若为mac机器
            machine = platform.machine()
            # 默认为x64架构CPU
            flutter_download_url = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/macos/flutter_macos_%s-stable.zip" % self.flutter_sdk_version
            flutter_zip_name = "flutter_macos_%s-stable.zip" % self.flutter_sdk_version
            if machine.__contains__('arm'):
                # 若为arm架构CPU
                flutter_download_url = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_%s-stable.zip" % self.flutter_sdk_version
                flutter_zip_name = "flutter_macos_arm64_%s-stable.zip" % self.flutter_sdk_version

        if not os.path.exists(self.flutter_sdk_cache_home):
            # 若Flutter SDK安装目录不存在，则创建
            os.mkdir(self.flutter_sdk_cache_home)

        flutter_version_path = os.path.join(self.flutter_sdk_cache_home, self.flutter_sdk_version)
        if not os.path.exists(flutter_version_path):
            # 若fvm home下无该Flutter SDK版本，则进行安装
            zip_path = os.path.join(self.flutter_sdk_cache_home, flutter_zip_name)
            flutter_sdk_init = True
            count = 0
            while True:
                # 若有其他线程在进行Flutter SDK安装，则进行等待
                if not os.path.exists(zip_path):
                    break
                if count >= 20:
                    # 默认等待20分钟，若仍未安装好，则可能存在下载中断的情况，直接删除
                    os.remove(zip_path)
                    raise Exception('[ERROR] 安装Flutter SDK过程出现异常')
                flutter_sdk_init = False
                logger.info(self.flutter_sdk_version + "  正在安装中")
                # 一分钟轮询一次
                time.sleep(60)
                count = count + 1

            if flutter_sdk_init:
                logger.info("指定的Flutter SDK " + self.flutter_sdk_version + "不存在，进行预安装")
                download_large_file(flutter_download_url, zip_path)
                source_path = os.path.join(self.flutter_sdk_cache_home, 'flutter')
                target_path = os.path.join(self.flutter_sdk_cache_home, self.flutter_sdk_version)
                self.unzip_flutter_sdk(zip_path, source_path, target_path)
                os.remove(zip_path)
                logger.info("Flutter SDK " + self.flutter_sdk_version + "安装完成")
        else:
            logger.info("目标Flutter SDK " + self.flutter_sdk_version + "已存在")

    def unzip_flutter_sdk(self, zip_path, source_path, target_path):
        if zip_path.endswith('tar.xz'):
            # tar.xz方式解压
            execute_command(['tar', '-xJf', zip_path, '-C', self.flutter_sdk_cache_home], need_print=False)
        else:
            # zip方式解压
            execute_command(['unzip', zip_path, '-d', self.flutter_sdk_cache_home], need_print=False)
        execute_command(['mv', source_path, target_path], need_print=False)

    def get_flutter_config(self):
        """
        获取Flutter相关配置
        :return: Flutter SDK版本，fvm本地缓存目录，Flutter命令绝对路径
        """
        workspace_path = os.getcwd()
        build_config_path = os.path.join(workspace_path, 'target', 'build_config.json')
        build_config_content = read_file_content(build_config_path)
        build_config_json = json.loads(build_config_content)
        # 获取Flutter SDK版本
        # 优先从app的config.json 中获取app/assets/app_factory/app/config.json
        app_config_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory', 'app', 'config.json')
        app_config_content = read_file_content(app_config_path)
        app_config_json = json.loads(app_config_content)
        flutter_config_array = app_config_json.get('flutter')
        flutter_sdk_version = ''
        if flutter_config_array:
            for target_flutter_json in flutter_config_array:
                if not isinstance(target_flutter_json, dict):
                    continue
                flutter_sdk_version = target_flutter_json['flutter_sdk_version']
                break
        if flutter_sdk_version == '':
            # 若app配置中不存在flutter sdk版本，则获取构建配置中的版本
            flutter_sdk_version = build_config_json['flutter_sdk_default_version']
        logger.info("使用Flutter SDK:" + flutter_sdk_version)

        # 获取本地缓存路径（Flutter SDK安装目录）
        flutter_sdk_home = build_config_json['flutter_sdk_home_android']
        if platform.system() == "Darwin":
            # 若为ios，则获取ios安装目录
            flutter_sdk_home = build_config_json['flutter_sdk_home_ios']
        # 获取flutter命令绝对路径
        flutter_command = os.path.join(flutter_sdk_home, flutter_sdk_version, 'bin', 'flutter')
        return flutter_sdk_version, flutter_sdk_home, flutter_command

    def perform(self, args):
        """
        Flutter构建插件入口
        :param args:
        :return:
        """
        workspace_path = os.getcwd()
        flutter_dependency = self.analyze_flutter_dependency()
        if flutter_dependency.__len__() <= 0:
            return
        # 当存在flutter依赖时，进行flutter相关构建
        # 准备环境
        self.prepare_flutter_sdk()

        self.clone_flutter_template_project()
        self.template_project_init()
        self.replace_flutter_package_dependency(flutter_dependency)
        # 加载资源
        flutter_skin_resource = FlutterSkinResource(self.flutter_template_path, os.path.join(workspace_path, 'target'),
                                                    flutter_dependency)
        flutter_language_resource = FlutterLanguageResource(self.flutter_template_path,
                                                            os.path.join(workspace_path, 'target'),
                                                            flutter_dependency)
        flutter_skin_resource.load()
        flutter_language_resource.load()
        self.flutter_build_service.skin_resource_md5 = flutter_skin_resource.md5_buffer
        self.flutter_build_service.language_resource_md5 = flutter_language_resource.md5_buffer
        # 拉取依赖
        self.pull_flutter_package()
        use_cache = self.flutter_build_service.get_cache()
        if not use_cache:
            # 若不使用缓存，则开始构建
            self.template_project_pre_build()
            self.build_project()
        self.flutter_build_service.after_build()

    def build_project(self):
        """
        发起构建
        :return:
        """
        self.flutter_build_service.build()
        self.flutter_build_service.generate_cache()

    def analyze_flutter_dependency(self):
        """
        解析flutter依赖
        :return:
        """
        logger.info("开始解析flutter依赖")
        workspace_path = os.getcwd()
        dependency_final_path = os.path.join(workspace_path, 'target', 'defines.json')
        dependency_final_file = read_file_content(dependency_final_path)
        dependency_final_json = json.loads(dependency_final_file)
        flutter_package_json = {}
        flutter_package_name_list = {}
        for index in range(len(dependency_final_json)):
            key = list(dependency_final_json.keys())[index]
            value = dependency_final_json[key]
            types_json = value['types']
            flutter_package_list = []
            for types_index in range(len(types_json)):
                types_key = list(types_json.keys())[types_index]
                if types_key != 'flutter':
                    continue
                types_value = types_json[types_key]
                flutter_dependency_array = types_value['dependency']
                for flutter_package in flutter_dependency_array:
                    flutter_package_name = flutter_package['package_name']
                    flutter_package_name_list[flutter_package_name] = key
                    flutter_package_list.append(flutter_package)
            if flutter_package_list.__len__() > 0:
                flutter_package_json[key] = flutter_package_list
        logger.info("解析flutter依赖完成")

        return flutter_package_json

    def replace_flutter_package_dependency(self, flutter_package_json):
        """
        将flutter依赖包替换到pubspec.yaml中
        :param flutter_package_json:
        :return:
        """
        logger.info("开始替换flutter依赖文件")
        workspace_path = os.getcwd()
        dependency_file_path = os.path.join(self.flutter_template_path, 'pubspec.yaml')
        data = read_file_content(dependency_file_path)
        match = re.search(r"^dependencies:\s*flutter:\s*sdk: flutter$", data, re.S | re.M)
        old_dependencies = ''
        if match:
            old_dependencies = match.group()

        dependencies = old_dependencies
        for index in range(len(flutter_package_json)):
            comp_info = list(flutter_package_json.keys())[index]
            dependencies += '\n  # from ' + comp_info
            flutter_package_list = flutter_package_json[comp_info]
            for flutter_package in flutter_package_list:
                flutter_package_name = flutter_package['package_name']
                flutter_package_version = flutter_package['version']
                dependencies += '\n  ' + flutter_package_name + ': ' + flutter_package_version

        final_data = data.replace(old_dependencies, dependencies)
        write_content_to_file(dependency_file_path, final_data)
        logger.info("替换flutter依赖文件完成")

    def pull_flutter_package(self):
        """
        拉取flutter依赖包
        :return:
        """
        logger.info("开始替换flutter依赖包")
        execute_command([self.flutter_command, '--version'], chdir=self.flutter_template_path)
        execute_command([self.flutter_command, 'pub', 'get'], chdir=self.flutter_template_path)
        logger.info("拉取flutter依赖完成")

    def template_project_init(self):
        """
        初始化flutter模板工程
        :return:
        """
        logger.info("开始执行flutter init.sh")

        execute_command(['chmod', '755', './scripts/init.sh'], chdir=self.flutter_template_path)
        execute_command(['sh', './scripts/init.sh', '--project-name', self.app_name, '--android-identifier', self.package_name, '--ios-identifier', self.package_name], chdir=self.flutter_template_path)
        logger.info("执行flutter init.sh完成")

    def template_project_pre_build(self):
        """
        flutter模板工程预构建
        :return:
        """
        logger.info("开始执行flutter pre_build.sh")
        execute_command(['chmod', '755', './scripts/pre_build.sh'], chdir=self.flutter_template_path)
        execute_command(['sh', './scripts/pre_build.sh', '--flutter-command', self.flutter_command], chdir=self.flutter_template_path)
        logger.info("执行flutter pre_build.sh完成")

    def clone_flutter_template_project(self):
        """
        克隆flutter模板工程到工作空间
        :return:
        """
        workspace_path = os.getcwd()
        target_path = os.path.join(workspace_path, 'target')

        # 读取git_templates.json中flutter模板工程地质
        git_templates_path = os.path.join(target_path, 'git_templates.json')
        git_templates_data = read_file_content(git_templates_path)
        git_templates_json = json.loads(git_templates_data)
        flutter_git_templates = git_templates_json['flutter']
        flutter_git_templates_json = flutter_git_templates['git']
        flutter_git_templates_repository = flutter_git_templates_json['source']
        flutter_git_templates_commit_id = flutter_git_templates_json['commit-id']

        # 在target目录下clone flutter模板工程
        platform_name = platform.system()
        if platform_name == 'Windows':
            git_clone_command = [
                'git',
                'clone',
                '--depth',
                '1',
                flutter_git_templates_repository,
                '.'
            ]
            git_checkout_command = [
                'git',
                'checkout',
                flutter_git_templates_commit_id
            ]
        else:
            git_clone_command = [
                '/usr/bin/git',
                'clone',
                flutter_git_templates_repository,
                '.'
            ]
            git_checkout_command = [
                '/usr/bin/git',
                'checkout',
                flutter_git_templates_commit_id
            ]
        logger.info(" 命令: %s, 执行 /usr/bin/git clone %s ." % (git_clone_command, flutter_git_templates_repository))
        if not os.path.exists(self.flutter_template_path):
            os.mkdir(self.flutter_template_path)
        execute_command(git_clone_command, chdir=self.flutter_template_path)
        execute_command(git_checkout_command, chdir=self.flutter_template_path)
