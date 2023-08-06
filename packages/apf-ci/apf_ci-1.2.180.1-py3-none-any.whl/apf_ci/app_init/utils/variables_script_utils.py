
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
target/variables_script.json 相关操作

"""
from apf_ci.app_init.utils.build_config_utils import *
from apf_ci.app_init.utils.language_utils import logger

class VariableScript:
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_path = os.path.join(target_path, 'variables_script.json')

    def read_variable_json(self):
        if os.path.exists(self.file_path):
            variable_data = read_file_content(self.file_path)
            return json.loads(variable_data)