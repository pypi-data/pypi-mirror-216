#!/usr/bin/python3
# -*- coding:utf-8 -*-

import random

from concurrent.futures import ProcessPoolExecutor

def fib(n, test_arg):
    if n > 30:
        raise Exception('can not > 30, now %s' % n)
    if n <= 30:
        return 1

def use_map():
    nums = [random.randint(0, 33) for _ in range(0, 10)]
    with ProcessPoolExecutor() as executor:
        results = executor.map(fib, nums, nums)
        for result in results:
            print('fib result is %s.' % result)

if __name__ == '__main__':
    # 为了测试 ProcessPoolExecutor中的try catch 无法正常抛出异常。
    # executor.map执行完后，返回是一个迭代器。遍历迭代器就是每个线程的返回值。有可能是1，也有可能是异常
    use_map()