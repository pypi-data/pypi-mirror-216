#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import os
import sys
import urllib.request
import zipfile
import imghdr
import shutil
import time
import requests
import traceback
from urllib.parse import quote
import platform
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool
from apf_ci.util.md5_utils import *
from apf_ci.util.log_utils import logger
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum


def is_image(filename):
    img_type = imghdr.what(filename)
    if img_type == 'gif' or img_type == 'jpeg' or img_type == 'png':
        return True
    else:
        return False


def read_file_content(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_dir(workspace_path):
    for root, dirs, files in os.walk(workspace_path, topdown=False):
        for name in files:
            #if 'jenkins_build_debug2.log' in name:
            #    print(name)
            #    continue
            try:
                os.remove(os.path.join(root, name))
            except Exception:
                continue
        for name in dirs:
            del_dir = os.path.join(root, name)
            try:
                os.rmdir(del_dir)
            except NotADirectoryError:
                os.remove(del_dir)


def create_parent_path(file_path):
    # 获取文件的父路径
    # file_dir = os.path.abspath(os.path.dirname(file_path) + os.path.sep + '.')
    file_dir = os.path.dirname(file_path)

    # 判断文件路径是否存在，不存在则创建
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)


def write_content_to_file(file_path, content):
    create_parent_path(file_path)

    with open(file_path, "w", encoding='utf-8') as f:
        f.write(content)


def read_cs_content(cs_url):
    logger.debug("read_cs_content url %s" % cs_url)
    response = urllib.request.urlopen(cs_url)
    return response.read()


def is_file_invalid(file_path):
    if file_path is None:
        return True
    if len(file_path) <= 0:
        return True
    if not os.path.exists(file_path):
        return True
    if not os.path.isfile(file_path):
        return True
    return False


def download_cs_file(cs_url, file_path, maxRetry):
    logger.debug('下载【%s】到【%s】' % (cs_url, file_path))
    create_parent_path(file_path)
    for i in range(maxRetry):
        try:
            # 图片资源：根据cs_url的md5值判断是否有缓存 其他资源无视缓存
            if check_use_cache(cs_url):
                file_download_cache(cs_url, file_path, "picture")
            else:
                r = requests.get(cs_url, timeout=60)
                if r.status_code != 200:
                    if i == maxRetry - 1:
                        raise Exception("下载失败！")
                    continue
                with open(file_path, "wb") as code:
                    code.write(r.content)

                    #with open(file_path, "wb") as f:
                    #    # 附加不转换字符参数，对中文进行处理
                    #response = urllib.request.urlopen(quote(cs_url, safe='/:?='))
                    #f.write(response.read())
            break
        except Exception as e:
            if maxRetry - i == 1:
                traceback.print_exc()
                raise e
            time.sleep(0.5)


def unzip(unzip_file_path, file_path):
    logger.debug('解压【%s】到【%s】' % (unzip_file_path, file_path))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_zip = zipfile.ZipFile(unzip_file_path, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, file_path)

    file_zip.close()


