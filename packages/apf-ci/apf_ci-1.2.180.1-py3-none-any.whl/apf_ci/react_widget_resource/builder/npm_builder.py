# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
import json
import platform
import sys

from apf_ci.constant.path_constant import PathConstant
from apf_ci.util.execute_command_utils import execute_command
from apf_ci.util.file_utils import *
from apf_ci.util.log_utils import logger
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
class NpmBuilder:

    def __init__(self, page, npm_dependencies, plugin_id_dir):
        self.page = page
        self.npm_dependencies = npm_dependencies
        self.plugin_id_dir = plugin_id_dir

    def perform(self, variables_json):
        try:
            logger.debug(" 当前pluginIdDir为：%s page为:%s" % (self.plugin_id_dir, self.page))
            module_str = self.page.id

            # 拷贝npm构建所需文件
            self.download_build_template_file(variables_json, module_str)

            # 更新package.json文件中dependencies节点信息
            workspace_path = os.getcwd()
            self.update_package_file(workspace_path, self.plugin_id_dir, module_str)

            # 将pages节点内容独立成一个page.json
            self.create_page_file(workspace_path, self.plugin_id_dir, module_str)

            # 将page下脚本文件压缩成zip包
            self.zip_page_project(workspace_path, self.plugin_id_dir, module_str)

            self.execute_npm_build(variables_json, self.plugin_id_dir, module_str)
        except Exception as e:
            traceback.print_exc()
            error_msg = "npm操作构建异常：%s" % e
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR,error_msg)
            sys.exit()

    def download_build_template_file(self, variables_json, module_str):

        workspace_path = os.getcwd()
        react_widget_path = os.path.join(workspace_path, "target", "react_widget")

        plugin_id_dir_path = os.path.join(react_widget_path, self.plugin_id_dir)
        if not os.path.exists(plugin_id_dir_path):
            os.makedirs(plugin_id_dir_path)

        module_path = os.path.join(plugin_id_dir_path, module_str)
        if not os.path.exists(module_path):
            os.makedirs(module_path)
        git_repository = variables_json["git_repository"]
        commit_id = variables_json["commit_id"]

        platform_name = platform.system()
        if platform_name == 'Windows':
            git_clone_command = ["git", "clone", git_repository, "."]
        else:
            git_clone_command = ["/usr/bin/git", "clone", git_repository, "."]
        logger.info(" 命令: %s, 执行 /usr/bin/git clone %s ." % (git_clone_command, git_repository))
        execute_command(git_clone_command, chdir=module_path)

        if platform_name == 'Windows':
            git_checkout_command = ["git", "checkout", commit_id]
        else:
            git_checkout_command = ["/usr/bin/git", "checkout", commit_id]
        logger.info(" 命令：%s, 执行 /usr/bin/git checkout %s ." % (git_checkout_command, commit_id))
        execute_command(git_checkout_command, chdir=module_path)

    def update_package_file(self, workspace_path, plugin_id_dir, module_str):
        """
        更新package_json_file.json文件
        :param workspace_path:
        :param plugin_id_dir:
        :param module_str:
        :return:
        """
        # 获取package.json文件内容
        package_path = PathConstant.MOUDLE_PACKAGE_JSON_FILE.replace("{PLUGIN_ID_DIR}", plugin_id_dir).replace(
            "{TAG_MOUDLE}", module_str)
        package_json_file_path = os.path.join(workspace_path, package_path)
        logger.debug(" [module]:%s  package_json_file_path: %s" % (module_str, package_json_file_path))

        package_json_content = read_file_content(package_json_file_path)
        package_json_content_object = json.loads(package_json_content)

        # 获取dependencies节点内容
        dependencies_json_object = package_json_content_object.get("dependencies")

        # 去除dependencies节点
        package_json_content_object.pop("dependencies")

        # 合并dependencies节点内容
        logger.debug(" dependencies_json_object:%s npm_dependencies：%s" % (
            dependencies_json_object, self.npm_dependencies))
        dependencies = dependencies_json_object.copy()
        dependencies.update(self.npm_dependencies)

        # 重新添加dependencies节点
        package_json_content_object["dependencies"] = dependencies

        # 新增pages节点
        pages_json_array = []
        pages_json_array.append(self.page.__dict__)
        package_json_content_object["pages"] = pages_json_array

        # 向package.json文件写入数据
        logger.info(" 向package.json文件写入数据 路径：%s" % package_json_file_path)
        write_content_to_file(package_json_file_path, json.dumps(package_json_content_object, ensure_ascii=False))

    def create_page_file(self, workspace_path, plugin_id_dir, module_str):
        page_file_path = PathConstant.MOUDLE_PAGES_JSON_FILE.replace("{PLUGIN_ID_DIR}", plugin_id_dir).replace(
            "{TAG_MOUDLE}", module_str)
        pages_json_file_path = os.path.join(workspace_path, page_file_path)

        logger.info(" 正在写入文件：%s" % pages_json_file_path)
        write_content_to_file(pages_json_file_path, json.dumps(self.page.__dict__))

    def zip_page_project(self, workspace_path, plugin_id_dir, module_str):
        input_file_name = os.path.join(workspace_path, PathConstant.REACT_WIDGET, plugin_id_dir, module_str)
        zip_file_name = input_file_name + ".zip"
        logger.debug(" page：%s下的文件压缩成zip包: %s" % (module_str, zip_file_name))
        # 整合该page下的所有文件路径
        need_zip_file_list = []
        for file_name in os.listdir(input_file_name):
            absolute_path = os.path.join(input_file_name, file_name)
            need_zip_file_list.append(absolute_path)

        zip_multi_file(zip_file_name, need_zip_file_list, False)

    def execute_npm_build(self, variables_json, plugin_id_dir, module_str):
        module_path = os.path.join(os.getcwd(), "target/react_widget", plugin_id_dir, module_str)

        install_command = ["npm", "install"]
        logger.info(" 命令： %s. 执行: npm install" % install_command)
        execute_command(install_command, chdir=module_path)

        build_tool = variables_json["build_tool"]
        if build_tool:
            nd_react_install_command = ["npm", "install", "@sdp.nd/nd-react"]
            logger.info(" 命令： %s. 执行: npm install @sdp.nd/nd-react" % nd_react_install_command)
            execute_command(nd_react_install_command, chdir=module_path)

            out_put = "../i18n/" + module_str
            node_lang_comman = ["node", "node_modules/@sdp.nd/nd-react", "lang", "-t", "widget", "-o", out_put, "-b",
                                "true"]
            logger.info(" 命令： %s. 执行：node node_modules/@sdp.nd/nd-react lang -t widget -o %s -b true" % (
                node_lang_comman, out_put))
            execute_command(node_lang_comman, chdir=module_path)
        else:
            android_lang_command = ["node", "node_modules/@sdp.nd/nd-react", "lang", "-t", "widget", "-p", "android",
                                    "-b", "true"]
            logger.info(" 命令： %s. 执行：node node_modules/@sdp.nd/nd-react lang -t widget -p android -b true" %
                  android_lang_command)
            execute_command(android_lang_command, chdir=module_path)

            ios_lang_command = ["node", "node_modules/@sdp.nd/nd-react", "lang", "-t", "widget", "-p", "iOS",
                                "-b", "true"]
            logger.info(" 命令： %s. 执行：node node_modules/@sdp.nd/nd-react lang -t widget -p iOS -b true" %
                  ios_lang_command)
            execute_command(ios_lang_command, chdir=module_path)

        skin_command = ["node", "node_modules/@sdp.nd/nd-react", "skin"]
        logger.info(" 命令： %s. 执行：node node_modules/@sdp.nd/nd-react skin " % skin_command)
        execute_command(skin_command, chdir=module_path)
