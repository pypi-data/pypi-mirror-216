#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import hashlib
import os

def get_md5(data):
    """
    对数据进行MD5加密
    :param data:
    :return:
    """
    if isinstance(data, str):
        data = data.encode(encoding='utf-8')

    hl = hashlib.md5()
    hl.update(data)
    return hl.hexdigest()

def upload_and_calc_md5(file, json, filter_path):
    if os.path.isdir(file):
        files = os.listdir(file)
        for file_ele in files:
            file_abs_path = os.path.join(file, file_ele)
            if os.path.isdir(file_abs_path):
                upload_and_calc_md5(file_abs_path, json, filter_path)
            else:
                relative_path =file_abs_path.replace(filter_path, "")[1:]
                with open(file_abs_path, 'rb') as f:
                    file_content_byte = f.read()
                md5 = get_md5(file_content_byte)
                json[relative_path] = md5
    else:
        relative_path = os.path.abspath(file).replace(filter_path, "")[1:]
        with open(file, 'rb') as f:
            file_content_byte = f.read()
        md5 = get_md5(file_content_byte)
        json[relative_path] = md5


if __name__ == "__main__":
    #file_path = 'F:\\workplace\\apf-ci\\slp-app-teacher_3611707_reinforce.apk'
    file_path = 'D:\\Downloads\\pubspec.yaml'
    with open(file_path, 'rb') as f:
        file_content_byte = f.read()
        md5 = get_md5(file_content_byte)
        print(md5)