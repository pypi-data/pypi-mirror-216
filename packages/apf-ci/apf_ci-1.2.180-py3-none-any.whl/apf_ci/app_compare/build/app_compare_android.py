#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app对比工具
"""

__author__ = '370418'

import re
from apf_ci.app_compare.build.app_compare_utils import *
from apf_ci.app_compare.build.dependency_utils import get_mobile_dependencies

aapt_path = 'aapt'
#aapt_path = 'D://software//Java//Android//sdk_studio//build-tools//27.0.3//aapt.exe'


def main(variable_dict, build_config_json):
    package_old = variable_dict['packageOld']
    package_new = variable_dict['packageNew']
    target_path = variable_dict['targetPath']

    data = {}
    package_old_path = os.path.join(target_path, "package_old.apk")
    package_new_path = os.path.join(target_path, "package_new.apk")
    download_pac(package_old, package_new, package_old_path, package_new_path)

    package_old_dir_path = os.path.join(target_path, "package_old")
    package_new_dir_path = os.path.join(target_path, "package_new")

    package_old_work_path = os.path.join(package_old_dir_path, "assets")
    package_new_work_path = os.path.join(package_new_dir_path, "assets")

    unzip_pac_all(variable_dict, package_old_path, package_new_path, package_old_dir_path, package_new_dir_path)
    getpacBaseInfo(data, package_old, package_old_path, package_new, package_new_path)

    getAppInfo(data, package_old_work_path, package_new_work_path)

    getDependencyInfo(build_config_json, data, package_old_work_path, package_new_work_path)

    getBizDependencyInfo(build_config_json, data)

    getBuildInfo(data, package_old_work_path, package_new_work_path)
    return data


def getpacBaseInfo(data, package_old, package_old_path, package_new, package_new_path):
    summary = {}
    getApBaseItemInfo(summary, package_old, package_old_path, "old")
    getApBaseItemInfo(summary, package_new, package_new_path, "new")
    summary["package_old"] = package_old
    summary["package_new"] = package_new
    summary["createTime"] = time.time()
    data["summary"] = summary


def getApBaseItemInfo(summary, package_url, package_path, ver):
    item = {}
    item["platform"] = "Android"
    try:
        output = os.popen("%s d badging %s" % (aapt_path, package_path)).read()
        # 返回 KB 为单位的安装包大小
        pac_size_b = os.path.getsize(package_path)
        pac_size_kb = '%.1f' % float(pac_size_b / 1000)
        item["size"] = pac_size_kb
        # 支持应用名带空格
        app_name = re.compile("application-label:'([\S\t ]+)'").search(output).group(1)
        item["name"] = app_name

        match = re.compile(
            "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output)
        package_name = match.group(1)
        version_code = match.group(2)
        version_name = match.group(3)
        item["packageName"] = package_name
        item["version"] = version_code
        item["versionName"] = version_name

        with open(package_path, 'rb') as f:
            file_content_byte = f.read()
        pac_md5 = get_md5(file_content_byte)
        item["md5"] = pac_md5
        summary[ver] = item
    except Exception:
        raise Exception("从安装包中获取包信息失败：" + package_url)


def getDependencyInfo(build_config_json, data, package_old_dir_path, package_new_dir_path):
    dependency_info = {}
    getDependencyItemInfo(build_config_json, data, dependency_info, package_old_dir_path, "old")
    getDependencyItemInfo(build_config_json, data, dependency_info, package_new_dir_path, "new")
    data["dependencyTree"] = dependency_info


def getDependencyItemInfo(build_config_json, data, dependency_info, package_path, ver):
    if "tree" not in dependency_info:
        dependency_info["tree"] = {}
    if "trees" not in dependency_info:
        dependency_info["trees"] = {}
    dependency_tree = []
    tree_path = os.path.join(package_path, "Tree.txt")
    tree_file = read_file_content(tree_path)
    dep_end = tree_file.rfind("\---")
    tree_file_end = tree_file[dep_end:]
    tree_file_split = tree_file_end.split("\n")
    for item in tree_file_split:
        if item.startswith("jar") or item.startswith("aar"):
            item_split = item.split("\t")
            if len(item_split) == 2:
                dependency_tree.append(item_split[1])
    dependency_info["tree"][ver] = dependency_tree
    dependency_info["trees"][ver] = get_mobile_dependencies(build_config_json, data, dependency_tree,ver)
