#!/usr/bin/python3
# -*- coding: utf-8 -*-

class PackageModel:
    def __init__(self):
        self.dependencies = "{}"
        self.other = ""
        self.pages = "{}"

    def format_tostring(self):
        string_buffer = "{ dependencies: %s , other: %s , pages: %s}" % (self.dependencies, self.other, self.pages)
        return string_buffer
