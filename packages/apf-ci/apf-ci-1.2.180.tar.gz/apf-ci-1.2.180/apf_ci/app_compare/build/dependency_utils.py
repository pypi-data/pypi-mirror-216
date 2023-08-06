#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.util.http_utils import get_data
import re


def get_app_dependencies(build_config_json, packagename, version, platform):
    '''
     获取产品的业务组件依赖数据
    '''
    dep_host = build_config_json['service_host']['app-factory-dependency-service']['default']
    factory_dependency_check = build_config_json['service_host']['factory_dependency_check']['default']
    app_dep_url = "%s/v0.2/build_relation/search?appVersionCode=%s&appVersionOs=%s" % (dep_host, version, platform)
    factory_dependency_check_url = "%s/v0.1/entity_size_report/product_business_dependencies?version=%s&platform=%s&name=%s" % (
        factory_dependency_check, version, platform.lower(), packagename)
    if 'android' == platform.lower():
        app_dep_url = app_dep_url + ('&packageNameAndroid=%s' % packagename)
    else:
        app_dep_url = app_dep_url + ('&packageNameIos=%s' % packagename)
    fac_app_deps = []
    deps = get_data(app_dep_url)
    dep_sizes = get_biz_dependencies_size(factory_dependency_check_url)
    for dep in deps:
        biz_name = dep['biz_name']
        if biz_name == None:
            continue
        biz_label = dep['biz_label']
        biz_namespace = dep['biz_namespace']
        biz_version = dep['biz_version']
        biz_dep = get_biz_dependencies(dep_host, biz_name, biz_namespace, biz_version, platform)
        biz = {}
        biz['biz_label'] = biz_label
        biz['biz_name'] = biz_name
        biz['biz_namespace'] = biz_namespace
        biz['biz_version'] = biz_version
        biz['dependencies'] = biz_dep
        biz_key = biz['biz_namespace'] + "." + biz['biz_name']
        get_biz_size(dep_sizes, biz, biz_key)
        fac_app_deps.append(biz)
    return fac_app_deps


def get_mobile_dependencies(build_config_json, data, dependency_tree, ver):
    '''
      获取移动组件的依赖数据
    '''
    dependency_trees =[]
    app_info = data['summary'][ver]
    factory_dependency_check = build_config_json['service_host']['factory_dependency_check']['default']
    factory_dependency_check_url = "%s/v0.1/entity_size_report/product_mobile_dependencies?version=%s&platform=%s&name=%s" % (
        factory_dependency_check, app_info['version'], app_info['platform'].lower(), app_info['packageName'])
    dep_sizes = get_biz_dependencies_size(factory_dependency_check_url)
    for dependency in dependency_tree:
        dependency_item = {}
        dependency_arr = dependency.split(':')
        if app_info['platform'].lower() == 'android':
            dependency_item['name'] = dependency_arr[0] + ":" + dependency_arr[1]
            dependency_item['version'] = dependency_arr[2]
        else:
            dependency_item['name'] = dependency_arr[0]
            dependency_item['version'] = dependency_arr[1]
        get_biz_size(dep_sizes, dependency_item, dependency_item['name'])
        dependency_trees.append(dependency_item)
    return dependency_trees

def get_biz_size(dep_sizes, biz, biz_key):
    '''
     将依赖数据中大小相关数据，保存到依赖中
    '''
    if biz_key in dep_sizes:
        dep_item = dep_sizes[biz_key]
        if 'zip_total_size' in dep_item:
            biz['zip_total_size'] = dep_item['zip_total_size']
        if 'total_size' in dep_item:
            biz['total_size'] = dep_item['total_size']
        if 'dependencies_zip_total_size' in dep_item:
            biz['dependencies_zip_total_size'] = dep_item['dependencies_zip_total_size']
        if 'dependencies_total_size' in dep_item:
            biz['dependencies_total_size'] = dep_item['dependencies_total_size']
        if 'version' in dep_item:
            biz['dep_version'] = dep_item['version']


def get_biz_dependencies_size(factory_dependency_check_url):
    '''
     获取依赖数据，并根据组件名，生成map
    '''
    dependencies_map = {}

    dep_sizes = get_data(factory_dependency_check_url)
    if dep_sizes and len(dep_sizes) > 0:
        dep_size = dep_sizes[0]
        if 'dependencies' in dep_size:
            dependencies = dep_size['dependencies']

            for dep_item in dependencies:
                dependencies_map[dep_item['name']] = dep_item
    return dependencies_map


def get_biz_dependencies(dep_host, biz_name, biz_namespace, biz_version, platform):
    biz_dep_url = "%s/v0.2/build_relation/search_aar?bizName=%s&bizNamespace=%s&bizVersion=%s" % (
        dep_host, biz_name, biz_namespace, biz_version)
    deps = get_data(biz_dep_url)
    fac_deps = []

    for dep in deps:
        # 只返回对应平台的移动组件依赖
        if dep['type'].lower() == platform.lower():
            fac_deps.append(dep)

    return fac_deps


if __name__ == '__main__':
    data_url = 'https://cs.101.com/v0.1/static/test_package_repository/compare/5f168de3e812d190623e4d55/1595313697831.json'
    match = re.compile("compare/'(\S+)'/'(\d+)'\.json").match(data_url)
    package_name = match.group(1)
    version_code = match.group(2)

    build_config_json = {}
    dep_host = {}
    dep_host['default'] = 'https://app-factory-dependency-service.sdp.101.com/'
    build_config_json['app-factory-dependency-service'] = dep_host

    packagename = 'com.nd.app.factory.testforsign2'
    version = '3446785'
    platform = 'android'

    app_dependencies = get_app_dependencies(build_config_json, packagename, version, platform)
    platform = 'android'

