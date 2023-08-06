#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app对比工具
"""

__author__ = '370418'

from apf_ci.app_compare.build.app_compare_utils import *
from apf_ci.app_compare.build.dependency_utils import get_mobile_dependencies
import plistlib
import re


def main(variable_dict, build_config_json):
    package_old = variable_dict['packageOld']
    package_new = variable_dict['packageNew']
    target_path = variable_dict['targetPath']

    data = {}
    package_old.split(".")
    package_old_path = os.path.join(target_path, "package_old.ipa")
    package_new_path = os.path.join(target_path, "package_new.ipa")
    download_pac(package_old, package_new, package_old_path, package_new_path)

    package_old_dir_path = os.path.join(target_path, "package_old")
    package_new_dir_path = os.path.join(target_path, "package_new")
    unzip_pac_all(variable_dict, package_old_path, package_new_path, package_old_dir_path, package_new_dir_path)
    package_old_work_path = os.path.join(package_old_dir_path, get_ios_work_dir(package_old_path))
    package_new_work_path = os.path.join(package_new_dir_path, get_ios_work_dir(package_new_path))

    getpacBaseInfo(data, package_old, package_old_path, package_old_work_path, package_new, package_new_path,
                   package_new_work_path)

    getAppInfo(data, package_old_work_path, package_new_work_path)

    getDependencyInfo(build_config_json, data, package_old_work_path, package_new_work_path)

    getBizDependencyInfo(build_config_json, data)

    getBuildInfo(data, package_old_work_path, package_new_work_path)

    return data


def get_ios_work_dir(package_path):
    zipfiles = zipfile.ZipFile(package_path) #拼接成一个路径
    pattern = re.compile(r'Payload/[^/]*.app/')
    for file in zipfiles.namelist():
        m = pattern.match(file)
        if m is not None:
            zipfiles.close()
            return m.group().replace('/', os.path.sep)


def getpacBaseInfo(data, package_old, package_old_path, package_old_work_path, package_new, package_new_path,
                   package_new_work_path):
    summary = {}
    getApBaseItemInfo(summary, package_old, package_old_path, package_old_work_path, "old")
    getApBaseItemInfo(summary, package_new, package_new_path, package_new_work_path, "new")
    summary["package_old"] = package_old
    summary["package_new"] = package_new
    summary["createTime"] = time.time()
    data["summary"] = summary


def getApBaseItemInfo(summary, package_url, package_path, package_work_path, ver):
    item = {}
    item["platform"] = "Ios"
    try:
        pac_size_b = os.path.getsize(package_path)
        pac_size_kb = '%.1f' % float(pac_size_b / 1000)
        item["size"] = pac_size_kb

        plist_path = os.path.join(package_work_path, 'Info.plist')
        plist_root = plistlib.readPlist(plist_path)

        item["packageName"] = plist_root['CFBundleIdentifier']
        item["version"] = plist_root['CFBundleVersion']
        item["versionName"] = plist_root['DTPlatformVersion']
        item["name"] = plist_root['CFBundleName']

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
    tree_path = os.path.join(package_path, "ci", "components.json")
    tree_file = read_file_content(tree_path)
    tree_json = json.loads(tree_file)
    component_version = tree_json['component_version']
    for item in component_version:
        dependency_tree.append(item + ":" + component_version[item])

    dependency_info["tree"][ver] = dependency_tree
    dependency_info["trees"][ver] = get_mobile_dependencies(build_config_json, data, dependency_tree, ver)