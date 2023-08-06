#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Page:
    def __init__(self):
        self.id = ""
        self.path = ""
        self.uri = ""
        self.widgets = []
        self.pluginKey = ""

    def format_tostring(self):
        string_buffer = "{ id: %s , path: %s , uri: %s , widgets: %s , pluginKey: %s}" % (
        self.id, self.path, self.uri, self.widgets, self.pluginKey)
        return string_buffer
