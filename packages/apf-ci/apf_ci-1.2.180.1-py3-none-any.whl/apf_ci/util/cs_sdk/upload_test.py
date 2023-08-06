#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import base64
import hmac
import datetime
from hashlib import md5, sha1
from urllib.parse import quote_plus
import uuid
from pathlib import Path

import requests
from requests_toolbelt import MultipartEncoder

import sys

service_name = 'qa_content_native_storage'
access_key = 't5329TepSQSS23YL'
secret_key = 'RUaDeiLuFKHM5gX5qgW871NYvv31p28N'
path = '/qa_content_native_storage/guard/empty.txt'
filename = 'empty.txt'

# 上传策略，查看方式为公开，path为上传的文件路径
policy = json.dumps({
    'path': path,
    'uid': 505459,
    'role': 'admin',
    'policyType': 'upload',
    'scope': 1,
}, separators=(',', ':'))

date_gmt = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
print("date_gmt=" + date_gmt)
#date_gmt = "Thu, 20 Feb 2021 9:45:55 GMT"
sign_source_str = "{}\n{}\n{}\n{}".format(
    date_gmt, '/v0.1/upload', 'POST', policy)
# base64后的策略，与java的有差异后面会多= 需要替换掉
policy_str = bytes.decode(base64.urlsafe_b64encode(
    policy.encode())).replace('=', '')

print("stringToSign=\n" + sign_source_str)
print("policy_json=" + policy)
print("policy_base64=" + policy_str)

sign = hmac.new(secret_key.encode(),
                sign_source_str.encode(), sha1).digest()
sign_str = bytes.decode(base64.urlsafe_b64encode(sign)).replace('=', '')
token = '{}:{}:{}'.format(service_name, access_key, sign_str)

url = "https://betacs.101.com/v0.1/upload?token=" + token + \
    "&date=" + quote_plus(date_gmt) + "&policy=" + policy_str
print("token=" + token)
print("date=" + quote_plus(date_gmt))
print("url=" + url)
data = open('F:\\workplace\\apf-ci\\13663591898_180525.txt', 'rb')
md5sum = md5(data.read(1024)).hexdigest()
size = Path('F:\\workplace\\apf-ci\\13663591898_180525.txt').stat().st_size
print(size)

# 上传文件
boundary = '----' + uuid.uuid4().hex
encoder = MultipartEncoder(fields={
    'file': (filename, open('F:\\workplace\\apf-ci\\13663591898_180525.txt', 'rb'), 'tetx/plain'),
    'name': filename,
    'path': path,
    'md5': md5sum,
}, boundary=boundary)

headers = {
    'Content-Type': 'multipart/form-data; boundary=' + boundary
}
r = requests.post(url, data=encoder, headers=headers)
print(r)
sys.stdout.buffer.write(r.content)