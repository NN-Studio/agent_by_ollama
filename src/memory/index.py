#!/usr/bin/python3
# coding=utf-8

from os import path
from tools.readFile import readFile
from skills.loadSummary import loadSummary


# 记忆功能
class MemoryClass:
    def __init__(self):
        messages = []

        # 加载用户身份
        messages.append(
            {"role": "system", "content": readFile(path.join("../memory", "USER.md"))}
        )

        # 加载Agent人格设定
        messages.append(
            {"role": "system", "content": readFile(path.join("../memory", "SOUL.md"))}
        )

        # 加载长期记忆
        messages.append(
            {"role": "system", "content": readFile(path.join("../memory", "MEMORY.md"))}
        )

        # 加载skills概述
        messages.append(loadSummary())

        self.messages = messages

    def valueOf(self):
        return self.messages

    def addMessage(self, message):

        # 这里是否可以考虑添加一些判断，来区分是长期记忆还是短期记忆
        # 如果是长期记忆，可以考虑将其保存到文件中，以便下次加载时使用
        # 而短期记忆则只保存在内存中，随着程序的运行而存在。
        return self.messages.append(message)
