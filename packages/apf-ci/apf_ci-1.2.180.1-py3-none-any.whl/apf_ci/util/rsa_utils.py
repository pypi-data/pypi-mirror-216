#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
使用cryptography 模块，实现rsa加密、解密、签名、验签功能。
原java插件已提供秘钥。这里将直接使用秘钥内容。
"""

import json
import base64

import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from apf_ci.util.file_utils import *
from apf_ci.util.http_utils import get_data
from apf_ci.util.log_utils import logger
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum


# 私钥内容b
__private_key_str = b'-----BEGIN RSA PRIVATE KEY-----\n' + \
                    b'MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAKj5o8Bxz/9H6C67\n' + \
                    b'mBzAFBqQBI76PBIjLCkGgGkJMos4XeBf/hk2khhPCIUNw06l+X41uYKEsao+7ayi\n' + \
                    b'VUnLdmBB1SdyFMrm5DhvciX8p9wXKgq0JRmA8clmgVjgTjomVGCy4HXNn8iK72CI\n' + \
                    b'XESHnlXZcGN1crDOQCQ6MvvKuvvtAgMBAAECgYAzRROvd5kBvyKu01KzHoC7Eomf\n' + \
                    b'jEOfyTZD+GoL9LN2VJL/WoDxy4IGiCxwmp1xBqEt70UrWfHCUzewUs0ICAkRa4qC\n' + \
                    b'/Yf0fi8odN810EB7nxLdTU5v0LK9MHG42ov12OY53uixZ3iJGu4b8rg9vHF3ODFQ\n' + \
                    b'lJWEJWgnBT0LhgGDAQJBANRVfOu5wgmJlW3cTqInIyXFO7rzKn3BCqv7F2FpAJOn\n' + \
                    b'Jl9OQf6K6UggIonvN4orz7IqAANo58c3lGPKIBrkaa0CQQDLuX1I8nv+ytnzwAH5\n' + \
                    b'NcI0f/R5J0JvNY+11uUYaF4V40alKM/DQ5JYdfz0268rDrQD3VBG/8XSpSs8IF4Z\n' + \
                    b'n6NBAkEAwrfy6ylaa+ykAC98XO+PJ+ALupGscc5JvxVwh4AHa2BprBTUKF2zONVf\n' + \
                    b'Vybsw+URfs1NXdMiWmr5xdliP8cfsQJBALUHcujrcHuMzffnWtmUh6oXOaqe1E32\n' + \
                    b'DmnLN3Bk7ZYNi60fgt9EoDqzPcBnplRgkF4Ov1MX3TW9R5n6OSQT0wECQQCd3HZT\n' + \
                    b'vUMkHVeGOH9rXt9yh6YIWoRvD9lDYuaeP0QKBIPNJdeqPrh0cCXUiWfxTKagSN/8\n' + \
                    b'gUluy6Y52XBC2YpE\n' + \
                    b'-----END RSA PRIVATE KEY-----\n'

def encrypt(src_data, public_key_content):
    """
    对原始数据使用指定的公钥进行加密
    :param src_data: 原始数据（bytes数组）
    :param public_key_content: 用于加密的公钥（公钥可通过私钥生成）（bytes类型）
    :return: 加密结果的为bytes
    """
    # 从公钥数据中加载公钥
    public_key = serialization.load_pem_public_key(
        public_key_content,
        backend=default_backend()
    )

    # 使用公钥对原始数据进行加密，使用PKCS#1 v1.5的填充方式
    out_data = public_key.encrypt(
        src_data,
        padding.PKCS1v15()
    )

    # 返回加密结果
    encodestr = base64.b64encode(out_data).decode("utf-8")
    logger.debug("加密后输出的是bytes，加密后数据(base64编码): %s" % encodestr)
    return out_data


def decrypt(src_data):
    """
    对原始数据使用指定的私钥进行解密
    :param src_data: 原始数据（bytes数组）
    :return: 解密结果为bytes
    """
    # 从私钥数据中加载私钥
    private_key = serialization.load_pem_private_key(
        __private_key_str,
        password=None,
        backend=default_backend()
    )

    # 使用私钥对数据进行解密，使用PKCS#1 v1.5的填充方式
    out_data = private_key.decrypt(
        src_data,
        padding.PKCS1v15()
    )

    # 返回解密结果
    logger.debug("解密后数据: %s" % out_data)
    return out_data


def private_sign(src_data):
    """
    使用私钥签名（相当于用私钥加密）
    :param src_data: 需要签名的字符串（bytes数组）
    :return:返回的结果为bytes
    """
    private_key = serialization.load_pem_private_key(
        __private_key_str,
        password=None,
        backend=default_backend()
    )

    signature = private_key.sign(
        src_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    encodestr = base64.b64encode(signature).decode("utf-8")
    logger.debug(' 返回结果为bytes，签名后数据(base64编码)：', encodestr)
    return signature


def public_verify(src_data, sign_data):
    """
    使用私钥提取公钥，用于解签验证签名数据是否匹配。若不匹配
    :param src_data:原签名字符串（bytes数组）
    :param sign_data:提供签名的数据,需要bytes数组的形式
    :param private_key_content:用于验签的私钥数据（私钥提取公钥验签）（bytes数组）
    :return:
    """
    private_key = serialization.load_pem_private_key(
        __private_key_str,
        password=None,
        backend=default_backend()
    )
    try:
        public_key = private_key.public_key()
        public_key.verify(
            sign_data,
            src_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except cryptography.exceptions.InvalidSignature as e:
        error_msg = "该签名验证失败:", e
        logger.error(LoggerErrorEnum.VALIDATE_FAILURE,error_msg)
        traceback.print_exc()


def rsa_util_jar_encryptMd5(md5_data):
    """
    调用证书服务rsa接口签名
    :param md5_data: 原始md5数据,str类型
    :return:
    """
    if not md5_data:
        logger.warning(" 计算出的Md5.json文件的md5值为空！")
        return ""
    variables_path = os.path.join(os.getcwd(), "target/variables.json")
    variables_dict = json.loads(read_file_content(variables_path))
    codesign_host = variables_dict["codesign"]
    url = codesign_host + "/v0.1/common/tools/rsa/sign/" + md5_data
    resp = get_data(url)
    result_content = resp.get("rsa_sign", "")
    return result_content


if __name__ == "__main__":
    # 读取私钥、公钥
    with open(r"D:\prikey_pubkey\rsa_private.pem", "rb") as prifile:
        private_key_content = prifile.read()
    with open(r"D:\prikey_pubkey\rsa_pub.pem", "rb") as pubfile:
        public_key_content = pubfile.read()

    # 原字符串（文件内容md5的数据）(bytes类型)
    file_md5_bytes = b"6ddd55183703d54ad14463f3e45ae759"

    # 公钥加密
    #out = encrypt(file_md5_bytes, public_key_content)
    # 私钥解密
    # out = decrypt(out)

    # 私钥签名
    out = private_sign(file_md5_bytes)

    # 公钥验签
    public_verify(file_md5_bytes, out)

    # 使用Jar包进行rsa加密
    print(rsa_util_jar_encryptMd5("48a7b9a8c23a659fcd834961c2700841"))
