# coding: utf-8
# Error.py
# Created by Bayonet on 2016/1/15.

class worldError(Exception):
    # 自定义WorldPress 异常类
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
