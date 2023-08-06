#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
动态tab构建-构建流程
"""

__author__ = '370418'

from apf_ci.util.file_utils import *
from apf_ci.util.upload_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.execute_command_utils import *
from apf_ci.app_init.utils.variable_utils import Variable
from apf_ci.util.content_service_config import ContentServiceConfig


def main():
    workspace_path = os.getcwd()
    target_path = os.path.join(workspace_path, 'target')
    variables_utils = Variable(target_path)
    variables_json = variables_utils.read_variable_json()

    update_page_json(workspace_path, variables_json)
    copy_images_file(workspace_path,variables_json)
    zip_file_path = zip_tab(workspace_path)
    storage_cs_zip_path = upload_to_cs(variables_json, zip_file_path)
    upload_to_portal(variables_json, storage_cs_zip_path)

    variables_json['tab_url'] = storage_cs_zip_path
    variable = Variable(target_path)
    variable.write_variable_json(variables_json)


def update_page_json(workspace_path, variables_json):
    logger.info('开始更新page.json文件')
    target_path = variables_json['target_path']
    app_factory_path = os.path.join(workspace_path, 'app', 'assets', 'app_factory')
    target_app_factory_path = os.path.join(target_path, 'app_factory')
    languages_array = variables_json['languages']
    for language in languages_array:
        # 读取pages.json
        language_path = os.path.join(app_factory_path, language)
        pages_path = os.path.join(language_path, 'pages', 'pages.json')
        pages_data = read_file_content(pages_path)
        pages_json = json.loads(pages_data)

        # 读取最初的app_pages.json,获取tab中图片的url地址，合并到page.json
        target_pages_path = os.path.join(target_app_factory_path, language, 'pages', 'app_pages.json')
        app_pages_data = read_file_content(target_pages_path)
        app_pages_json = json.loads(app_pages_data)
        pages_json_new = {}
        pages_path_new = pages_path.replace('app' + os.sep + 'assets', 'tab')
        logger.debug('tab pages.json路径：%s' % pages_path_new)
        if pages_json:
            for key in pages_json:
                pages_item = pages_json[key]
                if 'cmp://com.nd.smartcan.appfactory.main_component/main?pageid' in pages_item["template"] \
                    or 'cmp://com.nd.smartcan.appfactory.main_component/main_fragment?pageid' in pages_item["template"]:
                    pages_item_new = {}
                    for item_key in pages_item:
                        if not item_key.startswith('_'):
                            pages_item_new[item_key] = pages_item[item_key]
                    pages_json_new[key] = pages_item_new

            write_content_to_file(pages_path_new, json.dumps(pages_json_new, ensure_ascii=False))
    logger.info('结束更新page.json文件')


def copy_images_file(workspace_path, variables_json):
    build_app_type = variables_json["build_app_type"]
    if build_app_type.lower() == 'android':
        copy_images_file_android(workspace_path, variables_json)
    elif build_app_type.lower() == 'ios':
        copy_images_file_ios(workspace_path, variables_json)


def copy_images_file_android(workspace_path, variables_json):
    logger.info('开始拷贝 tab 和tab-fragment 用到的图片资源')
    res_path = os.path.join(workspace_path, 'app', 'res')
    res_dir_list = os.listdir(res_path)
    for res_dir in res_dir_list:
        # 只要drawable-xxx目录的tab相关图片，还有 raw目录下json类型的图片资源
        if res_dir.startswith('drawable-') or res_dir == "raw":
            # 找到 drawable-xxx的图片目录
            drawable_path = os.path.join(res_path, res_dir)
            if not os.path.isdir(drawable_path):
                continue
            drawable_dir_list = os.listdir(drawable_path)
            for drawable_file in drawable_dir_list:
                if drawable_file.startswith('main_pageid') or drawable_file.startswith('main_fragment_pageid'):
                # 找到 tab 和tab-fragment 用到的图片资源
                    drawable_file_path = os.path.join(drawable_path, drawable_file)
                    if not os.path.isfile(drawable_file_path):
                        continue
                    drawable_file_path_new = drawable_file_path.replace('app' + os.sep + 'res',
                                                                        'tab' + os.sep + 'images')
                    # 复制到tab 目录下,.9.png的另外处理下
                    if drawable_file.endswith('.9.png'):
                        convert_9_png(variables_json, drawable_file_path, drawable_file_path_new)
                    else:
                        copy_file(drawable_file_path, drawable_file_path_new)

    logger.info('结束拷贝 tab 和tab-fragment 用到的图片资源')


def convert_9_png(variables_json, source_path, des_path):
    fpath, fname = os.path.split(des_path)
    if not os.path.exists(fpath):
            os.makedirs(fpath)
    sdk_path = variables_json["sdk_path"]
    aapt_path = '%s/build-tools/28.0.3/aapt' % sdk_path
    try:
        execute_command([aapt_path, 's', '-i', source_path, '-o', des_path, ])
    except Exception:
        error_message = ".9.png处理异常 %s" % source_path
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_message)


def copy_images_file_ios(workspace_path, variables_json):
    logger.info('开始拷贝 tab 和tab-fragment 用到的图片资源')
    #build_app_name = variables_json["build_app_name"]
    build_app_name = variables_json["replace_string"]
    res_path = os.path.join(workspace_path, build_app_name, 'Resources', 'skin',
                            'com.nd.smartcan.appfactory.main_component_skin.bundle')
    drawable_dir_list = os.listdir(res_path)
    for drawable_file in drawable_dir_list:
        if drawable_file.startswith('main_pageid') or drawable_file.startswith('main_fragment_pageid'):
        # 找到 tab 和tab-fragment 用到的图片资源
            drawable_file_path = os.path.join(res_path, drawable_file)
            if not os.path.isfile(drawable_file_path):
                continue
            drawable_file_path_new = os.path.join(workspace_path, 'tab', 'images', drawable_file)
            # 复制到tab 目录下
            copy_file(drawable_file_path, drawable_file_path_new)
    logger.info('结束拷贝 tab 和tab-fragment 用到的图片资源')


def zip_tab(workspace_path):
    '''
    压缩到tab.zip
    '''
    tab_path = os.path.join(workspace_path, 'tab')
    zip_file_path = os.path.join(workspace_path, 'tab.zip')
    #need_zip_file_path = os.path.join(tab_path, 'app', 'assets')
    zipDir(tab_path, zip_file_path)
    return zip_file_path


def upload_to_cs(variables_json, zip_file_path):
    # 配置存储内容服务
    storage_cs = ContentServiceConfig()
    storage_cs.host = variables_json["h5_grain_storage_cs_host"]
    storage_cs.server_name = variables_json["h5_grain_storage_cs_server_name"]
    storage_cs.session_id = variables_json["h5_grain_storage_cs_session_id"]
    storage_cs.user_id = variables_json["h5_grain_storage_cs_user_id"]
    storage_cs.access_key = variables_json["h5_grain_storage_cs_access_key"]
    storage_cs.secret_key = variables_json["h5_grain_storage_cs_secret_key"]
    build_package = variables_json["build_package"]

    # 上传到cs,并在生产时候，替换成cdn地址
    storage_cs_path = "/" + build_package + "/tab/"
    storage_cs_host_path = storage_cs.host + "/static/" + storage_cs.server_name + storage_cs_path
    cs_zip_file_name = "" + str(int(time.time() * 1000)) + ".zip"
    upload_file_to_cs(zip_file_path, storage_cs_path, cs_zip_file_name, storage_cs)
    storage_cs_zip_path = storage_cs_host_path + cs_zip_file_name
    storage_cs_zip_path = storage_cs_zip_path.replace("http://cs.101.com", "https://gcdncs.101.com")
    logger.debug("动态tab上传cs成功：" + storage_cs_zip_path)
    return storage_cs_zip_path


def upload_to_portal(variables_json, storage_cs_zip_path):
    # 提测到发布库
    mobile_grey = variables_json['mobile_grey']
    factory_id = variables_json["factoryId"]
    build_package = variables_json["build_package"]
    build_app_type = variables_json["build_app_type"]
    envtarget = variables_json['envtarget']
    version_code = variables_json['tab_version_code']
    version_name = variables_json['tab_version_name']
    version_description = variables_json['tab_version_desc']
    package_type = 0
    if build_app_type.lower() == 'ios':
        package_type = 1

    tab_url = mobile_grey + 'v1.0/tabs'
    body = {
        "identifier": factory_id,
        "package_type": package_type,
        "package_name": build_package,
        "version_code": version_code,
        "version_name": version_name,
        "version_description": version_description,
        "download_url": storage_cs_zip_path,
        "env": envtarget
    }
    resp = post_for_array(tab_url, body)
    logger.debug(resp)


if __name__ == '__main__':
    variables_json = {}
    variables_json['sdk_path'] = 'D:/software/Java\Android/sdk_studio'
    source = 'F:/workplace/python/jenkins-plugin-python/anonymous_chat_icon_popup_arrow.9.png'
    des = 'F:/workplace/python/jenkins-plugin-python/cc.9.png'
    convert_9_png(variables_json, source, des)

    #variables_json = {}
    #variables_json['mobile_grey'] = 'https://portal-android-grey.beta.101.com/'
    #variables_json['factoryId'] = 'cadcd82c-4ff8-4376-936f-50f290730e3c'
    #variables_json['build_package'] = 'com.nd.app.factory.testforsign2'
    #variables_json['build_app_type'] = 'Android'
    #variables_json['envtarget'] = 'preproduction'
    #variables_json['tab_version_code'] = '0.0.2'
    #variables_json['tab_version_name'] = 'yushengchang'
    #variables_json['tab_version_desc'] = '预生产'
    #storage_cs_zip_path = 'http://betacs.101.com/v0.1/static/preproduction_content_native_app/com.nd.app.factory.testforsign2/tab/1588088159323.zip'
    #upload_to_portal(variables_json, storage_cs_zip_path)