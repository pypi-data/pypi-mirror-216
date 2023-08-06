#/usr/bin/python3
# -*- coding: utf-8 -*-

class MetaDataNote:
    def __init__(self):
        self.name = ""
        self.label = ""
        self.xpath = ""
        self.file = ""
        self.cdata = ""
        self.type = ""
        self.child_node = {}

    def tostring_format(self):
        return "MetaDataNote { name='%s', label='%s', xpath='%s', file='%s', cdata='%s', type='%s', child_node='%s'" % (
            self.name, self.label, self.xpath, self.file, self.cdata, self.type, self.child_node
        )