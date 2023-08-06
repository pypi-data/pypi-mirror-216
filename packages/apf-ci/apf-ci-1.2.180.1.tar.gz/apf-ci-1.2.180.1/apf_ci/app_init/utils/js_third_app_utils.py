#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
app/js_third_app.json 相关操作

"""
from apf_ci.app_init.utils.build_config_utils import *


class JsThirdApp:
    def __init__(self, workspace_path):
        self.workspace_path = workspace_path
        self.app_path = os.path.join(self.workspace_path, 'app', 'assets', 'app_factory', "app")
        self.file_path = os.path.join(self.app_path, "js_third_app.json")

    def get_content(self):
        """
        下载js_third_app.json
        :return:
        """
        content_json = []
        config_josn_path = os.path.join(self.app_path, "config.json")
        config_content = read_file_content(config_josn_path)
        config_json = json.loads(config_content)

        appid = config_json.get("appid")
        if appid == '':
            return content_json

        domain_service = config_json["domain_service"]
        content_url = domain_service + "v1.0/jsfunctions/" + appid

        content_data = read_cs_content(content_url)
        if content_data:
            content = json.loads(content_data)
            content_json = content['items']
        return content_json

    def write_content(self, content_str):
        write_content_to_file(self.file_path, json.dumps(content_str, ensure_ascii=False))

    def read_content(self):
        if os.path.exists(self.file_path):
            variable_data = read_file_content(self.file_path)
            return json.loads(variable_data)


if __name__ == "__main__":
    #pass

    workspace_path = 'F://workplace//python//jenkins-plugin-python//tests'
    third_app = JsThirdApp(workspace_path)
    content = third_app.get_content()
    third_app.write_content(content)
    print(content)

