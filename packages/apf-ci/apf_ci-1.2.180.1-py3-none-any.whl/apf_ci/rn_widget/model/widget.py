#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Widget:
    def __init__(self):
        self.path = ""
        self.uri = ""

    def format_tostring(self):
        string_buffer = "{ path: %s , uri: %s}" % (self.path, self.uri)
        return string_buffer
