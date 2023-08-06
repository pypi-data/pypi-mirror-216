"""
把前端的配置信息同步到assets目录下的特定文件中便于应用框架访问
"""
import json
import os
import sys

# pip install jsonmerge
from jsonmerge import merge

from apf_ci.app_init.utils import Variable
from apf_ci.util.log_factory.logger_error_enum import LoggerErrorEnum
from apf_ci.util.log_utils import logger

__version__ = "0.0.1"

__author__ = 'chenqian'

__date__ = "2019-6-18"


def is_file_invalid(file_path):
    if file_path is None:
        return True
    if len(file_path) <= 0:
        return True
    if not os.path.exists(file_path):
        return True
    if not os.path.isfile(file_path):
        return True
    return False


def get_file_rb(file_path):
    """读取文件内容为bytes，如path为空那么返回None"""
    if file_path is not None and len(file_path) > 0:
        with open(file_path, "rb") as fr:
            return fr.read()
    else:
        return None


def get_file_str(file_path):
    """读取文件内容为字符串，如path为空那么返回None"""
    if len(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as fr:
            return fr.read()
    else:
        return None


def loader_json_file(file_path):
    str_json = get_file_rb(file_path)
    if str_json is not None:
        return json.loads(str_json)
    else:
        return None


def get_sub_dict_json(json_data, key_list):
    """
        取json的某个子json
        当前json必须为dict
    """
    if json_data is None or not isinstance(json_data, dict):
        return json_data
    if key_list is None or not isinstance(key_list, list) or len(key_list) == 0:
        message = 'key_list 参数为空或者非list'
        logger.warning(message)
        return json_data

    sub_json = json_data
    for i in key_list:
        if isinstance(sub_json, dict) and i in sub_json:
            sub_json = sub_json[i]
        else:
            break

    return sub_json


def merge_json_file(json_path1, json_path2, key_list1, key_list2, dest_json_path):
    """
       取2个json文件的某一部分（只适用于dict）合并
       如果2个待合并的json结构都是dict，或者都是list,则直接合并
       否则都转成list合并
    """
    try:
        if is_file_invalid(json_path1):
            message = json_path1 + ' 文件名不合法或文件不存在!'
            logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
            return False
        if is_file_invalid(json_path2):
            message = json_path2 + ' 文件名不合法或文件不存在!'
            logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
            return False
        if is_file_invalid(dest_json_path):
            message = dest_json_path + ' 文件名不合法或文件不存在!'
            logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
            return False
        json1 = loader_json_file(json_path1)
        json2 = loader_json_file(json_path2)
        sub_json1 = get_sub_dict_json(json1, key_list1)
        sub_json2 = get_sub_dict_json(json2, key_list2)
        result = merge_json(source_json1=sub_json1, source_json2=sub_json2)
        if result is None:
            message = dest_json_path + ' 合并json失败！'
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, message)
            return False
        with open(dest_json_path, mode='w', encoding='utf-8') as outfile:
            json.dump(result, outfile, ensure_ascii=False)
            return True
    except BaseException as err:
        message = '合并json文件发生异常: ' + err.__str__()
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, message)
        return False


def merge_json(source_json1, source_json2):
    if source_json1 is None or source_json2 is None:
        return None
    json1 = source_json1
    json2 = source_json2
    isMergeList = False
    if isinstance(json1, list):
        isMergeList = True
        if not isinstance(json2, list):
            json2 = [json2]
    if isinstance(json2, list):
        isMergeList = True
        if not isinstance(json1, list):
            json1 = [json1]
    schema = {
        "mergeStrategy": "objectMerge"
    }
    if isMergeList:
        schema = {
            "mergeStrategy": "append"
        }
    result = merge(json1, json2, schema)
    return result


