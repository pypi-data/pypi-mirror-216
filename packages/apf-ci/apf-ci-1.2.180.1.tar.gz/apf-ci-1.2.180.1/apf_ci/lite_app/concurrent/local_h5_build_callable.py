#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apf_ci.lite_app.service.local_h5_service import *


class LocalH5BuildCallable:

    def call(self, npm_dto):
        logger.debug(" %s" % npm_dto.tostring_format())

        local_h5_service = LocalH5Service()
        local_h5_service.build(npm_dto)

        return "[%s 构建成功]" % npm_dto.npm
