#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = '370418'

import os
import datetime
from apf_ci.util.file_utils import is_file_invalid
from apf_ci.util.http_utils import *
from apf_ci.util.cs_sdk.chunk_utils import *
from urllib.parse import quote_plus

class Dentry:
    def __init__(self):
        self.path = ''
        self.name = ''
        self.filePath = None
        self.scope = 0
        self.get_cs_token = ''
        self.cs_config = ''
        self.cs_file_path = ''
        self.req_url_path = ''


    def upload(self, cs_config, file_path, upload_data, upload_progress_call_back):
        if is_file_invalid(file_path):
            error_message = 'file_path  参数异常 %s ' % file_path
            logger.warning(error_message)
            return error_message
        file_size = os.path.getsize(file_path)
        if file_size <= CHUNK_SIZE:
            return self.upload_cs_file(file_path, upload_data)
        chunks = count_chunks(file_size)
        upload_data.chunks = chunks

        index = 0
        #self.get_upload_status(cs_config,upload_data)
        while index < chunks:
            start_index = count_start_index(index)
            end_index = count_end_index(file_size, index)
            fstream = to_byte_array(file_path, start_index, end_index)
            upload_data.chunk = index
            upload_data.chunk_size = end_index - start_index
            upload_data.pos = start_index
            upload_data.file_size = file_size
            upload_response = self.upload_cs_file_chunk(file_path, fstream, get_file_md5(file_path), upload_data)
            try :
                pinpoint_traceid =  upload_response.headers._store['pinpoint-traceid'][1]
                if pinpoint_traceid :
                    pinpoint_traceid_message = 'cs 分块上传traceid： ' + pinpoint_traceid
                    logger.debug(pinpoint_traceid_message)
            except:
                pass
            if upload_response.status_code != 200 or index == (chunks - 1):
                return upload_response
            else:
                upload_progress_call_back(end_index, file_size)
            index = index + 1

    def get_cs_upload_api(self):
          date_gmt = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
          cs_token, policy_str = self.get_cs_token(self.cs_config, self.cs_file_path,self. req_url_path, 'POST', date_gmt)
          cs_upload_api = "%s/upload?token=%s&date=%s&policy=%s" % (
          self.cs_config.host, cs_token, quote_plus(date_gmt), policy_str)
          logger.debug("[DEBUG] upload_file_to_cs请求： %s" % cs_upload_api)
          return  cs_upload_api

    def upload_cs_file_chunk(self, file_path, fstream, file_md5, upload_data):
        logger.info('正在分块上传 %s' % file_path)
        data = {
            'path': self.path,
            'name': self.name,
            'scope': self.scope,
            'size': upload_data.file_size,
            'chunk': upload_data.chunk,
            'chunks': upload_data.chunks,
            'chunk_size': upload_data.chunk_size,
            'expireDays': upload_data.expire_days,
            'md5': file_md5
        }
        if self.filePath is not None:
            data.pop('path', None)
            data['filePath'] = self.filePath
        files = {
            'filename': fstream
        }
        upload_response = requests.post(self.get_cs_upload_api(), data, files=files)
        return upload_response

    def upload_cs_file(self, file_path, upload_data):
        logger.info('一次性上传 %s' % file_path)
        data = {
            'path': self.path,
            'name': self.name,
            'scope': self.scope,
            'expireDays': upload_data.expire_days
        }
        if self.filePath is not None:
            data.pop('path', None)
            data['filePath'] = self.filePath
        with open(file_path, 'rb') as filename:
            files = {
                'filename': filename
            }
            upload_response = requests.post(self.get_cs_upload_api(), data, files=files)
        return upload_response

    def get_upload_status(self, cs_config, upload_data):
        '''
        获取分块上传状态，暂时不接入使用
        '''
        date_gmt = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        cs_token, policy_str = self.get_cs_token(self.cs_config, self.cs_file_path,self. req_url_path, 'POST', date_gmt)
        cs_upload_status = cs_config.host + '/upload/actions/status?token=' + cs_token
        cs_upload_status = cs_upload_status + '&chunks=' + str(upload_data.chunks)
        cs_upload_status = cs_upload_status + '&path=' + self.path
        cs_upload_status = cs_upload_status + '&name=' + self.name
        response_body = get_data(cs_upload_status)
        #print(response_body)

