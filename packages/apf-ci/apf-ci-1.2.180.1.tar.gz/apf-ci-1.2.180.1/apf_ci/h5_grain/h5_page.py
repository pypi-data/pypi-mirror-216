#!/usr/bin/python3
# -*- coding: utf-8 -*-

class H5Page:
    def __init__(self):
        self.id = ""
        self.path = ""
        self.uri = ""
        self.widgets = []

    def format_tostring(self):
        string_buffer = "{ id: %s , path: %s , uri: %s , widgets: %s}" % (
        self.id, self.path, self.uri, self.widgets)
        return string_buffer
