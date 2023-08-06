# coding=utf-8

"""
生成各种符合要求的随机串
"""
__author__ = 'Administrator'

import random
import string
import uuid


class CoRand(object):
    def __init__(self):
        pass

    @staticmethod
    def randomword(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    @staticmethod
    def randomwordnumber(length):
        return ''.join(random.choice(string.digits) for i in range(length))

    @staticmethod
    def uuid(length=16):
        uuid_str = str(uuid.uuid4())
        uuid_str = uuid_str.replace('-', '')

        return uuid_str[:16]

    @staticmethod
    def get_rand_num(num, start=0, end=100):
        serial_arr = list()
        rand_arr = list()
        i = start
        while i <= end:
            serial_arr.append(i)
            i += 1

        for i in range(num):
            rnd_num = random.choice(serial_arr)
            rand_arr.append(rnd_num)
            serial_arr.remove(rnd_num)

        return rand_arr


if __name__  == "__main__":
    rand_o = CoRand()
    # 生成10个字符长度的字符串
    print(rand_o.randomword(10))
    print( rand_o.uuid())
    print(rand_o.get_rand_num(5, end=9))




