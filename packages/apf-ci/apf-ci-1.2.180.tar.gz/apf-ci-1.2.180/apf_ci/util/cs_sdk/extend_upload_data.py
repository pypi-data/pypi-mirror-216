#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = '370418'
"""
cs 上传接口数据
"""

class ExtendUploadData:

    def __init__(self):
        self.file_path = ""
        self.chunks = 0
        self.chunk = 0
        self.chunk_size = 0
        self.pos = 0
        self.expire_days = 0
        self.rename = True
        self.file_size = 0