#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.app_compare.build.app_compare import main as app_compare

#  用于本地测试脚本，这里用于备份，不在这里运行，因为初始化文件夹下所有文件
class ArgDict():
    pass



def getparam():
    variable_dict = ArgDict()
    variable_dict.packageOld = 'http://portal.s3.nds.sdp/release_app_fac_dysm/android/com.nd.sdp.component.debug4.apfc_fuabre/apfc_fuabre/preproduction/apfc_fuabre_3407481.apk'
    variable_dict.packageNew = 'http://portal.s3.nds.sdp/release_app_fac_dysm/android/com.nd.sdp.component.debug4.apfc_fuabre/apfc_fuabre/preproduction/apfc_fuabre_3408928.apk'
    variable_dict.appCompareId = "5ea8298f857b360010465942"
    variable_dict.envJenkins = "2"
    variable_dict.appType = "android"
    variable_dict.isLocal = "true"


def getparam2():
    variable_dict = ArgDict()
    variable_dict.packageOld = 'https://gcdncs.101.com/v0.1/static/release_package_repository/android/com.nd.app.factory.egyptofficialim/EgyptOfficialIM/aws-california/EgyptOfficialIM_3528206.apk'
    variable_dict.packageNew = 'https://gcdncs.101.com/v0.1/static/release_package_repository/android/com.nd.app.factory.egyptofficialim/EgyptOfficialIM/aws-california/EgyptOfficialIM_3528378.apk'
    variable_dict.appCompareId = "5f460232139e320010cfed01"
    variable_dict.envJenkins = "8"
    variable_dict.appType = "android"
    variable_dict.isLocal = "true"

    return variable_dict

def getparam3():
    variable_dict = ArgDict()
    variable_dict.packageOld = 'https://gcdncs.101.com/v0.1/static/test_package_repository/ios/com.nd.app.factory.testforsign2/ap1591349307097/test/ap1591349307097_3567344.ipa'
    variable_dict.packageNew = 'https://gcdncs.101.com/v0.1/static/test_package_repository/ios/com.nd.app.factory.testforsign2/ap1591349307097/test/ap1591349307097_3567354.ipa'
    variable_dict.appCompareId = "5faa5f75e591dc0010951600"
    variable_dict.envJenkins = "2"
    variable_dict.appType = "ios"
    variable_dict.isLocal = "true"

    return variable_dict

if __name__ == '__main__':
    variable_dict = getparam3()
    app_compare(variable_dict)
    #tab_build()


