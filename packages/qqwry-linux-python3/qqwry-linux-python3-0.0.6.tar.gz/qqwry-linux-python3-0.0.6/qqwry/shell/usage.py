#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/22 15:21
# @Author  : unclear
# @File    : usage.py
# @Software: PyCharm
from time import ctime

from qqwry import __version__


def run():
    cur_time = ctime()
    text = f"""
    # qqwry

    version {__version__} ({cur_time} +0800)
    """
    print(text)