def provide_android_capabilities_to_app(work_space_path):
    """
       把配置的android_capabilities内容从android_config_data.json拷贝到app.json，
       这样便于应用框架读取
       注意：如果dict结构的json和list结构的json合并，会导致最终结构为list
    """
    logger.info(' 开始准备提供安卓能力相关配置 ')
    if (work_space_path is None) or (len(work_space_path) == 0):
        message = '传入的工作空间地址是空，无法继续'
        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
        sys.exit(1)
    try:
        target_path = os.path.join(work_space_path, 'target')
        variable = Variable(target_path)
        variable_dict = variable.read_variable_json()
        # 获取当前语言环境
        lan = variable_dict['defaultLang']
        if lan is None or len(lan) == 0:
            message = ' 获取语言环境失败，无法继续'
            logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
            sys.exit(1)
        app_json = os.path.abspath(os.path.join(work_space_path, 'app', 'assets', 'app_factory', 'app', 'app.json'))
        android_config_data_json = os.path.abspath(
            os.path.join(work_space_path, 'app', 'assets', 'app_factory', lan, 'components',
                         'android_config_data.json'))
        android_config_data_keys = ['com.nd.sdp.component.android-capabilities', 'properties']
        if merge_json_file(json_path1=app_json,
                           json_path2=android_config_data_json,
                           key_list1=None,
                           key_list2=android_config_data_keys,
                           dest_json_path=app_json):
            logger.info(android_config_data_json + ' 的内容已经合并到 ' + app_json)
        else:
            message = android_config_data_json + ' 内容合并失败！ '
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, message)
    except BaseException as err:
        message = '提供安卓能力相关配置出现异常 ' + err.__str__()
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, message)
        sys.exit(1)
    else:
        logger.info(' 提供安卓能力相关配置过程没有发现异常')
    finally:
        logger.info(' 结束提供安卓能力相关配置')


def get_variables(work_space_path, want_key):
    """
    读取variables中配置
    :param work_space_path: 工作空间
    :param want_key:要获取变量中的key。
    :return:
    """
    if work_space_path is None or len(work_space_path) <= 0:
        print("[Error] android 构建传入工作空间路径为空")
        return None
    if want_key is None or len(want_key) <= 0:
        print("[Error] android 构建传入" + want_key + "是空")
        return None
    # 1 读取"target", "variables.json"配置的值
    # 取全局变量
    variables_path = os.path.join(work_space_path, "target", "variables.json")
    variables_dict = loader_json_file(variables_path)
    if variables_dict is not None and want_key in variables_dict:
        return variables_dict[want_key]
    else:
        return None


def provide_android_permission_to_assets(work_space_path):
    """
       把配置的高敏感权限内容permission_config_data.json从target下拷贝到assets下
       这样便于应用框架读取
    """
    logger.info(' 准备提供安卓高敏感权限的相关配置 ')
    if (work_space_path is None) or (len(work_space_path) == 0):
        message = '传入的工作空间地址是空，无法继续'
        logger.error(LoggerErrorEnum.REQUIRE_ARGUMENT, message)
        sys.exit(1)
    try:
        # 遍历语言环境
        language_json = get_variables(work_space_path, want_key='languages')
        if language_json is not None:
            for lang in language_json:
                language_name = str(lang)
                # 源文件
                src_android_permission_path = os.path.join(work_space_path,
                                                           "target",
                                                           "app_factory",
                                                           language_name,
                                                           "components",
                                                           "permission_config_data.json")
                # 目标文件
                dest_android_permission_path = os.path.join(work_space_path,
                                                            "app",
                                                            "assets",
                                                            "app_factory",
                                                            language_name,
                                                            "components",
                                                            "permission_config_data.json")
                if not copy_android_permission(src_android_permission_path, dest_android_permission_path):
                    logger.error(LoggerErrorEnum.FILE_NOT_EXIST, '新增高敏感权限功能，请重新保存编辑器配置后打包')
                    sys.exit(1)
    except Exception as err:
        message = '提供安卓高敏感权限的相关配置出现异常 ' + err.__str__()
        logger.error(LoggerErrorEnum.UNKNOWN_ERROR, message)
        sys.exit(1)
    else:
        logger.info('提供安卓高敏感权限的相关配置过程没有发现异常')
    finally:
        logger.info('结束提供提供安卓高敏感权限的相关配置')


def copy_android_permission(src_path, dest_path):
    if src_path is None or dest_path is None:
        logger.error(LoggerErrorEnum.INVALID_ARGUMENT, "文件路径不允许为空")
        return False
    if is_file_invalid(src_path):
        logger.error(LoggerErrorEnum.FILE_NOT_EXIST, src_path + "文件路径异常")
        return False
    permission_json = loader_json_file(src_path)
    if permission_json is not None and 'android' in permission_json:
        android_permission_json = permission_json['android']
        with open(dest_path, mode='w', encoding='utf-8') as outfile:
            json.dump(android_permission_json, outfile, ensure_ascii=False)
        return True
    return False
