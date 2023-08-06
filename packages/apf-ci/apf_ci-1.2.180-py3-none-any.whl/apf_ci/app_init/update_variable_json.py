#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
更新 target/variable.json文件
"""
from  apf_ci.app_init.utils import *
from  apf_ci.app_init.utils.appinfo_utils import AppInfo

__author__ = '370418'


def get_versionInfo(env_jenkins, is_local):
    version_info = envs_value('versionInfo', env_jenkins, is_local)
    ## 本地测试数据
    #if (version_info == '' and is_local):
    #    version_info_json ={"app":{"chinese_name":"testforsign2","ico_url":"http://cs.101.com/v0.1/static/biz_comp_mng/default-icon/icon.png","launchImg":"http://gcdncs.101.com/v0.1/static/portal_app_skin/640-960.png","welcomeImg":"http://gcdncs.101.com/v0.1/static/portal_app_skin/1242-2208.png","name":"ap1591349307097","package_name_android":"com.nd.app.factory.testforsign2","launchImgByAndroid":"http://gcdncs.101.com/v0.1/static/portal_app_skin/1080-1920-new.9.png","oid":"6e508e37-c5ee-4854-ba6d-ac4b7382631e","package_name_ios":"com.nd.app.factory.testforsign2","trial_period":30,"build_type":"production"},"version":{"publisher_id":"","app_name":"ap1591349307097","version_white_name":[],"version_name":"0.0.8","version_desc":"0.0.8","create_time":1618800367496,"oid":"607ceeefdbfcb20010943c51","app_id":"6e508e37-c5ee-4854-ba6d-ac4b7382631e"}}
    #    version_info = json.dumps(version_info_json)
    return version_info


def get_gradel_home(env_jenkins, is_local=False):
    gradle_home_str = ''

    workspace_path = os.getcwd()
    pro_file = open(workspace_path + '/gradle/wrapper/gradle-wrapper.properties', 'r')
    for line in pro_file.readlines():
        line = line.strip().replace('\n', '')
        if line.find('#') == -1 and line.find('=') > 0:
            strs = line.split('=')
            if strs[0].strip() == 'distributionUrl':
                strs[1] = line[len(strs[0]) + 1:]
                gradle_home_str = strs[1].strip().replace('https\://', 'https://')
    pro_file.close()

    if gradle_home_str:
        gradle_home_final = envs_value(gradle_home_str, env_jenkins, is_local)
        if gradle_home_final:
            if not os.path.exists(gradle_home_final):
                gradle_home_str = 'GRADLE_HOME_SHELL'
        else:
            gradle_home_str = 'GRADLE_HOME_SHELL'
    else:
        gradle_home_str = 'GRADLE_HOME_SHELL'

    return gradle_home_str


def init_gradle_home(variable_dict):
    app_type = variable_dict['build_app_type']
    env_jenkins = variable_dict['envJenkins']
    is_local = variable_dict['is_local']
    gradle_home = ''
    if app_type.lower() == 'android':
        gradle_home = get_gradel_home(env_jenkins, is_local)
    variable_dict['gradleHome'] = gradle_home


def update_variable_json(variable_dict):
    target_path = variable_dict['target_path']
    envtarget = variable_dict['envtarget']
    env_jenkins = variable_dict['envJenkins']
    is_local = variable_dict['is_local']
    version_id = variable_dict['versionId']
    portal_host = variable_dict['app_protal']
    version2_app_factory = variable_dict['version2AppFactory']
    storage_host = variable_dict['app_native_storage']
    portal_host = variable_dict['app_protal']
    factory_id = variable_dict['factoryId']
    app_type = variable_dict['build_app_type']

    result_json = {}
    PACKAGE_NAME_ANDROID = ''
    PACKAGE_NAME_IOS = ''
    CHINESE_NAME = ''
    VERSION_NAME = ''
    VERSION_DESC = ''
    APP_NAME = ''

    force = envs_value('force', env_jenkins, is_local)
    logger.debug(" force: %s" % force)

    version_info = get_versionInfo(env_jenkins, is_local)
    logger.debug(" versionInfo: %s" % version_info)

    variable_dict_string = ', '.join([f"{key}: {value}" for key, value in variable_dict.items()])
    logger.info(" variable_dict %s" % variable_dict_string)

    if version_info:
        result_json = json.loads(version_info)

        PACKAGE_NAME_ANDROID = 'package_name_android'
        PACKAGE_NAME_IOS = 'package_name_ios'
        CHINESE_NAME = 'chinese_name'
        VERSION_NAME = 'version_name'
        VERSION_DESC = 'version_desc'
        APP_NAME = 'app_name'
    else:
        if version_id:
            portal_info_url = "%s/third/info/%s" % (portal_host, version_id)
            if version2_app_factory:
                portal_info_url = version2_app_factory + version_id

            result_json = get_data(portal_info_url)
            logger.info('portal_info_url = %s' % portal_info_url)
            logger.info('portal_info_url result_json = %s' % result_json)
            try:
                error_msg = "%s " % result_json['message']
                logger.error(LoggerErrorEnum.JENKINS_BUILD_ERROR_000001, error_msg)
                raise Exception()
                sys.exit(1)
            except KeyError:
                pass
        else:
            result_json = ''

        PACKAGE_NAME_ANDROID = 'packageName'
        PACKAGE_NAME_IOS = 'packageNameIOS'
        CHINESE_NAME = 'chineseName'
        VERSION_NAME = 'versionName'
        VERSION_DESC = 'versionDesc'
        APP_NAME = 'appName'

    com_test_type = ''
    build_type = ''

    if result_json:
        app_json = result_json['app']

        type_value = ''
        try:
            type_value = app_json['type']
        except KeyError:
            pass

        logger.debug(" app type: %s (11--biz_component_fun_test, 12--biz_component_com_test)" % type_value)

        if type_value == 11 or type_value == 12:
            com_test_type = app_json['comTestType']

        #app_info_url = "%s/v0.8/appinfo/%s" % (storage_host, factory_id)
        #app_info_json = get_data(app_info_url)
        app_info = AppInfo(target_path)
        app_info_json = app_info.get_app_info(storage_host, factory_id)
        # 这里git clone 没完成，不能写入文件
        #app_info.write_app_info(app_info_json)
        try:
            error_msg = "[ERROR] %s " % app_info_json['message']
            logger.error(LoggerErrorEnum.UNKNOWN_ERROR, error_msg)
            raise Exception(error_msg)
        except KeyError:
            pass

        icon_url = ''
        try:
            if app_info_json['icon'] and app_info_json['icon'].find('../') == -1:
                icon_url = app_info_json['icon']
        except KeyError:
            icon_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/app.png'

        if icon_url == '' or icon_url == None:
            icon_url = 'http://cdncs.101.com/v0.1/static/sdp_nd/portal/app.png'

        factory_app_type = 'main'
        try:
            if app_info_json['app_type']:
                factory_app_type = app_info_json['app_type']
        except KeyError:
            pass
        logger.debug(" 应用主子类型factoryAppType: %s" % factory_app_type)
        variable_dict['factoryAppType'] = factory_app_type

        package_name = ''
        package_name_str = ''
        if app_type.lower() == 'android':

            android_icon = app_info_json['android_icon']
            if android_icon:
                icon_url = android_icon

            package_name = app_info_json['package_name']
            package_name_str = PACKAGE_NAME_ANDROID

            try:
                launch_image_android = {}
                launch_image_android = app_info_json['launch_image']['android']
                if launch_image_android['default'] is None or launch_image_android['default'] == '':
                    launch_image_android[
                        'default'] = 'http://cdncs.101.com/v0.1/static/app_factorty_config/app_factory_config/android_launch.9.png'
            except KeyError:
                launch_image_android[
                    'default'] = 'http://cdncs.101.com/v0.1/static/app_factorty_config/app_factory_config/android_launch.9.png'

            logger.debug(" launch_image_android: %s" % json.dumps(launch_image_android))
            variable_dict['launch_image_android'] = launch_image_android

        elif app_type.lower() == 'ios':

            ios_icon = app_info_json['ios_icon']
            if ios_icon:
                icon_url = ios_icon

            package_name = app_info_json['package_name_ios']
            package_name_str = PACKAGE_NAME_IOS
            launch_image_ios = app_info_json['launch_image']['ios']
            try:
                #launch_small_url = app_info_json['ios5_image']
                launch_small_url = launch_image_ios['default']
            except KeyError:
                launch_small_url = ''

            if launch_small_url == '' or launch_small_url == None:
                launch_small_url = ''
            print("[INFO] 启动小图标: %s" % launch_small_url)
            variable_dict['smallLaunchImg'] = launch_small_url


            try:
                #launch_big_url = app_info_json['ios6_image']
                launch_big_url = launch_image_ios['iPhone6P']
            except KeyError:
                launch_big_url = ''

            if launch_big_url == '' or launch_big_url == None:
                launch_big_url = ''
            print("[INFO] 启动大图标: %s" % launch_big_url)
            variable_dict['bigLaunchImg'] = launch_big_url

            try:
                #pad_launch_big_url = app_info_json['ios_pad_image']
                pad_launch_big_url = launch_image_ios['iPad_portrait']
            except KeyError:
                pad_launch_big_url = ''

            if pad_launch_big_url == '' or pad_launch_big_url == None:
                pad_launch_big_url = ''
            print("[INFO] pad横屏启动大图标: %s" % pad_launch_big_url)
            variable_dict['padLaunchImg'] = pad_launch_big_url

            try:
                #pad_landscape_launch_img = app_info_json['ios_pad_landscape_image']
                pad_landscape_launch_img = launch_image_ios['iPad_landscape']
            except KeyError:
                pad_landscape_launch_img = ''

            if pad_landscape_launch_img == '' or pad_landscape_launch_img == None:
                pad_landscape_launch_img = ''
            print("[INFO] pad竖屏启动大图标: %s" % pad_landscape_launch_img)
            variable_dict['padLandscapeLaunchImg'] = pad_landscape_launch_img

            try:
                iphonex_launch_img = app_info_json['ios10_image']
                iphonex_launch_img = launch_image_ios['iPhoneXSMax']
            except KeyError:
                iphonex_launch_img = ''

            if iphonex_launch_img == '' or iphonex_launch_img == None:
                iphonex_launch_img = ''
            print("[INFO] iPhoneX启动图标: %s" % iphonex_launch_img)
            variable_dict['iPhoneXLaunchImg'] = iphonex_launch_img

            variable_dict['build_icon_64'] = os.path.join(os.getcwd(), 'target/temp/AppIcon64.png')
            variable_dict['build_icon_128'] = os.path.join(os.getcwd(), 'target/temp/AppIcon128.png')

        print("[INFO] icon_url: %s" % icon_url)
        variable_dict['build_app_icon'] = icon_url

        if package_name == '':
            try:
                package_name = app_json[package_name_str]
            except KeyError:
                package_name = 'com.nd.app.factory.app' + app_json['name'].replace('-', '')

            if package_name == '' or package_name == None:
                package_name = 'com.nd.app.factory.app' + app_json['name'].replace('-', '')

        print("[INFO] package_name: %s" % package_name)
        variable_dict['build_package'] = package_name

        try:
            label = app_json[CHINESE_NAME]
        except KeyError:
            label = app_json['name']

        if label == '' or label == None:
            label = app_json['name']
        print("[INFO] label: %s" % label)
        variable_dict['build_app_label'] = label

        version_json = result_json['version']

        version_name = ''
        try:
            version_name = version_json[VERSION_NAME]
        except KeyError:
            pass
        print("[INFO] version_name: %s" % version_name)
        variable_dict['build_version_label'] = version_name

        version_description = ''
        try:
            version_description = version_json[VERSION_DESC]
        except KeyError:
            pass
        print("[INFO] version_description: %s" % version_description)
        variable_dict['build_version_description'] = version_description

        build_multi_channel = ''
        try:
            build_multi_channel = version_json['build_multi_channel']
        except KeyError:
            pass
        print("[INFO] build_multi_channel: %s" % build_multi_channel)
        variable_dict['build_multi_channel'] = build_multi_channel

        version_white_name = ''
        try:
            version_white_name = ','.join(version_json['version_white_name'])
        except KeyError:
            pass
        print("[INFO] version_white_name: %s" % version_white_name)
        variable_dict['versionWhiteName'] = version_white_name

        env_client = 'dev'
        try:
            env_type = version_json['envType']
            if env_type == '8':
                env_client = 'release'
            elif env_type == '10':
                env_client = 'aws'
            elif env_type == '16':
                env_client = 'party'
        except KeyError:
            pass
        print("[INFO] env_client: %s" % env_client)
        variable_dict['env_client'] = env_client

        app_name = ''
        try:
            app_name = version_json[APP_NAME]
        except KeyError:
            pass
        print("[INFO] app_name: %s" % app_name)
        variable_dict['build_app_name'] = app_name

        try:
            build_type = app_json['buildType']
        except KeyError:
            pass

        try:
            trial_period = app_json['trial_period']
        except KeyError:
            trial_period = '0'
        print("[INFO] 试用期（企业门户应用）trial_period: %s" % trial_period)
        variable_dict['trial_period'] = trial_period

        oid = ''
        try:
            oid = app_json['oid']
        except KeyError:
            pass
        print("[INFO] oid: %s" % oid)
        variable_dict['build_app_id'] = oid

    print("[INFO] com_test_type: %s" % com_test_type)
    variable_dict['comTestType'] = com_test_type

    print("[INFO] 应用版本（企业门户应用）buildType: %s" % build_type)
    variable_dict['build_type'] = build_type

    if envtarget.lower() == 'aws-california-wx':
        envtarget = 'aws-california'
    variable_dict['env_target'] = envtarget


