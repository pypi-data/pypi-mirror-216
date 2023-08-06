#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
实现python解析properties文件。
v1.0 :解析properties，可增加，修改，查询是否存在
"""

import re
import os
import tempfile
import time


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception:
            open(self.file_name, 'w')
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        self.replace_property(self.file_name, key + '=.*', key + '=' + value, True)

    def replace_property(self, file_name, from_regex, to_str, append_on_not_exists=True):
        tmpfile = tempfile.TemporaryFile()

        if os.path.exists(file_name):
            # 读取原文件
            r_open = open(file_name, 'r')
            pattern = re.compile(r'' + from_regex)
            found = None
            for line in r_open:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(from_regex, to_str, line)
                # 写入临时文件
                tmpfile.write(line.encode())
            if not found and append_on_not_exists:
                asc_time = time.asctime(time.localtime(time.time()))
                tmpfile.write(('\n#\n#' + asc_time + "\n" + to_str).encode())
            r_open.close()
            tmpfile.seek(0)

            # 读取临时文件中的所有内容
            content = tmpfile.read().decode('utf-8')

            if os.path.exists(file_name):
                os.remove(file_name)

            # 将临时文件中的内容写入原文件
            with open(file_name, 'w') as file:
                file.write(content)
            # 关闭临时文件，同时也会自动删掉临时文件
            tmpfile.close()
        else:
            logger.debug("file %s not found" % file_name)


if __name__ == "__main__":
    # 使用方法
    file_path = 'local.properties'
    # 读取文件
    props = Properties(file_path)
    # 修改/添加key=value
    props.put('react', 'false')
    # 根据key读取value
    print(props.get('react'))
    # 判断是否包含该key
    print("props.has_key('react')=" + str(props.has_key('react')))
