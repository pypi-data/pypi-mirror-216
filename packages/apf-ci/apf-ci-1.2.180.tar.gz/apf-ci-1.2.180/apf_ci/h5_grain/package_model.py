#!/usr/bin/python3
# -*- coding:utf-8 -*-


class PackageModel:
    def __init__(self):
        self.dependencies = "{}"
        self.other = ""
        self.pages = "[]"

    def tostring_format(self):
        string_buffer = "{"
        string_buffer += '"dependencies":'
        string_buffer += self.dependencies + ","

        other = self.other
        if other:
            self.other = other[other.find("{") + 1: other.rfind("}")]
            string_buffer += self.other + ","
        string_buffer += '"pages":' + self.pages
        string_buffer += "}"
        return string_buffer
