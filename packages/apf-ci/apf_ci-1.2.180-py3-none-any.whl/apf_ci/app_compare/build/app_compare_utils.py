#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app对比工具
"""

__author__ = '370418'

from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.app_compare.build.dependency_utils import get_app_dependencies
from apf_ci.util.content_service_config import ContentServiceConfig
import re


def download_pac(package_old, package_new, package_old_path, package_new_path):
    download_cs_file(package_old, package_old_path, 3)
    download_cs_file(package_new, package_new_path, 3)


def unzip_pac_all(variable_dict, package_old_path, package_new_path, package_old_dir_path, package_new_dir_path):
    unzip_pac(package_old_path, package_old_dir_path)
    unzip_pac(package_new_path, package_new_dir_path)


def unzip_pac(package_path, package_dir_path):
    zipfiles = zipfile.ZipFile(package_path) #拼接成一个路径
    for file in zipfiles.namelist():
        zipfiles.extract(file, package_dir_path)
    zipfiles.close()


def getAppInfo(data, package_old_dir_path, package_new_dir_path):
    app_base_info = {}
    getAppItemInfo(app_base_info, package_old_dir_path, package_new_dir_path, "app.json")
    #getAppItemInfo(app_base_info, package_old_dir_path, package_new_dir_path, "config.json")
    data["appBaseInfo"] = app_base_info


def getAppItemInfo(app_base_info, package_old_dir_path, package_new_dir_path, file_name):
    app_json = {}
    app_json_old_path = os.path.join(package_old_dir_path, "app_factory", "app", file_name)
    app_json_old_file = read_file_content(app_json_old_path)
    app_json_old = json.loads(app_json_old_file)
    app_json_new_path = os.path.join(package_new_dir_path, "app_factory", "app", file_name)
    app_json_new_file = read_file_content(app_json_new_path)
    app_json_new = json.loads(app_json_new_file)
    app_json["old"] = app_json_old
    app_json["new"] = app_json_new
    app_base_info[file_name] = app_json


def getBuildInfo(data, package_old_dir_path, package_new_dir_path):
    build_info = {}
    getBuildItemInfo(build_info, package_old_dir_path, data, "old")
    getBuildItemInfo(build_info, package_new_dir_path, data, "new")
    data["build"] = build_info


def getBuildItemInfo(build_info, package_path, data, ver):
    app_json = data["appBaseInfo"]["app.json"][ver]
    language_enable = app_json["language_enable"]
    app_factory_path = os.path.join(package_path, "app_factory")

    biz_dependency = data['biz_dependency'][ver]
    biz_dependency_obj = {}
    for biz in biz_dependency:
        biz_dependency_obj[biz['biz_namespace']+":"+biz['biz_name']] = biz

    for language in language_enable:
        build_json_path = os.path.join(app_factory_path, language, "components", "build.json")
        build_json_file = read_file_content(build_json_path)
        build_json = json.loads(build_json_file)
        build_json_new = []
        if biz_dependency != []:
            # 给build.json补充组件中文名，也有可能还是英文
            for item in build_json:
                component = item['component']
                namespace = component['namespace']+":"+component['name']
                if namespace in biz_dependency_obj:
                    item['biz_label'] = biz_dependency_obj[namespace]['biz_label']
                    #print(item['biz_label'])
                    build_json_new.append(item)
        else:
            build_json_new = build_json

        if language not in build_info:
            build_info[language] = {}
            build_info[language]["build.json"] = {}
        build_info[language]["build.json"][ver] = build_json_new



def getBizDependencyInfo(build_config_json, data):
    biz_dependency_info = {}
    summary = data['summary']
    getBizDependencyItemInfo(build_config_json, summary, biz_dependency_info, 'old')
    getBizDependencyItemInfo(build_config_json, summary, biz_dependency_info, 'new')
    data["biz_dependency"] = biz_dependency_info


def getBizDependencyItemInfo(build_config_json, summary, biz_dependency_info, ver):
    package_info = summary[ver]
    app_dependencies = get_app_dependencies(build_config_json, package_info['packageName'], package_info['version'],
                                            package_info['platform'])
    biz_dependency_info[ver] = app_dependencies


def save_and_upload(target_path, build_config_json, app_compare_id, upload_file_name, file_json):
    pac_file_path = os.path.join(target_path, upload_file_name)
    write_content_to_file(pac_file_path, json.dumps(file_json))
    data_url = upload_to_cs(pac_file_path, build_config_json, app_compare_id)
    return data_url


def upload_to_cs(data_path, build_config_json, app_compare_id):
    # 配置存储内容服务
    storage_cs = ContentServiceConfig()
    cs_server = build_config_json["cs_server"]

    storage_cs.host = cs_server["cs_host"]
    storage_cs.server_name = cs_server["cs_server_name"]
    storage_cs.session_id = cs_server["cs_session_id"]
    storage_cs.user_id = cs_server["cs_user_id"]
    storage_cs.secret_key = cs_server["secret_key"]
    storage_cs.access_key = cs_server["access_key"]

    # 上传到cs,并在生产时候，替换成cdn地址
    storage_cs_path_end = "/compare/" + app_compare_id + "/"
    storage_cs_host_path = storage_cs.host + "/static/" + storage_cs.server_name + storage_cs_path_end
    cs_file_name = "" + str(int(time.time() * 1000)) + ".json"
    upload_file_to_cs(data_path, storage_cs_path_end, cs_file_name, storage_cs)
    storage_cs_path = storage_cs_host_path + cs_file_name
    storage_cs_path = storage_cs_path.replace('http://', 'https://').replace('//cs.101.com',
                                                                          '//gcdncs.101.com')

    return storage_cs_path


def get_download_url(build_config_json, data_url):
    readonly_portal = build_config_json['service_host']["appfactory-readonly-portal"]["default"]
    match = re.search("compare/(\S+)/(\S+).json", data_url)
    if match:
        app_compare_id = match.group(1)
        upload_id = match.group(2)
        report_url = readonly_portal + '#/appDiff/' + app_compare_id + '/' + upload_id
        return report_url


