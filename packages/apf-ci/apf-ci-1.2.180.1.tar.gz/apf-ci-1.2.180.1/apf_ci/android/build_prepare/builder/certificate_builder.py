#!/usr/bin/python3
# -*- coding: utf-8 -*-
from apf_ci.util.file_utils import *
from apf_ci.util.md5_utils import *
from apf_ci.util.http_utils import *
from apf_ci.util.property import *
from apf_ci.util.execute_command_utils import *
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger
from apf_ci.app_init.utils.build_config_utils import BuildConfig


class CertificateBuilder:
    def __init__(self, app_id, cert_host, is_custom_build, package_name):
        self.app_id = app_id
        self.cert_host = cert_host
        self.is_custom_build = is_custom_build
        self.package_name = package_name

    def perform(self, variables_dict):
        logger.info(" 开始do android certificate init")
        workspace_path = os.getcwd()
        env_target = variables_dict["envtarget"]
        factory_id = variables_dict["factoryId"]

        compiled_mode = ""
        config_file_path = os.path.join(workspace_path, "app/assets/app_factory/app/config.json")
        if os.path.exists(config_file_path):
            config_str = read_file_content(config_file_path)
            config_json = json.loads(config_str)
            if config_json.get("assemble_mode"):
                compiled_mode = config_json.get("assemble_mode", "").capitalize()
        else:
            logger.warning("app/assets/app_factory/app/config.json 文件不存在")

        transfer_map = {}
        upper_case_package_name_android = []
        build_config = BuildConfig(os.path.join(workspace_path, 'target'))
        build_json = build_config.read_build_config()
        arr = build_json.get("app_factory_build_environment", [])
        for object in arr:
            if isinstance(object, dict):
                key = object.get("envtarget", "")
                value = object.get("name", "")
                transfer_map[key] = value
        upper_case_package_name_android = build_json.get("upper_case_package_name_android", [])
        logger.debug("统一配置中upper_case_package_name_android: %s" % upper_case_package_name_android)

        if not compiled_mode:
            compiled_mode = transfer_map.get(env_target)
        public_key_str = self._certificate_init(factory_id, compiled_mode, env_target)
        logger.debug("签名公钥：【 %s 】包名：【 %s 】" % (public_key_str, self.package_name))

        package_name_real = self._check_package_name(self.package_name, upper_case_package_name_android)
        logger.debug("要签名的包名为：%s" % package_name_real)

        hex_number = str(int(public_key_str, 16))
        logger.debug("签名公钥获取16进制：%s" % hex_number)

        tag_str = "com.nd" + hex_number + package_name_real
        tag_str = get_md5(get_md5(tag_str) + package_name_real)

        logger.debug("签名业务加密后：【 %s 】" % tag_str)

        next_line = "\r\n\t"
        java_code = ""
        java_code += "package com.nd.smartcan.appfactory.demo;" + next_line
        java_code += next_line
        java_code += "public class Const {" + next_line
        java_code += ' public static final String TAG = "%s";' % tag_str
        java_code += next_line
        java_code += "}" + next_line

        self._write_java_code_into_file("Const.java", java_code)

        logger.info(" do android certificate init完毕")


    def _write_java_code_into_file(self, java_class_name, java_code_str):
        appfactory_demo_path = os.path.join(os.getcwd(), "app/src/main/java/com/nd/smartcan/appfactory/demo/")
        java_file_path = os.path.join(appfactory_demo_path, java_class_name)
        if not os.path.exists(appfactory_demo_path):
            os.makedirs(appfactory_demo_path)
        else:
            logger.debug(" java code file 已存在，直接写入生成的code")

        write_content_to_file(java_file_path, java_code_str)


    def _check_package_name(self, package_name, upper_case_package_name_android):
        if package_name not in upper_case_package_name_android:
            package_name = package_name.replace("-", "").lower()
            if package_name.startswith("[1-9]"):
                package_name = "n" + package_name
        return package_name


    def _certificate_init(self, factory_id, target_evn, env_target):
        logger.debug("打包环境：【 %s 】" % target_evn)
        workspace_path = os.getcwd()

        url = self.cert_host + "/v0.1/android/codesign/" + factory_id
        logger.debug("签名信息：%s" % url)
        cert = get_data_with_env_headers(url, env_target)
        if not cert or len(cert) <= 0:
            if not self.is_custom_build:
                store_password = "android"
                key_password = "android"
                key_alias = "androiddebugkey"
                store_destination = "/usr/android/keystore/debug.keystore"
                public_key_str = "9ac668501468effdffe0adef929395d41567ea387dc88b5abb9a95076965f60b191529b01d098de825521216fcfacb955ff6f003f5f14ff7ccd4eafaab009a4bc8fb463060b591325af0ed3773081869e9dfdb101e649e496339d722e1e7c5ce4e2d02595fd94bb529cc9c6c8c26a995345387fcfbf71043d982e605d2ebe579"
            else:
                if target_evn == "Release":
                    return "abb797153279d4fbca4fdd8f4ba44f85567824c15c7f3fe99d087899bc3164b05baf41fbd2983beba91bad1efa7f557db17d0ef6e76c892345e2b3913a3f326288bdb8fc81bce890c7377defd679c63095fc19285bfe657bf36cce1d6c86e352f6dfe07e2bf0b678d577adbf7b12705eec5e9d6996f96bcbb7357ee5a28fa5c53426d68bc01ec6cb47637b0fca4d91c6c7c58262a9f793fbf3ca95829bbb2f3f1ebcb6ef2797dea357c8cb79938ca1a9bd1c9497c9a3c97a646bfcd419c11dc17a71287d12871d1bfc5846f592535b050835bac3dde9128f0451a20e3ded1e4a673bbb981cc5cc41b1de0a8edbcae3be98a12d0d20ef6494d4c029cb406ba579"

                return "8da98ab1a61f9a403735c89d8f56c552592c8cc33a9af22f64cd7a376d82a013a94be33a5fe065f9ca3057cea948e35ac8d39ca9b57266a385ceebdfb19e01e3444e6af72d3385ba946d73a8dba805ffda1bd2ea76bc6280aebf644dd1a2f02be0e86e68205a500dd4a4b861d792da01a23225e292dc8003824d575392aed14c6e634634ab3690756997feef0fffec65699e162eba7f3a7b6e701fa7801acbfb15be5d6f8ccb6bdd396e18ba0c64067d766095cf099a934a5072c1a7c00c95963b9a31955661508ba0ca906223afdc1b9470b0e35d75993b8e2b55f3caa604e98998fb2e32e5bc45747a8de6422a42821df7ee5eefd1515be96fed89686345d7"
        else:
            # 下载证书

            data = cert[0]
            file_url = data.get("url")
            keystore_file_name = data.get("name")
            store_destination = os.path.join(workspace_path, keystore_file_name)
            download_cs_file(file_url, store_destination, 3)

            # keystore文件的相关信息字段
            store_password = data.get("password")
            keys = data['keys']
            key_alias = ''
            key_password = ''
            for key_item in keys.keys():
                key_alias = key_item
                key_password = keys[key_item]
                break

            # 使用KeyTool命令 和 openssl命令解析keystore文件，生成16进制公钥
            # keystore生成的cer证书文件和公钥文件，将保存在target目录下,cer文件命名与keystore一致，公钥命名为pubkey.key
            cer_file_name = keystore_file_name[:keystore_file_name.find(".")] + ".cer"
            cer_file_path = os.path.join(workspace_path, "target", cer_file_name)
            pubkey_file_path = os.path.join(workspace_path, "target", "pubkey.key")
            try:
                # 通过keystore导出cer文件
                # keytool -export -alias xxx(别名) -storepass xxxx(密码) -file xxx.cer -keystore xxx.keystore
                common_gen_cer_str = "keytool -export -alias %s -storepass %s -file %s -keystore %s" % (
                    key_alias, store_password, cer_file_path, store_destination)
                logger.debug(" keytool命令： %s" % (common_gen_cer_str))
                subprocess.call([common_gen_cer_str], shell=True)

                # 通过cer文件提取rsa公钥，并在当前目录下生成publickey.key
                # openssl x509 -inform der -in xxxx.cer -pubkey -noout -modulus > publickey.key
                common_gen_public_str = "openssl x509 -inform der -in %s -pubkey -noout -modulus > pubkey.key" % cer_file_path
                logger.debug(" openssl命令： %s" % common_gen_public_str)
                # subprocess.call([common_gen_public_str], shell=True)
                # 提取出的publickey写入文件
                pubkey_content = execute_command(['openssl', 'x509', '-inform', 'der',
                                                  '-in', cer_file_path,
                                                  '-noout', '-modulus'])
                write_content_to_file(pubkey_file_path, pubkey_content)

                # 读取 pubkey.key文件
                public_key_str = read_file_content(pubkey_file_path)
                if public_key_str:
                    public_key_str = public_key_str[8:].lower()
                else:
                    error_message = '解析keystore出错，公钥文件内容为空，path: %s' % pubkey_file_path
                    logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, error_message)
                    raise Exception(error_message)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

        # 旧的证书
        # local.properties路径
        property_file_path = os.path.join(workspace_path, "local.properties")
        properties = Properties(property_file_path)
        properties.put("RELEASE_STORE_FILE", store_destination)
        properties.put("RELEASE_STORE_PASSWORD", store_password)
        properties.put("RELEASE_KEY_PASSWORD", key_password)
        properties.put("RELEASE_KEY_ALIAS", key_alias)
        properties.put("RELEASE_STORE_PUBLIC_KEY", public_key_str)

        # 新的证书
        properties.put("DEBUG_STORE_FILE", store_destination)
        properties.put("DEBUG_STORE_PASSWORD", store_password)
        properties.put("DEBUG_KEY_PASSWORD", key_password)
        properties.put("DEBUG_KEY_ALIAS", key_alias)
        properties.put("DEBUG_STORE_PUBLIC_KEY", public_key_str)

        return public_key_str


