# coding=utf-8
# python2 下uc代码，只做测试使用
import json
import hashlib
import sys
#from .http import Http
from urllib2 import urlparse
#from apf_ci.util.log_utils import logger
from apf_ci.util.uc_sdk import rand
#from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
import time
#from .nd_path import NdPath
#import http as cofHttp
#import restful as CoRestful
import re
import base64
import requests
from hmac import new
from pyDes import des, ECB, PAD_PKCS5

#nd_path_o = NdPath()


class UcEnv:
    ol = 1  # 无锡生产环境
    pre = 2 # 预生产环境
    awsca = 4
    wjt = 5
    snwjt = 6
    hk = 7

def get_beijing_time(utc_time):
    """
    根据iso时间获取北京时间
    utc_time 评价的创建时间，utc格式，'2015-12-28T03:05:56.000+0000'
    """
    real_time = utc_time[:-9]
    time_array = time.strptime(real_time, "%Y-%m-%dT%H:%M:%S")
    time_stamp = int(time.mktime(time_array))

    beijing_time_stamp = time_stamp + 60 * 60 * 8
    # beijing_time_stamp = time_stamp
    beijing_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(beijing_time_stamp))

    return beijing_time

def get_password_md5(passwd):
    """
    该函数用于获取加密过的密码
    :param passwd: 要加密的明文密码
    :return: password_md5就是加密后的密码了
    """
    passwd = passwd.replace('`', '\`')
    passwd = passwd.replace('\'', '\\\'')
    passwd = passwd.replace('"', '\\\"')

    # add laibaoyu  更新md5加密采用python计算，不在用jar计算
    hex_str = "a3aca1a3"  # UC 固定的插值 16进制字符byte：163 172 161 163
    salt = 'fdjf,jkgfkl'  # UC 固定的的salt值
    bt = []
    for i in range(0, len(hex_str), 2):
        b = hex_str[i:i + 2]
        bt.append(chr(int(b, 16)))
    btmd5 = ''.join(bt)
    md5_input = str(passwd) + btmd5 + salt
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(md5_input)
    passwd_md5 = hl.hexdigest()

    #md5_input2 = md5_input.encode('utf-8')
    #h2 = hashlib.md5()
    #h2.update()
    #passwd_md5 = hl.hexdigest()
    return passwd_md5

