#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum


class CacheEnum(Enum):
    FIRST_LEVEL_LOCAL_H5_CACHE = "FirstLevelLocalH5Cache"
    SECOND_LEVEL_LOCAL_H5_CACHE = "SecondLevelLocalH5Cache"
    THREE_LEVEL_LOCAL_H5_CACHE = "ThreeLevelLocalH5Cache"

    FIRST_LEVEL_REACT_CACHE = "FirstLevelReactCache"
    SECOND_LEVEL_REACT_CACHE = "SecondLevelReactCache"
    THREE_LEVEL_REACT_CACHE = "ThreeLevelReactCache"
