#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
target/build_config.json 相关操作

"""
from cryptography.fernet import Fernet
from apf_ci.util.jenkins_utils import envs_value
from jsonmerge import merge
from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import get_data_with_env_headers, get_data
import json
import sys

# cipher_key = Fernet.generate_key()
cipher_key = b'oBxeFR6T7ZnsWaTGQxLXBl5Lj_MjEJwlOYDrANWpzkw='
cipher = Fernet(cipher_key)


class BuildConfig:
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_path = os.path.join(target_path, 'build_config.json')

    def get_build_config(self, env_jenkins, is_local):
        """
        根据不同环境 下载 构建配置信息 并存储
        :return:
        """
        build_config_url = envs_value('APP_FACTORY_BUILD_CONFIG', env_jenkins, is_local)
        # build_config_url = self.envs_value('APP_FACTORY_BUILD_CONFIG', env_jenkins, is_local)
        logger.info('build_config_url=' + build_config_url)
        build_config_data = read_cs_content(build_config_url)
        return json.loads(build_config_data)

    def write_build_config(self, build_config_json):
        """
        写入 target/build_config.json ,并且加密其中的secret_config_data字段
        :return:
        """
        secret_config_data = build_config_json['secret_config_data']
        if secret_config_data:
            secret_config_str = json.dumps(secret_config_data)
            encrypt_data = cipher.encrypt(secret_config_str.encode())
            build_config_json['secret_config_data'] = encrypt_data.decode()
        write_content_to_file(self.file_path, json.dumps(build_config_json))

    def read_build_config(self):
        """
        读取 target/build_config.json，解密其中的secret_config_data字段，并展平
        :return:
        """
        if os.path.exists(self.file_path):
            build_config_data = read_file_content(self.file_path)
            build_config_json = json.loads(build_config_data)
            build_config_json = self.decrypy_build_config(build_config_json, True)
            return build_config_json

    def decrypy_build_config(self, build_config_json, is_encrypt=False):
        """
        对于build_config.json，解密其中的secret_config_data字段，并展平
        :is_encrypt： 是否加密后的数据，是的话需要解码，未加密的话，只需要展开字段
        :return:
        """
        result = build_config_json
        secret_config_data = build_config_json['secret_config_data']
        if secret_config_data:
            if is_encrypt:
                secret_config_str = json.dumps(secret_config_data)
                encrypt_data = cipher.decrypt(secret_config_str.encode())
                secret_config_data = json.loads(encrypt_data.decode())
            schema = {
                "mergeStrategy": "objectMerge"
            }
            # build_config_json['secret_config_data'] = ''
            result = merge(build_config_json, secret_config_data, schema)
        return result


def get_environment_name(build_config_json, envtarget):
    # build_config_json = get_build_config_json(target_path)
    environment_dict = get_environment_map(build_config_json)
    environment_json = environment_dict[envtarget]
    environment_name = environment_json['name']
    return environment_name


def get_environment_map(build_config_json):
    """
    解析build_config_json数据中的app_factory_build_environment节点
    :param build_config_json: build_config.json文件内容
    :return: 以envtarget值为key， 对应的整个json为value
    """
    environment_dict = {}
    environment_json_array = build_config_json['app_factory_build_environment']
    for environment_json in environment_json_array:
        key = environment_json['envtarget']
        environment_dict[key] = environment_json

    return environment_dict


# 已废弃，待移除
def get_ios_dns_enable_environment(build_config_json):
    return build_config_json['ios_dns_enable_environment']


def get_ios_dns_disable_environment(build_config_json):
    return build_config_json['ios_dns_disable_environment']


def get_rn_debug_mode(build_config_json):
    return build_config_json['rn_debug_mode']


def get_app_factory_deploy_host(build_config_json):
    return build_config_json['app_factory_deploy_host']


def parse_app_factory_deploy_host(build_config_json, config_json, lite_app_host, default_domain):
    deploy_host_json = get_app_factory_deploy_host(build_config_json)

    # 由于配置 app_factory_deploy_host 里存在 XXX 和 XXX_cdn 的情况，需要以cdn的为准。故多一个map来记录
    cdn_config_map = {}

    for deploy_host_key in deploy_host_json:
        host_json = deploy_host_json[deploy_host_key]
        default_host = host_json['default']
        stage = config_json['stage']

        # 如果以_cdn结尾的key，优先使用
        if deploy_host_key.endswith("_cdn_default"):
            if stage in host_json.keys() and host_json[stage]:
                # 加入去重判断表,并去掉key中的_cdn
                deploy_host_key = deploy_host_key[:deploy_host_key.index("_cdn_default")]
                if deploy_host_key == 'lite_app_host':
                    default_host = host_json[stage]["stage"] + 'v1'
                else:
                    default_host = host_json[stage]["stage"]

                cdn_default_host = default_host
                cdn_config_map[deploy_host_key] = True
                print("[INFO] deploy_host_key : " + deploy_host_key + " 替换CDN域名：" + cdn_default_host)
                parse_cdn_host(config_json, deploy_host_key, host_json, cdn_default_host, True)
        else:
            if deploy_host_key == 'update_host' or deploy_host_key == 'history_url':
                if stage in host_json.keys():
                    stage_host_json = host_json[stage]
                    if stage_host_json['stage']:
                        default_host = stage_host_json['stage']
            elif deploy_host_key == 'lite_app_host':
                default_host = lite_app_host + 'v1'
            else:
                if stage in host_json.keys():
                    if host_json[stage]:
                        default_host = host_json[stage]
            config_json[deploy_host_key] = default_host
            # 当已经去到cdn域名时，这里不再替换了
            if deploy_host_key not in cdn_config_map.keys():
                parse_cdn_host(config_json, deploy_host_key, host_json, default_domain, False)


def parse_cdn_host(config_json, deploy_host_key, host_json, default_domain, is_cdn=False):
    '''
     对，带有 common_component 字段的host ,在config.json 里生成 xxx_cdn
    '''
    if is_cdn:
        # 如果是config_{env}.json 配置的 xxxxx_cdn 的域名，则使用配置的cdn域名替换掉统一域名，且不加 通用组件common_component
        cdn_host = default_domain
        cdn_host_key = deploy_host_key + "_cdn"
        config_json[cdn_host_key] = cdn_host
    elif default_domain != "" and "common_component" in host_json:
        cdn_host = default_domain + "/" + host_json["common_component"]
        cdn_host_key = deploy_host_key + "_cdn"
        config_json[cdn_host_key] = cdn_host


def get_app_cdn_host(build_config_json, config_json, factory_id):
    '''
     对，带有 common_component 字段的host ,在config.json 里生成 xxx_cdn
    '''
    try:
        deploy_host_json = get_app_factory_deploy_host(build_config_json)
        domain_service = deploy_host_json["domain_service"]["default"]
        app_id_url = "%s/v0.1/apps/actions/query/apps/%s" % (domain_service, factory_id)
        app_id_resp = get_data(app_id_url, False)
        portal_web_domain_host = deploy_host_json["portal_web_domain_host"]["default"]
        # app_id = config_json["appid"]
        main_domain_url = "%s/v0.1/products/%s/sites/default-domains/actions/query" % (
            portal_web_domain_host, app_id_resp["sdp_app_id"])
        resp = get_data_with_env_headers(main_domain_url, config_json["env_client"])
        return resp["default_domain"]
    except Exception as e:
        logger.debug("获取 default_domain 失败")
        logger.warning(e)
        traceback.print_exc()
        return ""


def parse_private_host(deploy_host_json, app_json, env, deploy_host_key):
    '''
    从 deploy_host_json 获取相应环境的host
    '''
    host_json = deploy_host_json[deploy_host_key]
    default_host = host_json[env]['stage']
    # 参考 parse_app_factory_deploy_host  这里要加上 v1
    if deploy_host_key == 'lite_app_host':
        default_host = default_host + 'v1'

    app_json[deploy_host_key] = default_host


def get_dns_enable(env, ios_dns_disable_environment):
    dns_enable = True

    if env in ios_dns_disable_environment:
        dns_enable = False

    return dns_enable


def parse_app_host(build_config_json, config_json, lite_app_host):
    deploy_host_json = get_app_factory_deploy_host(build_config_json)

    for deploy_host_key in deploy_host_json:
        host_json = deploy_host_json[deploy_host_key]
        default_host = host_json['default']
        stage = config_json['stage']

        if deploy_host_key == 'update_host' or deploy_host_key == 'history_url':
            if stage in host_json.keys():
                stage_host_json = host_json[stage]
                if stage_host_json['stage']:
                    default_host = stage_host_json['stage']
        elif deploy_host_key == 'lite_app_host':
            default_host = lite_app_host + 'v1'
        else:
            if stage in host_json.keys():
                if host_json[stage]:
                    default_host = host_json[stage]

        config_json[deploy_host_key] = default_host


if __name__ == "__main__":
    pass
    target_path = 'F://workplace//python//jenkins-plugin-python//tests//target'
    config_path = target_path + '//config_aa.json'
    config_json = json.loads(read_file_content(config_path))

    build_config = BuildConfig(target_path)
    build_config.write_build_config(config_json)
    build_config_json = build_config.read_build_config()
    config_test_path = target_path + '//config_test.json'
    write_content_to_file(config_test_path, json.dumps(build_config_json))
