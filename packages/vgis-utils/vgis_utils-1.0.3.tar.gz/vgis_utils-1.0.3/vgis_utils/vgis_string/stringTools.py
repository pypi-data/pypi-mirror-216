#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/6/27 14:18
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : stringTools.py
# @Descr   : 
# @Software: PyCharm
import re


class StringHelper:
    def __int__(self):
        pass

    @staticmethod
    # 获取字符串里的数字
    def get_number_in_str(input_str):
        return re.findall("\d+", input_str)

    @staticmethod
    # 获取字符串里的第一个数字
    def get_first_num_in_str(input_str):
        return re.findall("\d+", input_str)[0]

    @staticmethod
    # 获取字符串里的英文
    def get_en_in_str(input_str):
        en_str = re.sub("[\u4e00-\u9fa5\0-9\,\。]", "", input_str)
        return en_str

    @staticmethod
    # 检验字符串是否含有中文字符
    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    @staticmethod
    # 获取字符串里的中文
    def get_cn_in_str(input_str):
        str_result = re.findall("[\u4e00-\u9fa5]", input_str)
        str_return = ""
        for one in str_result:
            str_return = str_return + one
        return str_return

    # 获取两个字符串中间的字符串
    @staticmethod
    def get_str_btw(s, f, b):
        par = s.partition(f)
        return (par[2].partition(b))[0][:]