def unzip_language(unzip_file_path, file_path, language_name):
    """
    只解压i18n目录结构下的文件
    :param dir_path:
    :param source_file_path:
    :param language_name:
    :return:
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_zip = zipfile.ZipFile(unzip_file_path, 'r')
    for file in file_zip.namelist():
        abs_file = file_path + file
        if file.startswith("i18n/"):
            if os.path.isdir(abs_file):
                # 不解压文件夹
                continue
            if file.endswith("/default.json"):
                file_zip.extract(file, file_path)
                os.rename(abs_file, abs_file.replace("/default.json", "/" + language_name + ".json"))
    file_zip.close()


def zip_filter_folder_file(zip_file_name, file_list_path, is_filter_folder, filter_list):
    zip_out = zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED)
    _zip_filter_file(zip_out, file_list_path, "", is_filter_folder, filter_list)
    zip_out.close()


def _zip_filter_file(zip_out, file_path, base_path, is_filter_folder, filter_list):
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        base_path = "" if len(base_path) == 0 else base_path + "/"
        for file_name in files:
            next_file_path = os.path.join(file_path, file_name)
            if os.path.isfile(next_file_path):
                base_temp = base_path + file_name
            else:
                base_temp = base_path + "/" + os.path.basename(next_file_path)
            if is_filter_folder and filter_list != [] and file_name in filter_list:
                continue
            _zip_filter_file(zip_out, next_file_path, base_temp, is_filter_folder, filter_list)
    else:
        zip_out.write(file_path, base_path)


def zip_multi_file(zip_file_name, file_list, is_filter_first_folder):
    """
    多文件压缩。
    :param zip_file_name: 要打包的zip文件名
    :param file_list: 要打包的文件列表
    :param is_filter_first_folder: 是否忽略一级目录（最外层的目录）。忽略则不会压缩进zip
    :return:
    """
    flag = False
    out = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    for file_path in file_list:
        base_path = os.path.basename(file_path)
        if is_filter_first_folder and os.path.isdir(file_path):
            base_path = ""
        _zip_file(out, file_path, base_path)
    out.close()


def _zip_file(out, file_path, base_path):
    if os.path.isdir(file_path):
        base_path = "" if len(base_path) == 0 else base_path + "/"
        for file in os.listdir(file_path):
            sub_file = os.path.join(file_path, file)
            _zip_file(out, sub_file, base_path + file)
    else:
        out.write(file_path, base_path)


def copy_file(src_file_path, dest_file_path):
    if not os.path.isfile(src_file_path):
        logger.debug('%s not exist!' % src_file_path)
    else:
        fpath, fname = os.path.split(dest_file_path)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(src_file_path, dest_file_path)
        logger.debug('copy %s -> %s' % (src_file_path, dest_file_path))


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def copy_directory(source_dir, target_dir):
    # 复制一整个文件目录结构以及文件
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if not os.path.isdir(source_dir):
        logger.debug('[WARN]copy_directory：source_dir参数必须为 目录类型, 路径：%s' % source_dir)
    else:
        # 复制层级结构
        for file in os.listdir(source_dir):
            source_f = os.path.join(source_dir, file)
            target_f = os.path.join(target_dir, file)
            if os.path.isfile(source_f):
                shutil.copy(source_f, target_f)
                # logger.debug("[DEBUG] copy_directory：拷贝文件: %s 到目录下： %s" % (file, target_f))
            if os.path.isdir(source_f):
                if not os.path.exists(target_f):
                    os.mkdir(target_f)
                    # logger.debug("[DEBUG] copy_directory：复制的目标目录不存在，创建目录： %s" % target_f)
                copy_directory(source_f, target_f)


def copy_file_first_level(src, dest):
    """
    只拷贝一级目录下的文件，文件夹忽略
    :param src:
    :param dest:
    :return:
    """
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        file_list = os.listdir(src)
        for file in file_list:
            src_file = src + "/" + file
            if not os.path.isdir(src_file):
                dest_file = dest + "/" + file
                shutil.copy(src_file, dest_file)
    else:
        shutil.copy(src, dest)


def copy_folder_first_level(src, dest):
    """
    只拷贝一级目录下 文件夹中的所有文件夹，文件忽略
    :param src:
    :param dest:
    :return:
    """
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        file_list = os.listdir(src)
        for file in file_list:
            src_file = src + "/" + file
            if os.path.isdir(src_file):
                dest_file = dest + "/" + file
                copy_directory(src_file, dest_file)
    else:
        shutil.copy(src, dest)


def copy_folder_except_folder(src, dest, is_copy_first_folder, not_copy_folder_name):
    """
    增加两个参数，控制：是否拷贝一级目录，是否排除掉某个目录
    :return: 
    """
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        file_list = os.listdir(src)
        for file in file_list:
            src_file = src + "/" + file
            if os.path.isdir(src_file):
                if is_copy_first_folder:
                    direct_name = os.path.basename(src_file)
                    if direct_name != not_copy_folder_name:
                        dest_file = dest + "/" + file
                        copy_folder_except_folder(src_file, dest_file, is_copy_first_folder, not_copy_folder_name)
            else:
                dest_file = dest + "/" + file
                shutil.copy(src_file, dest_file)
    else:
        shutil.copy(src, dest)


def resize_image(src_image_path, dest_image_path, width, height):
    """
    重置图片的格式大小 比如：722*960 -> 120*120之类的。
    :param src_image_path: 原图片 文件路径
    :param dest_image_path: 生成图片 文件路径
    :param width: 新图片的宽
    :param height: 新图片的长
    :return:
    """
    im = Image.open(src_image_path)
    try:
        out = im.resize((width, height), Image.ANTIALIAS)
        out.save(dest_image_path)
    except Exception:
        error_msg = '重置【%s】图片的格式大小保存在【%s】,出错' % (src_image_path, dest_image_path)
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_msg)
        traceback.print_exc()
        sys.exit(1)


def download_all_file(url_path_json):
    for cs_url in url_path_json:
        file_path = url_path_json[cs_url]
        logger.debug('下载url：%s ,下载目标路径：%s' % (cs_url, file_path))
        download_cs_file(cs_url, file_path, 3)

    return True


def multi_download_pool(url_path_array):
    down_size = len(url_path_array)
    logger.info('multi download 开始，总任务数：%s' % str(down_size))
    if down_size == 0:
        return
    start = time.time()

    # Make the Pool of workers
    pool = ThreadPool(12)

    # Open the urls in their own threads and return the results
    results = pool.map(download_all_file, url_path_array)
    # logger.debug((results)

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    end = time.time()
    logger.info('耗时：%s秒' % str(end - start))


def check_use_cache(cs_url):
    #图片的几种格式：
    suffix_tuple = ("bmp", "jpg", "jpeg", "png", "gif", "rle", "tag")
    begin_index = cs_url.rfind(".") + 1
    suffix_type = cs_url[begin_index:]
    if suffix_type.lower() in suffix_tuple:
        return True
    else:
        return False


def file_download_cache(cs_url, file_path, file_type):
    cache_base_path = "/data/jenkins/res"
    if platform.system() == "Darwin":
        cache_base_path = "/usr/local/sdp/jenkins/res"
        # 取url的md5值
    md5_value = get_md5(cs_url)
    # 文件名
    #begin_index = file_path.rfind("/") + 1
    #file_name = file_path[begin_index:]
    file_name = os.path.basename(file_path)

    cache_parent_path = os.path.join(cache_base_path, file_type, md5_value, file_name)
    if not os.path.exists(cache_parent_path):
        create_parent_path(cache_parent_path)
        # 下载到缓存区。
        r = requests.get(cs_url)
        with open(cache_parent_path, "wb") as code:
            code.write(r.content)
            # 拷贝文件到指定目录
    copy_file(cache_parent_path, file_path)


def del_file(del_file_path):
    os.remove(del_file_path)


def get_cs_download_path(cs_config, cs_path):
    """
    生成CS下载地址
    :param cs_config:
    :param cs_path:
    :return:
    """
    host_path = cs_config.host.replace("http://cs.101.com", "https://gcdncs.101.com") + "/static/" + cs_config.server_name + "/" + cs_path
    return host_path


def download_large_file(download_url, target_path):
    """
    下载大文件到指定目录下
    :param download_url:
    :param target_path:
    :return:
    """
    logger.info("开始下载")
    start_time = int(round(time.time() * 1000))
    r = requests.get(download_url, stream=True)
    with open(target_path, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    file.close()
    end_time = int(round(time.time() * 1000))
    logger.info("下载完成，耗时：" + str(end_time - start_time) + "ms")


if __name__ == '__main__':
    file_path = os.path.join('e:\\', 'target', 'skinTemp', 'native')

    path_one = os.path.join(file_path, '1527666335932.png')
    path_two = os.path.join(file_path, '1527666328131.png')

    url = 'http://betacs.101.com/v0.1/static/qa_content_native_storage/调接口图片0403_1527666335932.png'
    # url = 'http://betacs.101.com/v0.1/static/qa_content_native_storage/\u8c03\u63a5\u53e3\u56fe\u72470403_1527666335932.png'
    # url_1 = str(url.encode('utf-8'), encoding='utf-8')
    # url_1 = url.encode('gb2312')
    # logger.debug(quote(url, safe='/:?='))
    # response = urllib.request.urlopen(quote(url, safe='/:?='))

    url_path_array = [
        {
            url: path_one
        },
        {
            url: path_two
        }
    ]

    # multi_download_pool(url_path_array)
    cs_url = 'http://cdncs.101.com/v0.1/download?path=/release_package_repository/jenkins_app_factory_config/page_attributes.json&attachment=true&serviceName=release_package_repository'

    response = urllib.request.urlopen(quote(cs_url, safe='/:?='))
    response.read()
    #
    # # 过滤文件，压缩
    # zip_file = "E:\\copytest1\\ccc.zip"
    # zip_file_path = "E:\\copytest1\\1505284920731"
    #
    # filter_list = []
    # filter_list.append(".git")
    # filter_list.append(".idea")
    # filter_list.append("dist")
    # filter_list.append("node_modules")
    # zip_filter_folder_file(zip_file, zip_file_path, False, filter_list)

    # 文件拷贝
    # src = "E:\\copytest"
    # dest = "E:\\copytest1"
    # copy_folder_except_folder(src, dest, True, "zipfile")

    # # 文件解压
    # src = "E:\\copytest\\aaa.zip"
    # dest = "E:\\copytest1\\"
    # unzip_language(src, dest,"aaa")
