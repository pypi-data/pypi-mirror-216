"""
flutter android 构建模块
"""

__author__ = '961111'

from apf_ci.android.prepare.builder.generate_dependency_builder import *
from apf_ci.flutter.flutter_build import *
from apf_ci.flutter.flutter_command_utils import execute_command


class FlutterAndroidBuild(FlutterBuild):

    def build_backup(self):
        """
        android构建flutter（代码集成方式，已完善）
        :return:
        """
        logger.info("开始构建flutter android")
        workspace_path = os.getcwd()
        build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'build.gradle')
        build_gradle_content = read_file_content(build_gradle_path)
        # 替换android版本
        compile_sdk_version_pattern = re.compile(r'compileSdkVersion [0-9]*')
        compile_sdk_version_match = compile_sdk_version_pattern.search(build_gradle_content)
        if compile_sdk_version_match is not None:
            build_gradle_content = build_gradle_content.replace(compile_sdk_version_match.group(), 'compileSdkfluttVersion rootProject.compileSdkVersion')
        # 替换kotlin版本
        kotlin_version_pattern = re.compile(r'ext.kotlin_version = \'[0-9\.]*\'')
        kotlin_version_match = kotlin_version_pattern.search(build_gradle_content)
        if kotlin_version_match is not None:
            build_gradle_content = build_gradle_content.replace(kotlin_version_match.group(), "ext.kotlin_version = '1.3.40'")

        # 替换gradle版本
        gradle_version_pattern = re.compile(r'classpath \'com.android.tools.build:gradle:[0-9\.]*\'')
        gradle_version_match = gradle_version_pattern.search(build_gradle_content)
        if gradle_version_match is not None:
            gradle_version_replace = "Properties properties = new Properties()\n" \
                                     "        properties.load(project.rootProject.file('local.properties').newDataInputStream())\n" \
                                     "        def gradle_plugin_version = properties.getProperty('gradle_plugin_version')\n" \
                                     "        if(gradle_plugin_version == null || gradle_plugin_version.trim().isEmpty()){\n" \
                                     "            gradle_plugin_version = \"3.6.4\"\n" \
                                     "        }\n" \
                                     "        println ' -------------------------gradle_plugin_version ------------------------------------ is ' + gradle_plugin_version\n" \
                                     "        classpath 'com.android.tools.build:gradle:${gradle_plugin_version}'"
            build_gradle_content = build_gradle_content.replace(gradle_version_match.group(), gradle_version_replace)

        write_content_to_file(build_gradle_path, build_gradle_content)

        android_app_build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'app', 'build.gradle')
        android_app_build_gradle_content = read_file_content(android_app_build_gradle_path)
        # 替换android版本
        android_app_build_compile_sdk_version_pattern = re.compile(r'compileSdkVersion [0-9]*')
        android_app_build_compile_sdk_version_match = android_app_build_compile_sdk_version_pattern.search(android_app_build_gradle_content)
        if compile_sdk_version_match is not None:
            android_app_build_gradle_content = android_app_build_gradle_content.replace(android_app_build_compile_sdk_version_match.group(), 'compileSdkVersion rootProject.compileSdkVersion')

        # 替换target android版本
        android_app_build_target_sdk_version_pattern = re.compile(r'targetSdkVersion [0-9]*')
        android_app_build_target_sdk_version_match = android_app_build_target_sdk_version_pattern.search(android_app_build_gradle_content)
        if compile_sdk_version_match is not None:
            android_app_build_gradle_content = android_app_build_gradle_content.replace(android_app_build_target_sdk_version_match.group(), 'targetSdkVersion rootProject.compileSdkVersion')

        write_content_to_file(android_app_build_gradle_path, android_app_build_gradle_content)


        gradle_wrapper_path = os.path.join(self.flutter_template_path, '.android', 'gradle', 'wrapper', 'gradle-wrapper.properties')
        gradle_wrapper_content = read_file_content(gradle_wrapper_path)
        gradle_wrapper_pattern = re.compile(r'gradle-[0-9\.]*-all.zip')
        gradle_wrapper_match = gradle_wrapper_pattern.search(gradle_wrapper_content)
        if gradle_wrapper_match is not None:
            source_gradle_wrapper_path = os.path.join(workspace_path, 'gradle', 'wrapper', 'gradle-wrapper.properties')
            source_gradle_wrapper_content = read_file_content(source_gradle_wrapper_path)
            source_gradle_wrapper_pattern = re.compile(r'gradle-[0-9\.]*-all.zip')
            source_gradle_wrapper_match = source_gradle_wrapper_pattern.search(source_gradle_wrapper_content)
            if source_gradle_wrapper_match is not None:
                gradle_wrapper_content = gradle_wrapper_content.replace(gradle_wrapper_match.group(), source_gradle_wrapper_match.group())
                write_content_to_file(gradle_wrapper_path, gradle_wrapper_content)

        flutter_build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'Flutter', 'build.gradle')
        flutter_build_gradle_content = read_file_content(flutter_build_gradle_path)
        flutter_build_gradle_content = flutter_build_gradle_content.replace('flutter.compileSdkVersion', 'rootProject.compileSdkVersion')
        flutter_build_gradle_content = flutter_build_gradle_content.replace('flutter.targetSdkVersion', 'rootProject.compileSdkVersion')
        write_content_to_file(flutter_build_gradle_path, flutter_build_gradle_content)

        setting_gradle_path = os.path.join(workspace_path, 'settings.gradle')
        setting_gradle_content = read_file_content(setting_gradle_path)
        current_project_path = os.path.basename(workspace_path)
        include_flutter_groovy_path = os.path.join(current_project_path, 'flutter', '.android', 'include_flutter.groovy')
        setting_gradle_content += "\nsetBinding(new Binding([gradle: this]))\nevaluate(new File(settingsDir.parentFile, '" + include_flutter_groovy_path + "'))"
        write_content_to_file(setting_gradle_path, setting_gradle_content)

        app_build_gradle_path = os.path.join(workspace_path, 'app', 'app-factory-component.gradle')
        app_build_gradle_content = read_file_content(app_build_gradle_path)
        app_build_gradle_content = app_build_gradle_content.replace("dependencies{\nrepositories { flatDir { dirs './aars' } }", "dependencies{\nrepositories { flatDir { dirs './aars' } }\n    implementation project(':flutter')\n")
        write_content_to_file(app_build_gradle_path, app_build_gradle_content)

        logger.info("构建flutter android完成")

    def after_build(self):
        # 解析flutter插件依赖
        self.analyse_flutter_plugin_dependencies()
        # 重新生成app-factory-component.gradle
        self.regenerate_app_factory_gradle()
        # 替换gradle中的值
        self.replace_gradle()

    def build(self):
        """
        android构建flutter（aar方式集成，已完成）
        :return:
        """
        logger.info("开始构建flutter android")
        workspace_path = os.getcwd()

        # android_version = '28'
        # build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'build.gradle')
        # build_gradle_content = read_file_content(build_gradle_path)
        # # 替换android版本
        # compile_sdk_version_pattern = re.compile(r'compileSdkVersion [0-9]*')
        # compile_sdk_version_match = compile_sdk_version_pattern.search(build_gradle_content)
        # if compile_sdk_version_match is not None:
        #     build_gradle_content = build_gradle_content.replace(compile_sdk_version_match.group(),'compileSdkVersion ' + android_version)
        #
        # # 替换kotlin版本
        # kotlin_version_pattern = re.compile(r'ext.kotlin_version = \'[0-9\.]*\'')
        # kotlin_version_match = kotlin_version_pattern.search(build_gradle_content)
        # if kotlin_version_match is not None:
        #     build_gradle_content = build_gradle_content.replace(kotlin_version_match.group(), "ext.kotlin_version = '1.3.40'")
        #
        # # 替换gradle版本
        # gradle_version_pattern = re.compile(r'classpath \'com.android.tools.build:gradle:[0-9\.]*\'')
        # gradle_version_match = gradle_version_pattern.search(build_gradle_content)
        # if gradle_version_match is not None:
        #     gradle_version_replace = "classpath 'com.android.tools.build:gradle:3.6.4'"
        #     local_properties_path = os.path.join(workspace_path, 'local.properties')
        #     local_properties_content = read_file_content(local_properties_path)
        #     local_properties_pattern = re.compile(r'gradle_plugin_version=[0-9\.]*\'')
        #     local_properties_match = local_properties_pattern.search(local_properties_content)
        #     if local_properties_match is not None:
        #         gradle_version_replace = "classpath 'com.android.tools.build:gradle:" + local_properties_match.group().replace("gradle_plugin_version=", "") + "'"
        #     build_gradle_content = build_gradle_content.replace(gradle_version_match.group(), gradle_version_replace)
        #
        # write_content_to_file(build_gradle_path, build_gradle_content)
        #
        # # 替换gradle-wrapper
        # gradle_wrapper_path = os.path.join(self.flutter_template_path, '.android', 'gradle', 'wrapper', 'gradle-wrapper.properties')
        # gradle_wrapper_content = read_file_content(gradle_wrapper_path)
        # gradle_wrapper_pattern = re.compile(r'gradle-[0-9\.]*-all.zip')
        # gradle_wrapper_match = gradle_wrapper_pattern.search(gradle_wrapper_content)
        # if gradle_wrapper_match is not None:
        #     source_gradle_wrapper_path = os.path.join(workspace_path, 'gradle', 'wrapper', 'gradle-wrapper.properties')
        #     source_gradle_wrapper_content = read_file_content(source_gradle_wrapper_path)
        #     source_gradle_wrapper_pattern = re.compile(r'gradle-[0-9\.]*-all.zip')
        #     source_gradle_wrapper_match = source_gradle_wrapper_pattern.search(source_gradle_wrapper_content)
        #     if source_gradle_wrapper_match is not None:
        #         gradle_wrapper_content = gradle_wrapper_content.replace(gradle_wrapper_match.group(), source_gradle_wrapper_match.group())
        #         write_content_to_file(gradle_wrapper_path, gradle_wrapper_content)
        #
        # flutter_build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'Flutter', 'build.gradle')
        # flutter_build_gradle_content = read_file_content(flutter_build_gradle_path)
        # flutter_build_gradle_content = flutter_build_gradle_content.replace('flutter.compileSdkVersion', android_version)
        # flutter_build_gradle_content = flutter_build_gradle_content.replace('flutter.targetSdkVersion', android_version)
        # write_content_to_file(flutter_build_gradle_path, flutter_build_gradle_content)

        # build_gradle_path = os.path.join(self.flutter_template_path, '.android', 'build.gradle')
        # build_gradle_content = read_file_content(build_gradle_path)
        # build_gradle_replace = 'repositories {\n        maven {\n		    allowInsecureProtocol = true\n            name "nd nexus android-public"\n            url "http://nexus.sdp.nd/nexus/content/groups/android-public/"\n        }\n'
        # build_gradle_content = build_gradle_content.replace('repositories {', build_gradle_replace)
        # write_content_to_file(build_gradle_path, build_gradle_content)

        java_home_path = '/usr/java/jdk-11.0.18'
        gradle_property_path = os.path.join(self.flutter_template_path, '.android', 'gradle.properties')
        gradle_property_content = read_file_content(gradle_property_path)
        # 替换android版本
        gradle_property_content = gradle_property_content + '\norg.gradle.java.home=' + java_home_path
        write_content_to_file(gradle_property_path, gradle_property_content)

        execute_command([self.flutter_command, 'build', 'aar', '--no-debug', '--no-profile'], chdir=self.flutter_template_path)
        logger.info("构建flutter android完成")

        # 自动扫描打包产物aar列表
        flutter_plugin_source_path = os.path.join(self.flutter_template_path, 'build', 'host', 'outputs', 'repo')
        for root, dirs, files in os.walk(flutter_plugin_source_path):
            for name in files:
                # 2023.03.06 由于Flutter SDK不同版本产物目录结构不同，产物名也不同，故需要对此进行改造
                # 例:
                # Flutter SDK 3.3.7 会生成outputs/flutter/1.0/flutter-1.0-release.aar与outputs/flutter_release/1.0/flutter_release-1.0.aar
                # Flutter SDK 3.7.4 只会生成outputs/flutter/1.0/flutter-1.0.aar
                if name.endswith('.aar'):
                    # 对产物目录进行解析，只获取路径中以_release结尾的产物文件
                    root_split = os.path.split(root)
                    if root_split[root_split.__len__() - 2].endswith('_release'):
                        flutter_plugin_path = os.path.join(root, name)
                        target_plugin_path = os.path.join(workspace_path, 'app', 'libs', name)
                        copy_file(flutter_plugin_path, target_plugin_path)
                        target_plugin_path = os.path.join(workspace_path, 'flutter', 'caches', name)
                        copy_file(flutter_plugin_path, target_plugin_path)

    def regenerate_app_factory_gradle(self):
        """
        flutter产物构建完成后，重写app-factory-component.gradle文件
        :return:
        """
        # 取全局变量
        workspace = os.getcwd()
        variables_path = os.path.join(workspace, "target", "variables.json")
        variables_content = read_file_content(variables_path)
        variables_dict = json.loads(variables_content)
        factory_id = variables_dict["factoryId"]

        # do generate dependency
        generate_dependency_builder = GenerateDependencyBuilder(factory_id, variables_dict)

        groovy_strbuffer = ""
        dependency_strbuffer = "dependencies{\nrepositories { flatDir { dirs './aars' } }\n"
        # 获取defines.json文件内容
        defines_path = os.path.join(os.getcwd(), "target/defines.json")
        defines_content_str = read_file_content(defines_path)
        defines_json_dict = json.loads(defines_content_str)
        # 获取dependencyFinal.txt文件内容
        dependency_final_path = os.path.join(os.getcwd(), "target/dependencyFinal.txt")
        dependency_final_content_str = read_file_content(dependency_final_path)
        dependency_json_list = json.loads(dependency_final_content_str)

        biz_comp_xml_map = {}
        try:
            generate_dependency_builder._init_biz_comp_xml_map(defines_json_dict, biz_comp_xml_map)
        except Exception as e:
            logger.warning("解析各组件xml失败 %s" % e)
            traceback.print_exc()

        # 解析相关的main
        for dependency_element in dependency_json_list:
            if isinstance(dependency_element, dict):
                component = dependency_element.get("component", {})
                namespace = component.get("namespace", "")
                name = component.get("name", "")

                define_str = biz_comp_xml_map.get(namespace + ":" + name)
                if not isinstance(define_str, str):
                    logger.warning("查找不到对应的组件定义：" + namespace + ":" + name)
                define_dict = json.loads(define_str)
                types = define_dict.get("types", "")
                if types:
                    native_android = types.get("native-android", {})
                    if native_android:
                        dependency_strbuffer += native_android.get("dependency", "")
                        dependency_strbuffer += "\n"

                        groovy_strbuffer += native_android.get("groovy", "")
                        groovy_strbuffer += "\n"

        # add subapp dependencies
        subapp_dependency_json = generate_dependency_builder._get_subapp_dependencies(variables_dict["app_native_storage"])
        dependency_strbuffer += subapp_dependency_json["dependency"]
        dependency_strbuffer += "}"

        groovy_strbuffer += subapp_dependency_json["groovy"]
        dependency_strbuffer += groovy_strbuffer

        # dependency内容写入 app-factory-component.gradle
        gradle_path = os.path.join(os.getcwd(), "app/app-factory-component.gradle")
        write_content_to_file(gradle_path, dependency_strbuffer)

    def analyse_flutter_plugin_dependencies(self):
        """
        解析flutter插件中的依赖
        :return:
        """
        # 获取flutter构建产物中的依赖
        logger.info("开始flutter android plugin依赖解析")
        workspace_path = os.getcwd()
        build_config_path = os.path.join(workspace_path, 'target', 'build_config.json')
        build_config_content = read_file_content(build_config_path)
        build_config_json = json.loads(build_config_content)
        flutter_plugins_dependencies_exclude_array = build_config_json['flutter_android_plugin_dependencies_exclude']

        flutter_plugins_dependencies_path = os.path.join(self.flutter_template_path, '.flutter-plugins-dependencies')
        flutter_plugins_dependencies_content = read_file_content(flutter_plugins_dependencies_path)
        flutter_plugins_dependencies_json = json.loads(flutter_plugins_dependencies_content)
        dependencies_array = []
        for plugin in flutter_plugins_dependencies_json['plugins']['android']:
            # 获取依赖列表
            path = os.path.join(plugin['path'], 'android', 'build.gradle')
            name = plugin['name']
            dependencies_array = dependencies_array + self.analyse_flutter_plugin_build_gradle(path, name, flutter_plugins_dependencies_exclude_array)

        # 合并依赖
        final_dependencies_content = "\t// 此处开始为Flutter插件中的依赖\n"
        for item in dependencies_array:
            final_dependencies_content = final_dependencies_content + "\t" + item + "\n"
        final_dependencies_content = final_dependencies_content + "\n\t// Flutter插件依赖到此结束"

        # 依赖写入defines.json
        defines_path = os.path.join(os.getcwd(), 'target', 'defines.json')
        defines_content_str = read_file_content(defines_path)
        defines_json_dict = json.loads(defines_content_str)
        for define_key in defines_json_dict:
            if define_key.startswith('com.nd.sdp.component:flutter-runtime'):
                element = defines_json_dict[define_key]
                types = element['types']
                native_android = types['native-android']
                dependency = native_android['dependency']
                native_android['dependency'] = dependency + final_dependencies_content
                break
        write_content_to_file(defines_path, json.dumps(defines_json_dict))

        # 依赖写入xml
        xml_path = os.path.join(workspace_path, 'target', 'xmls_old.xml')
        xml_content = read_file_content(xml_path)
        xml_arrays = xml_content.splitlines()
        old_xml_content = ""
        new_xml_content = ""
        read_xml = False
        insert_dependency = True
        index = 0
        for xml_line in xml_arrays:
            if xml_line.__contains__('<component') \
                    and xml_line.__contains__('namespace="com.nd.sdp.component"') \
                    and xml_line.__contains__('name="flutter-runtime"'):
                # 若找到Flutter运行框架，则进行替换
                read_xml = True
                old_xml_content = old_xml_content + xml_line
                new_xml_content = new_xml_content + "\n" + xml_line
                continue
            if read_xml:
                # 读取Flutter运行框架的xml
                old_xml_content = old_xml_content + "\n" + xml_line
                if xml_line.__contains__('<android>'):
                    index = index + 1
                if xml_line.__contains__('<dependency>'):
                    index = index + 1
                if xml_line.__contains__('<![CDATA['):
                    index = index + 1
                new_xml_content = new_xml_content + "\n" + xml_line
                if index == 3:
                    # 将Flutter插件中的依赖加入Flutter运行框架中
                    if insert_dependency:
                        new_xml_content = new_xml_content + "\n" + final_dependencies_content
                        index = 0
                        insert_dependency = False
                if xml_line.strip().startswith('</component>'):
                    # 若解析到Flutter运行框架结束，则直接跳出
                    break

        xml_content = xml_content.replace(old_xml_content, new_xml_content)
        write_content_to_file(xml_path, xml_content)

    def analyse_flutter_plugin_build_gradle(self, build_gradle_path, plugin_name, exclude_array):
        """
        解析flutter插件中build.gradle的依赖信息
        :param build_gradle_path:
        :param plugin_name:
        :param exclude_array:
        :return:
        """
        build_gradle_content = read_file_content(build_gradle_path)
        arrays = build_gradle_content.splitlines()
        plugin_detail = "// plugin: " + plugin_name
        final_array = [plugin_detail]
        plugin_params = {}
        read_dependencies = False
        start_index = 0
        for item in arrays:
            final_item = item.strip()
            if final_item.startswith('def'):
                # 若该行为声明变量，则加入到变量列表中以供后续替换
                param_line = final_item.replace('def', '')
                param_split = param_line.split('=')
                if len(param_split) >= 2:
                    key = param_split[0].strip()
                    value = param_split[1].strip().replace('"', '').replace("'", "")
                    plugin_params[key] = value
            if final_item == 'dependencies {':
                # 若匹配到dependencies，则开始读取依赖，游标归零
                read_dependencies = True
                start_index = 0
                continue
            if final_item == '{' or final_item.endswith('{'):
                # 若匹配到{ ，游标+1
                start_index = start_index + 1
            if final_item == '}':
                # 若匹配到 }，游标-1
                start_index = start_index - 1
                if start_index < 0:
                    # 若此时游标<0，则意味着游标已经超出dependencies范围，停止读取依赖
                    read_dependencies = False
                if read_dependencies:
                    # 若此时仍处于可读状态，将 } 加入依赖列表中（兼容依赖中带{}的情况）
                    final_array.append(final_item)
                    continue

            if read_dependencies:
                if start_index > 0:
                    # 若标记为可读，且游标处于dependencies范围内，则直接加入列表中（兼容依赖中带{}的情况）
                    final_array.append(final_item)
                    continue

                if final_item.startswith('implementation') or final_item.startswith('compile') or final_item.startswith(
                        'api'):
                    check = False
                    if final_item.__contains__('project('):
                        # 过滤掉依赖中含有project()的情况
                        check = True
                    if not check:
                        # 根据白名单包列表进行过滤
                        for exclude in exclude_array:
                            if final_item.__contains__(exclude):
                                check = True
                                break
                    if not check:
                        # 加入依赖
                        final_array.append(final_item)

        # 替换参数
        if len(plugin_params) > 0:
            final_replaced_array = []
            for param in plugin_params:
                for item in final_array:
                    if item.__contains__('${' + param + '}'):
                        replaced_item = item.replace('${' + param + '}', plugin_params[param])
                    elif item.__contains__('$' + param):
                        replaced_item = item.replace('$' + param, plugin_params[param])
                    else:
                        replaced_item = item
                    final_replaced_array.append(replaced_item)
            return final_replaced_array
        else:
            return final_array

    def replace_gradle(self):
        """
        替换一些依赖包
        :return:
        """
        workspace_path = os.getcwd()
        aar_name_list = []
        libs_path = os.path.join(workspace_path, 'app', 'libs')
        for root, dirs, files in os.walk(libs_path):
            for name in files:
                if name.endswith('.aar'):
                    aar_name_list.append(name.replace('.aar', ''))

        app_factory_component_gradle_path = os.path.join(workspace_path, 'app/app-factory-component.gradle')
        app_factory_component_gradle_content = read_file_content(app_factory_component_gradle_path)
        app_factory_component_gradle_replace_content = "repositories { flatDir { dirs './aars', 'libs' } }\n"
        # 获取flutter引擎版本
        flutter_sdk_home, flutter_command_file = os.path.split(self.flutter_command)
        flutter_engine_version_path = os.path.join(flutter_sdk_home, 'internal', 'engine.version')
        flutter_engine_version = read_file_content(flutter_engine_version_path)
        flutter_engine_version = flutter_engine_version.strip()
        # 遍历aar列表并写入
        for aar_name in aar_name_list:
            app_factory_component_gradle_replace_content += "    implementation(name:'" + aar_name + "', ext:'aar')\n"
        app_factory_component_gradle_replace_content += "    implementation \"io.flutter:flutter_embedding_release:1.0.0-" + flutter_engine_version + "\"\n"
        app_factory_component_gradle_replace_content += "    implementation \"io.flutter:armeabi_v7a_release:1.0.0-" + flutter_engine_version + "\"\n"
        app_factory_component_gradle_replace_content += "    implementation \"io.flutter:arm64_v8a_release:1.0.0-" + flutter_engine_version + "\"\n"
        app_factory_component_gradle_replace_content += "    implementation \"androidx.activity:activity:1.0.0\"\n"

        app_factory_component_gradle_content = app_factory_component_gradle_content.replace("repositories { flatDir { dirs './aars' } }", app_factory_component_gradle_replace_content)
        write_content_to_file(app_factory_component_gradle_path, app_factory_component_gradle_content)

        project_build_gradle_path = os.path.join(workspace_path, 'build.gradle')
        project_build_gradle_content = read_file_content(project_build_gradle_path)
        project_build_gradle_replace_content = "allprojects {\n    repositories {\n        maven {  url \"https://storage.flutter-io.cn/download.flutter.io\"}\n"
        project_build_gradle_content = project_build_gradle_content.replace("allprojects {\n    repositories {", project_build_gradle_replace_content)
        write_content_to_file(project_build_gradle_path, project_build_gradle_content)

    def generate_cache(self):
        cache_path = os.path.join(self.flutter_template_path, 'caches')
        zip_name = 'android_aar.zip'
        zip_path = os.path.join(self.flutter_template_path, zip_name)

        zipDir(cache_path, zip_path)

        # 保存二级缓存
        self.generate_second_level_cache(zip_name, zip_path)

        # 保存一级缓存
        self.generate_first_level_cache(zip_name, zip_path)

        # 保存md5文件
        self.generate_md5_json()

    def get_cache(self):
        logger.info("开始拉取缓存文件")
        workspace_path = os.getcwd()

        check_md5 = self.check_use_cache()
        if not check_md5:
            return False

        zip_name = 'android_aar.zip'
        zip_path = os.path.join(self.flutter_template_path, 'caches',
                                zip_name)
        # 从一级缓存中获取
        first_level_cache_exits = self.get_first_level_cache(zip_name, zip_path)
        if not first_level_cache_exits:
            # 从二级缓存中获取
            second_level_cache_exits = self.get_second_level_cache(zip_name, zip_path)
            if not second_level_cache_exits:
                return False

            logger.info("获取到二级缓存文件")
            # 将二级缓存中的文件复制到一级缓存中
            self.generate_first_level_cache(zip_name, zip_path)
        else:
            logger.info("获取到一级缓存文件")

        unzip_path = os.path.join(workspace_path, 'app', 'libs')
        unzip(zip_path, unzip_path)
        return True

