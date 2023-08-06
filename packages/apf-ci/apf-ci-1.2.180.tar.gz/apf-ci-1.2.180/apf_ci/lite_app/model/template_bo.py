#!/usr/bin/python3
# -*- coding: utf-8 -*-

class TemplateBO:

    def __init__(self):
        self.git_repository = ""
        self.commit_id = ""
        self.build_tool = ""
        self.dev = ""

    def tostring_format(self):
        return "TemplateBO {gitRepository=%s, commitId==%s, buildTool=%s, dev=%s}" % (
            self.git_repository, self.commit_id, self.build_tool, self.dev)
