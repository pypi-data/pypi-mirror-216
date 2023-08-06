# /usr/bin/python3
# -*- coding: utf-8 -*-


# 获取ios最低支持版本，如果编辑器配置存在，且大于最低版本，使用编辑器配置，否则使用默认版本
def get_min_version_ios(build_config_json, version_min_sdk):
    ios_version_min_sdk_default = build_config_json.get("ios_version_min_sdk_default")
    if not version_min_sdk or not compare(version_min_sdk, ios_version_min_sdk_default):
        return ios_version_min_sdk_default
    return version_min_sdk

# 获取android最低支持版本，如果编辑器配置存在，且大于最低版本，使用编辑器配置，否则使用默认版本
def get_min_version_android(build_config_json, version_min_sdk):
    version_min_sdk_default = build_config_json.get("android_version_min_sdk_default")
    version_default = build_config_json.get("android_version_default")
    print("version_min_sdk:"+version_min_sdk)
    print("version_default:"+version_default)
    print("version_min_sdk_default:"+version_min_sdk_default)
    if not version_min_sdk or version_min_sdk == "":
        return version_default
    if not compare(version_min_sdk, version_min_sdk_default):
        return version_min_sdk_default
    return version_min_sdk

def get_target_version_android(build_config_json, version_target_sdk):
    android_target_version_default = build_config_json.get("android_target_version_default")
    print("android_target_version_default:"+android_target_version_default)
    if not compare(version_target_sdk, android_target_version_default):
        return android_target_version_default
    return version_target_sdk

# 如果 a_version 大于 b_version 返回True 否则返回False
def compare(a_version, b_version):
    if not a_version or not b_version or a_version == '' or b_version == '':
        return False
    la = a_version.split('.')
    lb = b_version.split('.')
    f = 0
    if len(la) > len(lb):
        f = len(la)
    else:
        f = len(lb)
    for i in range(f):
        try:
            if int(la[i]) > int(lb[i]):
                return True
            elif int(la[i]) == int(lb[i]):
                continue
            else:
                return False
        except IndexError as e:
            if len(la) > len(lb):
                return True
            else:
                return False
    return False