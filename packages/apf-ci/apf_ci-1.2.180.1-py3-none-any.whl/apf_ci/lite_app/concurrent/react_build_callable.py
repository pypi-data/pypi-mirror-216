#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.service.react_service import *

class ReactBuildCallable:

    def call(self, npm_dto):
        logger.debug(" %s" % npm_dto.tostring_format())

        react_service = ReactService()
        react_service.build(npm_dto)

        return "[%s 构建成功]" % npm_dto.npm
