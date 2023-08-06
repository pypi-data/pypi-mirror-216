#!/usr/bin/python3
# -*- coding: utf-8 -*-

class StringUtils:
    @classmethod
    def is_string_empty(cls, string):
        if string is None or len(string) == 0:
            return True
        return False

    @classmethod
    def contains_ignore_capitals(cls, full_string, sub_string):
        if full_string is None:
            return False
        if sub_string is None:
            return False
        return sub_string.lower() in full_string.lower()
