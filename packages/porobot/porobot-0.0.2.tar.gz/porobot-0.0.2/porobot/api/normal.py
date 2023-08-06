# -*- coding: UTF-8 -*-
'''
@Author  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/6/2 22:52
@Description     ：
'''

import akshare as ak


def chat(question: str = "你好") -> str:
    return ak.nlp_answer(question)