class NdUc(object):
    # UC登录版本默认为0.93, 非UC服务的测试环境对接UC预生产
    def __init__(self, env=UcEnv.ol, uc_version='0.93', uc_header=None):
        """
        :param env: 取值范围 class UcEnv
        :param uc_version: 支持0.93, 1.1
        :param uc_header:
        """
        self.uc_version = str(uc_version)
        #self.rest_o = CoRestful.Restful()
        self.auth_header_switch = ''
        if uc_header != None:
            self.header = uc_header
        else:
            self.header = {
                "Content-Type": "application/json"
            }
        self.session = None
        self.des_ecb = None     # 使用 session key的 ecb模式加解密方式

        self.login_info = None  # 个人或组织账户登录信息(已解密mac_key,user_id,account_id)
        self.bearer_login_info = None  # bearer账户登录信息

        # ------------根据版本号和环境配置uc域名--------------- #
        self.env = env
        self.port = None
        self.host = None
        self.ssl = None
        if self.uc_version == '0.93':
            if self.env == UcEnv.hk:
                self.host = "uchk.101.com"
            elif self.env == UcEnv.snwjt:
                self.host = "uc.sneduyun.com.cn"
            elif self.env == UcEnv.wjt:
                self.host = "ucwjt.101.com"
            elif self.env == UcEnv.ol:
                self.host = "aqapi.101.com"
            elif self.env == UcEnv.pre:
                self.host = "ucbetapi.101.com"
            elif self.env == UcEnv.awsca:
                self.host = "uc-awsca.101.com"
        elif self.uc_version == '1.1':
            if self.env == UcEnv.hk:
                self.host = "uc-gateway.hk.101.com"
            elif self.env == UcEnv.snwjt:
                self.host = "uc-gateway.sneduyun.com.cn"
            elif self.env == UcEnv.ol:
                self.host = "uc-gateway.101.com"
            elif self.env == UcEnv.pre:
                self.host = "uc-gateway.beta.101.com"
            elif self.env == UcEnv.awsca:
                self.host = "uc-gateway.awsca.101.com"
        else:
            raise Exception("UC认证服务版本未传或者指定有误！仅支持0.93, 1.1")

        # 目前，uc的生产、预生产环境，都使用https协议
        if self.env in [UcEnv.ol, UcEnv.pre, UcEnv.awsca, UcEnv.wjt, UcEnv.snwjt, UcEnv.hk]:
            self.is_ssl = True
        else:
            self.is_ssl = False
        #logger.info("uc version="+self.uc_version+" uc host="+ self.host)

    # -------------- 生成授权头部 Authorization ------------------ #

    def get_Authorization(self, request_url=None, http_method=None, request_host=None, request_header=None, auth_type="mac"):
        """
        获得授权令牌
        :param request_url: 请求的url
        :param http_method: 请求的http方法[GET, POST, PATCH, PUT, DELETE]
        :param request_host: 请求的服务host
        :param request_header: 请求header
        :param auth_type:  [bearer, mac]; 类型为"mac"时，上方四个参数必填，
        :return: 授权令牌的值
        """
        if auth_type == "bearer":
            authorization = 'Bearer '+'"'+ self.get_bearer_token()+'"'
            return authorization

        if auth_type == "mac":
            if request_url == None or http_method == None or request_host==None:
                raise Exception("缺少参数，无法生成mac令牌")
            mac_token = self.get_mac_token(request_url, http_method, request_host, request_header)
            authorization = 'MAC id="' + mac_token["access_token"] + '",nonce="' + mac_token["nonce"] + '",mac="' + mac_token["mac"] + '"'
            return authorization

        raise Exception("不支持的令牌类型: "+str(auth_type))

    # -------------- 生成 mac token ----------------- #

    def get_mac_token(self, request_url, http_method, request_host, request_header):
        """
        获取mac token（注：依赖前置步骤 set_login_info）
        :param request_url: 请求的url
        :param http_method: 请求的http方法[GET, POST, PATCH, PUT, DELETE]
        :param request_host: 请求的服务host
        :param request_header: 请求header
        :return: 用于拼接 authorization 的键值对
        """
        if self.login_info == None:
            raise Exception("请先执行set_login_info，设置账户登录信息")

        mac_key = self.login_info['mac_key']

        ms_format = int(time.time()*1000)  # 本地时间
        nonce = str(ms_format) + ':' + rand.CoRand.randomword(4) + rand.CoRand.randomwordnumber(4)

        request_content = nonce + '\n' + http_method + '\n' + request_url + '\n' + request_host + '\n'
        if self.uc_version == "1.1" and request_header != None:
            if request_header.has_key("auth-header-switch"):
                if request_header["auth-header-switch"] == "true" or request_header["auth-header-switch"] == "True" or request_header["auth-header-switch"] == True:
                    request_content += self.get_sorted_header_values(request_header)    # sdp开头的header排序后参与mac计算

        mac = base64.b64encode(new(mac_key, request_content, digestmod=hashlib.sha256).digest())
        mac_token = {
            "access_token": self.login_info["access_token"],
            "nonce": nonce,
            "mac": mac
        }
        return mac_token

    def set_login_info(self, login_name, password, org_name=None, if_person=False):
        """
        设置账户登录信息
        :param login_name: 登录名（必填，可以为工号，手机号）
        :param password: 密码（必填）
        :param org_name: 组织编码(选填，当login_name为工号时必填；在1.1称作org_code)
        :param if_person: 是否个人账户登录（手机号登录）
        :return:
        """
        response = self.login(login_name, password, org_name, if_person)
        data_dec = json.loads(response.text)
        #data_dec = self.rest_o.parse_response(response, 201, "账户登录失败")
        des_login_info = self.des_info(data_dec)
        self.login_info = des_login_info

    def login(self, login_name, password, org_name=None, if_person=False):
        """
        支持手机号和工号登录
        :param login_name: 登录名（必填，可以为工号，手机号）
        :param password: 密码（必填）
        :param org_name: 组织编码(选填，当login_name为工号时必填；在1.1称作org_code)
        :param if_person: False 组织账户登录，True 个人账户登录（手机号登录），默认False
        :return: uc登录接口的返回（未校验http code）
        """
        if if_person == False:
            if org_name == None:
                raise Exception("工号登录需传组织编码")
            return self.login_org_account(login_name, password, org_name)
        if if_person == True:
            return self.login_person_account(login_name, password)
        raise Exception("不支持的登录类型")

    def login_org_account(self, login_name, password, org_name):
        """
        组织账户登录
        :param login_name: 登录名（必填，可以为工号，手机号）
        :param password: 密码（必填）
        :param org_name: 组织编码(必填；在1.1称作org_code)
        :return:
        """
        log = "login_name: " + login_name + " org_name: " + org_name + " password: " + password
        #logger.info(log)
        login_name = bytes(login_name)
        self.init_http_obj()
        # 获得session
        session = self.get_session()
        self.session = session
        # 获得md5加密的密码
        #md5_pw = get_password_md5(password)
        md5_pw = password

        des_key = str(session['session_key'])
        des_ecb = des(des_key, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        self.des_ecb = des_ecb
        json_body = {
            "login_name": base64.b64encode(des_ecb.encrypt(login_name)),  # ecb加密后 base64加密
            "password": base64.b64encode(des_ecb.encrypt(md5_pw)),  # ecb加密后 base64加密
            "session_id": session['session_id']
        }
        if self.uc_version == "1.1":
            json_body.update({"login_name_type": "org_user_code", "org_code": org_name})
        if self.uc_version == "0.93":
            json_body.update({"org_name": org_name})

        #param = json.dumps(json_body)

        url = '/v' + str(self.uc_version) + '/tokens'
        response = self.http_post(url, json_body)
        #response = self.http_obj.post(url, param)

        return response

    def login_person_account(self, login_name, password):
        #logger.info("login_name: " + login_name + " password: " + password)
        login_name = bytes(login_name)
        self.init_http_obj()

        session = self.get_session()
        self.session = session

        md5_pw = get_password_md5(password)


        des_key = str(session['session_key'])
        des_ecb = des(des_key, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        self.des_ecb = des_ecb
        json_body = {
            "login_name": base64.b64encode(des_ecb.encrypt(login_name)),  # ecb加密后 base64加密
            "password": base64.b64encode(des_ecb.encrypt(md5_pw)),  # ecb加密后 base64加密
            "session_id": session['session_id']
        }

        param = json.dumps(json_body)

        url = '/v' + str(self.uc_version) + '/tokens'
        #response = self.http_obj.post(url, param)
        response = self.http_post(url, json_body)
        return response

    def logout(self, access_token):
        self.init_http_obj()
        url = '/v' + str(self.uc_version) + '/tokens/' + str(access_token)
        auth = self.get_Authorization(request_url=url, http_method="DELETE", request_host=self.host, request_header=self.header)

        #self.http_obj.header.update({"Authorization": auth})
        #response = self.http_obj.delete(url)
        #self.rest_o.parse_response(response, 200, "登出失败")

    def des_info(self, auth):
        auth['mac_key'] = self.des_ecb.decrypt(base64.b64decode(auth['mac_key']))  # base64解密后 ecb解密
        auth['user_id'] = self.des_ecb.decrypt(base64.b64decode(auth['user_id']))  # base64解密后 ecb解密
        if 'account_id' in auth:
            auth['account_id'] = self.des_ecb.decrypt(base64.b64decode(auth['account_id']))  # base64解密后 ecb解密
        #logger.info("解密后的登录信息 "+json.dumps(auth))
        return auth

    # -------------- 生成 bearer token ----------------- #

    def get_bearer_token(self):
        """
        获取bearer token,需先调用set_bearer_login_info，登录bearer账户
        :return:bearer账户的 access token
        """
        if self.bearer_login_info == None:
            raise Exception("请先执行 set_bearer_login_info，设置bearer账户登录信息")
        return self.bearer_login_info['access_token']

    def set_bearer_login_info(self, username, password=None, has_encoded=True):
        """
        设置bearer登录信息，仅当uc版本为0.93时有效
        :param username:bearer账号
        :param password:bearer密码
        :param has_encoded:密码是否已加密，默认已加密
        :return:
        """
        if self.uc_version != "0.93":
            raise Exception("仅uc 0.93版本支持bearer登录，当前设置版本号: "+str(self.uc_version))
        response = self.bearer_login(username, password, has_encoded)
        data_dec = self.rest_o.parse_response(response, 201, "bearer login faild")
        self.bearer_login_info = data_dec

    def bearer_login(self, username, password, has_encoded=True):
        """
        bearer登录，仅当uc版本为0.93时有效
        :param username:
        :param password:
        :param has_encoded: 密码是否已加密，默认已加密
        :return: uc登录接口的返回（未校验http code）
        """
        self.init_http_obj()
        if self.uc_version != "0.93":
            raise Exception("仅uc 0.93版本支持bearer登录，当前设置版本号: " + str(self.uc_version))

        if has_encoded is False:
            md5_pw = get_password_md5(password)
        else:
            md5_pw = password

        json_data = {
            "login_name": username,
            "password": md5_pw
        }
        param = json.dumps(json_data)

        url = "/v0.93/bearer_tokens"
        #response = self.http_obj.post(url, param)
        response = self.http_post(url, json_data)
        return response

    # -------------- 通用方法--------------------------- #

    def init_http_obj(self):
        """
        初始化http连接，内部调用
        :return:
        """
        #self.http_obj = cofHttp.Http(host=self.host, port=self.port, ssl=self.is_ssl)
        #self.http_obj.set_header(self.header)

    def set_host(self, host):
        """
        自定义设置账号中心主机
        :param host:
        :return:
        """
        self.host = host

    def set_port(self, port):
        """
        自定义设置账号中心端口
        :param port:
        :return:
        """
        self.port = port

    def set_version(self, version):
        """
        自定义设置账户中心的api版本号
        :param version:
        :return:
        """
        self.version = version


    def get_session(self):
        """
        获取session，用于登录加密
        :return:
        """
        randnum = rand.CoRand.randomwordnumber(20)
        check_char = base64.b64encode(get_password_md5(randnum))[2]
        device_id = check_char + 'w' + randnum
        response = self.create_session(device_id)
        code = 201
        message = '创建会话失败'
        if response.status_code != 201:
            error_message = "token获取失败"
            #logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
        token_response = json.loads(response.text)
        #data = self.rest_o.parse_response(response, code, message)
        return token_response

    def create_session(self, device_id, session_type=1):
        """
        {
        "session_type":1, --会话类型，0：注册(手机或邮箱注册)，1：登录(帐户、密码登录)，2：邮箱找回密码，11：登录(短信登录)，12：手机找回密码，13：更新手机号码
        "device_id":"" --设备唯一ID
        }
        :param device_id:
        :return:
        """
        url = ''
        if self.uc_version == "0.93":
            url = '/v' + str(self.uc_version) + '/session'
        if self.uc_version == "1.1":
            url = '/v' + str(self.uc_version) + '/sessions'

        self.init_http_obj()

        json_data = {
            "device_id": device_id,
            "session_type": session_type
        }
        param = json.dumps(json_data)
        #res = self.http_obj.post(url, param)
        res = self.http_post(url, json_data)
        return res


    def http_post(self, url, json_data):
        all_url= "https://"+self.host+url
        res = requests.post(all_url, json=json_data, headers=self.header)
        return res

    def get_sorted_header_values(self, header):
        """
        获得排序后的header值，sdp开头，按字母顺序排序，用于authorization生成
        :type header: dict
        """
        if header == None:
            return ""
        elif not isinstance(header, dict):
            #logger.info("header type invalid "+ str(header))
            return ""

        keys = list()
        values = ''

        pattern = re.compile(r'^sdp-[a-zA-Z][a-zA-Z0-9_-]{0,15}$')

        for key in header.keys():
            match = pattern.match(key.lower())
            if match:
                keys.append(key)
        keys = list(set(keys))
        keys.sort(lambda x, y: cmp(x.upper(), y.upper()))
        for key in keys:
            values += header[key] + '\n'
        return values

    def __del__(self):
        if self.login_info != None:
            access_token = self.login_info["access_token"]
            self.logout(access_token)
        else:
            pass



if __name__ == "__main__":
    username = "10005015"
    password = "4e4a54e852921c30233b75f60f0f2291"
    #password = "abc123456"
    #nd_uc = NdUc()
    nd_uc = NdUc( uc_version='1.1')
    #nd_uc.login(username,password,"nd")
    nd_uc.set_login_info(username,password,"nd")

    request_method = 'POST'
    request_host = 'widget-i18n-store.debug.web.nd'
    request_path = 'v0.1/widgets/language/app/query'
    #request_url = 'http://widget-i18n-store.debug.web.nd/v0.1/widgets/language/app/query'
    #request_uri = urlparse(request_url)
    #mac_tocken = nd_uc.get_Authorization(request_uri.path,request_method, request_uri.netloc)
    mac_tocken = nd_uc.get_Authorization(request_path,request_method, request_host)
    print(mac_tocken)