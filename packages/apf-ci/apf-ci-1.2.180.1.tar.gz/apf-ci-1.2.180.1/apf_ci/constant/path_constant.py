#!/usr/bin/python3
# -*- coding: utf-8 -*-

class PathConstant:
    ANDROID_RES_DIST = "dist/{PAGE_NAME}/dist/android/res"
    IOS_ASSETS_DIST = "dist/{PAGE_NAME}/dist/iOS/assets"

    ANDROID_I18N_DIST = "dist/{PAGE_NAME}/dist/android/i18n"
    IOS_I18N_DIST = "dist/{PAGE_NAME}/dist/iOS/i18n"

    ANDROID_I18N = "android/i18n"
    IOS_I18N = "iOS/i18n"
    REACT_WIDGET = "target/react_widget"
    PACKAGE_JSON_FILE = "target/react_widget/package.json"
    SKIN_PATH = "target/react_widget/{PLUGIN_ID_DIR}/skin"

    # package.json构建文件中pages-->uri值前缀
    URI_PREFIX = "react://com.nd.apf.react.native.widget"
    WIDGET_NAMESPACE_BIZNAME = "com.nd.apf.react.native:widget"
    WIDGET_BIZNAME = "widget"
    WIDGET_NAMESPACE = "com.nd.apf.react.native"

    TARGET_PAGES_FILE_PATH = "target/app_component_pages/${TAG_LANGUAGE}/pages.json"
    TARGET_WIDGETS_FILE_PATH = "target/app_component_pages/${TAG_LANGUAGE}/widgets.json"

    CONFIG_JSON_FILE = "app/assets/app_factory/app/config.json"
    DEFINES_JSON_FILE = "target/defines.json"
    BUILD_CONFIG_PATH = "target/build_config.json"
    MOUDLE_PACKAGE_JSON_FILE = "target/react_widget/{PLUGIN_ID_DIR}/{TAG_MOUDLE}/package.json"
    MOUDLE_PAGES_JSON_FILE = "target/react_widget/{PLUGIN_ID_DIR}/{TAG_MOUDLE}/page.json"
    MOUDLE_SKIN_FOLDER = "target/react_widget/{PLUGIN_ID_DIR}/{TAG_MOUDLE}/skin"
    MOUDLE_ANDROID_I18N_DIST = "{TAG_MOUDLE}/dist/{TAG_MOUDLE}/dist/android/i18n"
    MOUDLE_IOS_I18N_DIST = "{TAG_MOUDLE}/dist/{TAG_MOUDLE}/dist/iOS/i18n"

    PLUGIN_WIDGET_NAMESPACE = "com.nd.sdp.plugin"
