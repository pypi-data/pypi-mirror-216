#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
部分图片处理模块
"""

__author__ = '370418'


import os
from  apf_ci.util.file_utils import *
from  apf_ci.util.log_utils import logger


def download_image_file(target_path, app_type, new_files_map):
    """
    下载图片文件
    :param target_path:
    :param app_type:
    :param new_files_map:
    :return:
    """
    logger.info('下载newFile文件开始')
    base_path = os.path.dirname(target_path)
    if app_type.lower() == 'android':
        absolute = os.path.join(base_path, 'app', 'res', 'drawable-hdpi')
    elif app_type.lower() == 'ios':
        absolute = os.path.join(base_path, 'ComponentAppBase', 'Resources', 'skin',
                                'com.nd.smartcan.appfactory.main_component_skin.bundle')

    url_path_array = []
    for file_name in new_files_map:
        logger.debug('【判断文件】%s' % file_name)
        file_path_value = new_files_map[file_name]

        if file_name.endswith('.zip'):
            # 上传ZIP包图片，支持多分辨率
            handle_zip_file(file_name, target_path, absolute, app_type)
        else:
            if isinstance(file_path_value, str):
                # 正常图片下载
                if file_path_value:
                    file_path_value = file_path_value.replace('\"', '')
                    save_path = os.path.join(absolute, file_name)
                    logger.debug('下载文件【%s】保存在【%s】' % (file_path_value, save_path))

                    url_path_json = {}
                    url_path_json[file_path_value] = save_path
                    url_path_array.append(url_path_json)
            elif isinstance(file_path_value, dict):
                # 图片适配
                url = file_path_value['_value']
                if url:
                    try:
                        resizes = file_path_value['_resize']

                    except KeyError:
                        resizes = ''

                    if app_type.lower() == 'android':
                        file_name = file_name[file_name.find('@') + 1:]

                    if resizes:
                        # 按规定尺寸输出
                        for resize in resizes.split(','):
                            resize = resize.replace(' ', '')
                            if resize.find('@') > -1:
                                size = resize[0:resize.find('@')]
                            else:
                                size = resize

                            save_relative_path = absolute
                            if app_type.lower() == 'android':
                                hdpi_name = ''

                                if resize.find('@') > -1 and resize[resize.find('@') + 1:]:
                                    hdpi_name = '%s%s' % ('drawable-', resize[resize.find('@') + 1:])
                                else:
                                    model = file_path_value['_model']
                                    if model == 'hdpi' or model == 'xhdpi' or model == 'xxhdpi' or model == 'xxxhdpi':
                                        hdpi_name = '%s%s' % ('drawable-', model)

                                if hdpi_name:
                                    save_relative_path = os.path.join(os.path.dirname(absolute), hdpi_name)

                            save_file_path = os.path.join(save_relative_path, file_name)
                            download_cs_file(url, save_file_path, 3)
                            logger.debug('下载文件【%s】保存在【%s】' % (url, save_file_path))
                            logger.debug('【%s】需要重设图片大小【%s】' % (save_file_path, resizes))

                            if size:
                                if size.find('*') > -1:
                                    output_width = int(size[0:size.find('*')])
                                    output_height = int(size[size.find('*') + 1:])
                                else:
                                    output_width = int(size)
                                    output_height = int(size)

                                resize_image(save_file_path, save_file_path, output_width, output_height)
                    else:
                        save_relative_path = absolute

                        if app_type.lower() == 'android':
                            hdpi_name = ''
                            model = file_path_value['_model']
                            if model == 'hdpi' or model == 'xhdpi' or model == 'xxhdpi' or model == 'xxxhdpi':
                                hdpi_name = '%s%s' % ('drawable-', model)

                            if hdpi_name:
                                save_relative_path = os.path.join(os.path.dirname(absolute), hdpi_name)
                            if file_name.endswith('.json'):
                                # 支持json 格式的图片资源
                                save_relative_path = os.path.join(base_path, 'app', 'res', 'raw')
                        # 按原始尺寸输出
                        save_path = os.path.join(save_relative_path, file_name)
                        logger.debug('下载文件【%s】保存在【%s】' % (url, save_path))
                        url_path_json = {}
                        url_path_json[url] = save_path
                        url_path_array.append(url_path_json)

    if url_path_array.__len__() > 0:
        multi_download_pool(url_path_array)
    logger.info('下载newFile文件结束')

def handle_zip_file(file_name, target_path, absolute, app_type):
    """
    将zip包中的文件通过规则进行拷贝
    :param file_name:
    :param target_path:
    :param absolute:
    :param app_type:
    :return:
    """
    # 取文件名索引
    index = file_name.rfind('/')
    if index == -1:
        # 不带路径的文件索引
        index = 0
    else:
        # 带路径的文件索引
        index += 1

    # 取不带格式的文件名
    folder_name = file_name[index:file_name.rfind('.zip')]
    # 放置zip解压文件的临时路径
    zip_temp_path = os.path.join(target_path, 'zipTemp', folder_name)

    for root, dirs, files in os.walk(zip_temp_path):
        for src_file_name in files:
            format_index = src_file_name.rfind('.')
            suffix_format = src_file_name[format_index:]
            xx_suffix_format = '%s%s' % ('@2x', suffix_format)
            xxx_suffix_format = '%s%s' % ('@3x', suffix_format)

            if app_type.lower() == 'android':
                base_path = os.path.dirname(absolute)

                if src_file_name.endswith(xx_suffix_format):
                    png_path = 'drawable-xhdpi'
                elif src_file_name.endswith(xxx_suffix_format):
                    png_path = 'drawable-xxxhdpi'
                else:
                    png_path = 'drawable-mdpi'

                dest_file_path = os.path.join(base_path, png_path, folder_name, suffix_format)

            elif app_type.lower() == 'ios':
                if src_file_name.endswith(xx_suffix_format):
                    suffix_format = '%s%s' % ('@2x', suffix_format)
                elif src_file_name.endswith(xxx_suffix_format):
                    suffix_format = '%s%s' % ('@3x', suffix_format)

                dest_file_path = os.path.join(absolute, folder_name, suffix_format)

            src_file_path = os.path.join(root, src_file_name)
            copy_file(src_file_path, dest_file_path)
