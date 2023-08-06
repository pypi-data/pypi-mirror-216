#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = '370418'

import math
from apf_ci.util.md5_utils import get_md5

# 分块大小，大于 30MB 就需要分块
CHUNK_SIZE = 5242880*6


def count_chunks(byte_total):
    """
     计算分块上传的份数
    """
    count = byte_total / CHUNK_SIZE
    return math.ceil(count)


def count_start_index(chunk_index):
    """
     计算当前分块的起始值
    """
    return chunk_index * CHUNK_SIZE


def count_end_index(file_size, chunk_index):
    """
     计算当前分块的结束值
    """
    end_index = (chunk_index + 1) * CHUNK_SIZE
    if file_size < end_index:
        end_index = file_size
    return end_index


def to_byte_array(file_path, start, end):
    """
    读取文件指定片段的内容
    """
    fstream = open(file_path, mode='rb')
    fstream.seek(start)
    return fstream.read(end - start)

def get_file_md5(file_path):
    """
    读取文件指定片段的内容
    """
    fstream = open(file_path, mode='rb')
    md5 = get_md5(fstream.read())
    return md5