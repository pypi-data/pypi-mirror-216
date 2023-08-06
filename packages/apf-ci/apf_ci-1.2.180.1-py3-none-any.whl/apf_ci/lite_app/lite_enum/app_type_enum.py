#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum


class AppTypeEnum(Enum):
    android = "android"
    ios = "iOS"

    @staticmethod
    def get_platform_by_apptype(app_type):
        # key : android    value: AppTypeEnum.android
        for enum_key, enum_value in AppTypeEnum.__members__.items():
            if app_type.lower() == enum_key.lower():
                return enum_value.value
        return ""
