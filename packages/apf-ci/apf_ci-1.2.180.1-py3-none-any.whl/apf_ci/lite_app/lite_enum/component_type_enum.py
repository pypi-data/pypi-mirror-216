#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum


class ComponentTypeEnum(Enum):
    Android = "react-android"
    iOS = "react-ios"

    @staticmethod
    def get_component_type_by_app_type(app_type):
        # key : Android    value: ComponentTypeEnum.Android
        for enum_key, enum_value in ComponentTypeEnum.__members__.items():
            if app_type.lower() == enum_key.lower():
                return enum_value.value
        return ""