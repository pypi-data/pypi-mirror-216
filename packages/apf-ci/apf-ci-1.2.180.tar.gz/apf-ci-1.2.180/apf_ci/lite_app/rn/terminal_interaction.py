#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
终端交互模块
"""

envtarget_array = [
        'development',
        'test',
        'preproduction',
        'product',
        'aws',
        'party',
        'aws-california',
        'aws-california-wx',
        'wjt'
    ]

app_type_array = [
        'android',
        'ios'
    ]

env_jenkins_array = [1, 2, 5, 8]

class CommonIn:
    """适用于Windows输入"""

    __boolean_array = [
        'y',
        'yes',
        'n',
        'no'
    ]

    def enter_optional_value(self, parameter_value, parameter_name, prompt):
        if parameter_value:
            if parameter_name == 'envJenkins':
                index_array = [str(value) for value in env_jenkins_array]
                if parameter_value not in index_array:
                    value = input(prompt)
                    return self.enter_value(value, parameter_name, prompt)

        return parameter_value

    def enter_value(self, parameter_value, parameter_name, prompt):
        """
        用于必选项输入，并校验输入值
        :param parameter_value: 输入值
        :param parameter_name: 参数名称
        :param prompt: 提示符
        :return: 输出合法输入值
        """
        if parameter_value == '':
            value = input(prompt)
            return self.enter_value(value, parameter_name, prompt)
        else:
            if parameter_name == 'appType':
                if parameter_value != '0' and parameter_value != '1':
                    value = input(prompt)
                    return self.enter_value(value, parameter_name, prompt)
            elif parameter_name == 'envtarget':
                index_array = [str(i) for i, envtarget in enumerate(envtarget_array)]
                if parameter_value not in index_array:
                    value = input(prompt)
                    return self.enter_value(value, parameter_name, prompt)

        return parameter_value

    def enter_boolean_value(self, parameter_value, prompt):
        """
        用于校验boolean类型的输入值
        :param parameter_value: 输入值
        :param prompt: 提示符
        :return: 输出合法输入值
        """
        if parameter_value != '' and parameter_value.lower() not in self.__boolean_array:
            value = input(prompt)
            return self.enter_boolean_value(value, prompt)

        if parameter_value.lower() == 'y' or parameter_value.lower() == 'yes':
            parameter_value = 'true'
        elif parameter_value.lower() == 'n' or parameter_value.lower() == 'no':
            parameter_value = 'false'

        return parameter_value

class OtherIn:
    """适用于Mac、Linux输入"""

    def select_value(self):
        """
        下拉框选项选择输入值
        :return:
        """
        import inquirer
        questions = [
            inquirer.List('envtarget',
                          message="What envtarget do you need?",
                          choices=envtarget_array,
                          ),
            inquirer.List('appType',
                          message="What appType do you need?",
                          choices=app_type_array,
                          ),
            inquirer.List('envJenkins',
                          message="What envJenkins do you need?",
                          choices=env_jenkins_array,
                          default=8,
                          )
        ]

        answers = inquirer.prompt(questions)
        return answers


